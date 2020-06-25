import json
import dateutil.parser as dp #Datetime processing libraries
import time, datetime
import hashlib
from .models import CJ_notification, Fiat_transaction
from django.http import HttpResponse
import requests
import os
import telegram.bot as telegram

# test_cj_api_url = 'https://sandbox.clearjunction.com'
# test_wallet_UUID = '901d1848-1b47-45b0-936d-13a604d0a830'
# test_X_API_KEY = '901e90fa-c8a8-49e2-b5bc-20d5f4a1a185'
# test_apiPassword =  '1o23zbsfk3ms'
# test_payout_postbackURL = 'https://cryptostrat.herokuapp.com/cjs/nparser'

cj_api_url = os.environ['CJ_API_URL']
wallet_UUID = os.environ['CJ_WALLET_UUID']
X_API_KEY = os.environ['CJ_X_API_KEY']
apiPassword =  os.environ['CJ_API_Password']
payout_postbackURL = 'https://cryptostrat.herokuapp.com/cjs/nparser'
if (os.environ['DEBUG'] == 'True'):
    payout_postbackURL = 'https://csukdev.herokuapp.com/cjs/nparser'

def get_request_header(body, date):
    global X_API_KEY
    global apiPassword
    
    hashed_apiPassword = hashlib.sha512(apiPassword.encode('utf-8')).hexdigest()
    pre_hashing_request_signature = X_API_KEY.upper() + date + hashed_apiPassword.upper() + body.upper()
    request_signature = hashlib.sha512(pre_hashing_request_signature.encode('utf-8')).hexdigest()
    header = {
      #'Content-Type': 'application/json',
      'Date': date,
      'X-API-KEY': X_API_KEY,
      'Authorization': f'Bearer {request_signature}'
    }
    return header

def send_request(request_url, header, body, request_type = 'GET'):
    try:
        if request_type == 'GET':
            data = requests.get(request_url, headers=header, data = body)
        elif request_type == 'POST':
            data = requests.post(request_url, headers=header, data = body)
        if data.status_code == 200:
            transaction_data =  data.json()
            return transaction_data
        else:
            print('\nError: ')
            print(data)
            print(data.content)
    except:
        print(f'Uknown error requesting {request_url}')

def get_balance():
    global wallet_UUID
    request_url = f'{cj_api_url}/v7/bank/wallets/{wallet_UUID}?returnPaymentMethods=false'
    date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).replace(microsecond=0).isoformat()
    body = ''
    header = get_request_header(body, date)
    data = send_request(request_url, header, body)
    print('resuested')
    if data:
        balance_data = {'GBP': 0, 'EUR': 0}
        for currency in data['amounts']:
            if currency['currencyCode'] == 'GBP':
                balance_data['GBP'] = currency['availableFunds']
            if currency['currencyCode'] == 'EUR':
                balance_data['EUR'] = currency['availableFunds']
        print(balance_data)
        return balance_data
### Processing incoming notifications
def check_sig_and_timestamp(header, body):
    is_header_valid = False
    global X_API_KEY
    global apiPassword
    try:
        date = header['Date']
        X_API_KEY = header['X-API-KEY']
        authorization = header['Authorization']
    
        ### Check timestamp of generated notification if it is close
        is_timestamp_within_limit = False
        request_unix_time_stamp = int(dp.parse(date).strftime('%s'))
        current_unix_time_stamp = int(time.time())
        is_timestamp_within_limit = abs(current_unix_time_stamp - request_unix_time_stamp) < 15
        #check signature
        hashed_apiPassword = hashlib.sha512(apiPassword.encode('utf-8')).hexdigest()
        pre_hashing_request_signature = X_API_KEY.upper() + date + hashed_apiPassword.upper() + body.upper()
        request_signature = hashlib.sha512(pre_hashing_request_signature.encode('utf-8')).hexdigest()
        expected_authorization = request_signature
        
        is_header_valid = (expected_authorization == authorization) and is_timestamp_within_limit
        
        
        is_signature_valid = expected_authorization == authorization
        #print(f'Time stamp is valid: {is_timestamp_within_limit}')
        #print(f'Signature is valid: {is_signature_valid}')
    except:
        pass
    return is_header_valid    

def process_notification(request):
    """ Processes the notification request. Records all notification for recordkeeping and detection of intrusion attempts.  
    Checks for the validity of the signature and timestamp and if valid proceeds to adding the transaction to the database."""
    #### Still to add the processing of BACS, CHAPS, SEPA

    header = request.headers
    body = request.body.decode('utf-8')

    # for safety set as False by default
    valid_sig_and_timestamp= False 
    valid_sig_and_timestamp = check_sig_and_timestamp(header, body)

    #record all notifications regardless of validity to monitor breach attempts and for debugging
    CJ_notification(header = header, body = body , valid = valid_sig_and_timestamp).save()
    
    
    if valid_sig_and_timestamp == True:
        try: #process else return error. Most likely error is body is missing elements or is of an incorrect format
            body =json.loads(body)

            #Assign the variables that are shared between payin and payout notifications
            clientOrder = body['clientOrder']
            orderReference = body['orderReference']
            timestamp = body['operTimestamp']
            amount = body['amount']
            currency =  body['currency']
            operationAmount = body['operationAmount']
            status = body['status']
            returned = body['returned']
            operStatus = body['subStatuses']['operStatus']
            complianceStatus = body['subStatuses']['complianceStatus']

            transactionType = body['type'].replace('Notification', '')
            if transactionType == 'payin':
                #Collect the remaining variables that are not shared between payin and payout notifications
                description = body['paymentDetails']['description']
                payment_method = body['paymentDetails']['paymentMethod']
                iban = ''
                sortCode = ''
                accountNumber = ''
                bankSwiftCode = ''

                #assign variables depending on the transfer type as they have different ones.
                if payment_method == 'BankTransferFps':
                    name =  body['paymentDetails']['payerRequisite']['name']
                    sortCode = body['paymentDetails']['payerRequisite']['sortCode']
                    accountNumber = body['paymentDetails']['payerRequisite']['accountNumber']
                    payeeName = body['paymentDetails']['payeeRequisite']['name']
                if payment_method == 'BankTransferEu':
                    name =  body['paymentDetails']['payerRequisite']['name']
                    iban = body['paymentDetails']['payerRequisite']['iban']
                    bankSwiftCode = body['paymentDetails']['payerRequisite']['bankSwiftCode']
                try: #see if transaction exists and update the fields that need to be updated. 
                    #Some of these do not need to be updated but I still do, to be reviewed later.

                    transaction = Fiat_transaction.objects.get(orderReference = orderReference)
                
                    transaction.clientOrder = clientOrder
                    transaction.orderReference = orderReference
                    transaction.timestamp = timestamp
                    transaction.amount = amount
                    transaction.operationAmount = operationAmount
                    transaction.currency = currency
                    transaction.status = status
                    transaction.returned = returned
                    transaction.operStatus = operStatus
                    transaction.complianceStatus = complianceStatus
                    transaction.payment_method = payment_method
                    transaction.description = description
                    transaction.name = name
                    transaction.iban = iban
                    transaction.sortCode = sortCode
                    transaction.accountNumber = accountNumber
                    transaction.bankSwiftCode = bankSwiftCode
                    transaction.transactionType = transactionType
                
                    transaction.save()
                    
                except Fiat_transaction.DoesNotExist:
                    Fiat_transaction(
                        clientOrder = clientOrder,
                        orderReference = orderReference,
                        timestamp = timestamp,
                        amount = amount,
                        operationAmount = operationAmount,
                        currency = currency,
                        status = status,
                        returned = returned,
                        operStatus = operStatus,
                        complianceStatus = complianceStatus,
                        paymentMethod = payment_method,
                        description = description,
                        name = name,
                        iban = iban,
                        sortCode = sortCode,
                        accountNumber = accountNumber,
                        bankSwiftCode = bankSwiftCode,
                        transactionType = transactionType,
                        ).save()
                if is_payee_name_acceptable(payeeName):
                    telegram.send_new_payment_message.delay(f'<b>Payin:</b> \nName:{name} \nAmount: {operationAmount} \nReference: {description} \nOperation Status: {operStatus} \nCompliance Status: {complianceStatus}')
                else:
                    telegram.send_new_payment_message.delay(f'<b>Payin Manual Intervention Required!!!:</b> \nError: Customer sent funds with our account name as: {payeeName} \nName:{name} \nAmount: {operationAmount} \nReference: {description} \nOperation Status: {operStatus} \nCompliance Status: {complianceStatus}')
            elif transactionType == 'payout':
                try: #see if transaction exists which it should
                    transaction = Fiat_transaction.objects.get(orderReference = orderReference)
                
                    transaction.clientOrder = clientOrder
                    transaction.orderReference = orderReference
                    transaction.timestamp = timestamp
                    transaction.amount = amount
                    transaction.operationAmount = operationAmount
                    transaction.currency = currency
                    transaction.status = status
                    transaction.returned = returned
                    transaction.operStatus = operStatus
                    transaction.complianceStatus = complianceStatus
                    transaction.transactionType = transactionType
                
                    transaction.save()
                except:
                    return HttpResponse(status=400, content='Transaction not found')
            return HttpResponse(status=200, content=orderReference)
        except:
            return HttpResponse(status=400, content='Invalid body content')

    else: 
        return HttpResponse(status=401, content='Invalid signature or timestamp')
 
 
### Sending transactions

def send_FPS(transaction_data):
    global wallet_UUID
    global payout_postbackURL

    date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).replace(microsecond=0).isoformat()

    currency = transaction_data['currency']
    amount = transaction_data['amount']
    description = transaction_data['description']
    phone = transaction_data['phone']
    birthDate = transaction_data['birthDate']
    birthPlace = transaction_data['birthPlace']

    addressCountry = transaction_data['addressCountry']
    addressState = transaction_data['addressState']
    addressCity = transaction_data['addressCity']
    addressZip = transaction_data['addressZip']
    addressStreet = transaction_data['addressStreet']

    documentType = transaction_data['documentType']
    documentNumber = transaction_data['documentNumber']
    documentIssuedBy = transaction_data['documentIssuedBy']
    documentIssuedCountryCode = transaction_data['documentIssuedCountryCode']
    
    documentIssueDate = transaction_data['documentIssueDate']
    documentExpiryDate = transaction_data['documentExpiryDate']

    if birthDate != None:
        birthDate = birthDate.strftime('%Y-%m-%d')
    if documentIssueDate != None:
        documentIssueDate = documentIssueDate.strftime('%Y-%m-%d')
    if documentExpiryDate != None:
        documentExpiryDate = documentExpiryDate.strftime('%Y-%m-%d')


    firstName = transaction_data['firstName']
    lastName = transaction_data['lastName']
    middleName = transaction_data['middleName']

    sortCode = transaction_data['sortCode']
    accountNumber = transaction_data['accountNumber']
    date2 = datetime.datetime.utcnow()
    clientOrder = description + str(date2.day) + str(date2.hour)#has to be unique 
    body = {"clientOrder": clientOrder,
            'postbackUrl': payout_postbackURL,
            "currency": currency,
            "amount": amount,
            "description": description,
            "payer": {"walletUuid": wallet_UUID,
                     },
            "payee": {"individual": {"phone": phone,
                                     "email": None,
                                     "birthDate": birthDate,
                                     "birthPlace": birthPlace,
                                     "address": {"country": addressCountry,
                                                 "zip": addressZip,
                                                 "city": addressCity,
                                                 "street": addressStreet,
                                                },
                                     "document": {"type": documentType,
                                                  "number": documentNumber,
                                                  "issuedCountryCode": documentIssuedCountryCode,
                                                  "issuedBy": documentIssuedBy,
                                                  "issuedDate": documentIssueDate,
                                                  "expirationDate": documentExpiryDate,
                                                 },
                                     "lastName": lastName,
                                     "firstName": firstName,
                                     "middleName": middleName,
                                    }
                     },
            "payeeRequisite": {"sortCode": sortCode,
                               "accountNumber": accountNumber,
                              },
            "payerRequisite": {#"sortCode": '',
                               #"accountNumber": '',
                               #"iban": '',
                               #"bankSwiftCode": ''
                              }
           }
    request_url = f'{cj_api_url}/v7/gate/payout/bankTransfer/fps?checkOnly=false'
    body = json.dumps(body)
    header = get_request_header(body, date)
    
    #data = send_request(request_url, header, body, request_type = 'POST')
    
    #try:
    if 1 == 1:
        data = requests.post(request_url, headers=header, data = body)
        print(data.status_code)
        if data.status_code == 201 :
            transaction_data =  data.json()

            clientOrder = transaction_data['clientOrder']
            orderReference = transaction_data['orderReference']
            timestamp = transaction_data['createdAt']
            amount = amount #set previously
            currency = currency #set previousy 
            operStatus = transaction_data['subStatuses']['operStatus']
            complianceStatus = transaction_data['subStatuses']['complianceStatus']
            paymentMethod = 'BankTransferFps'
            description = description #set previously
            name = firstName + lastName #set previously
            sortCode = sortCode #set previously
            accountNumber = accountNumber #set previously
            transactionType = 'payout'
            Fiat_transaction(
                    clientOrder = clientOrder,
                    orderReference = orderReference,
                    timestamp = timestamp,
                    amount = amount,
                    operationAmount = None,
                    currency = currency,
                    status = operStatus,
                    returned = None,
                    operStatus = operStatus,
                    complianceStatus = complianceStatus,
                    paymentMethod = paymentMethod,
                    description = description,
                    name = name,
                    iban = None,
                    sortCode = sortCode,
                    accountNumber = accountNumber,
                    bankSwiftCode = None,
                    transactionType = transactionType,
                ).save()
            return 'Successful' + operStatus
        else:
            return data.content.decode()
            
    #except:
     #   data = 'Unable to send request to Clearjunction'


def is_payee_name_acceptable(name):
    acceptable_names = [
        'm5fintechltd',
        'm5fintech',
    ]
    if name.lower().replace(' ','') in acceptable_names:
        return True
    else:
        return False