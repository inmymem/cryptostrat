import os
import requests
import time
import hmac, hashlib
import base64
import json
from itertools import permutations 
from .models import RawSumSubNotification, Application, IdDoc, Address, AddressDoc, Person
import telegram.bot as telegram
from django.utils import timezone
from .verification_links import get_verification_url


# test_api_url = 'https://test-api.sumsub.com'
# test_username = 'cryptostrat_shahraab_ahmed_test'
# test_password = 	'l1edm26g5u'

# test_app_token = 'tst:WVqOZSQBxsWvSGm30xDi8kAU.k4WLu2dLgZt1cds8udoBvVTCNsxvPGTv'
# test_app_token_secret = 'mg1JHruBGADKiSdMc5kiESbBvpynq51x'

api_url = os.environ['SUMSUB_API_URL']
APP_TOKEN_KEY = os.environ['SUMSUB_APP_TOKEN']
APP_TOKEN_SECRET = os.environ['SUMSUB_SECRET_KEY']



token_lifespan_seconds = 1800


def get_access_token_for_sdk(userId, token_lifespan_seconds = token_lifespan_seconds ):
    """SDK tokens are valid for a limited time. You need to generate a new websdk token everytime 
    the user wants to complete the verification so that you are able to initialize the SDK window."""

    end_url = f'/resources/accessTokens'
    request_method = 'POST'
    parameters = {'userId': userId, 'ttlInSecs': token_lifespan_seconds}
    headers=''
    body = ''
    body = json.dumps(body)
    
   

    request = requests.Request(request_method, url=(api_url+end_url),headers= headers, data = body, params = parameters)
    response = sign_and_send_request(request)
    if response.status_code == 200:
        response = response.json()
        token = response['token']
        userId = response['userId']
        return token


basic_check = {
    "description":"",
    "applicant":{
        "email":"",
        "requiredIdDocs":{
            "docSets":[
                {"idDocSetType":"IDENTITY", "types":["ID_CARD","PASSPORT","DRIVERS","RESIDENCE_PERMIT"],"fields":None},
                {"idDocSetType":"SELFIE","types":["VIDEO_SELFIE"],"fields":None,"videoRequired":"liveness"},
                {"idDocSetType":"PROOF_OF_RESIDENCE","types":["UTILITY_BILL"],"subTypes":None,"fields": None,}
                ]
            },
        #"externalUserId":"random-wyavw5364zZSFGSegyjyiudddddd"
        }
    }
# basic_check_old = {
#     "description":"",
#     "applicant":{
#         "email":"",
#         "requiredIdDocs":{
#             "docSets":[
#                 {"idDocSetType":"IDENTITY", "types":["ID_CARD","PASSPORT","DRIVERS","RESIDENCE_PERMIT"],"fields":None},
#                 {"idDocSetType":"SELFIE","types":["SELFIE"],"fields":None,"videoRequired":"optional"},
#                 {"idDocSetType":"SELFIE2","types":["VIDEO_SELFIE"],"fields":None,"videoRequired":"liveness"},
#                 {"idDocSetType":"PROOF_OF_RESIDENCE","types":["UTILITY_BILL"],"subTypes":None,"fields":[
#                     {"name":"street","required":True},
#                     {"name":"subStreet","required":False},
#                     {"name":"town","required":True},
#                     {"name":"state","required":False},
#                     {"name":"postCode","required":True},
#                     {"name":"country","required":True}]
#                     }
#                 ]
#             },
#         "externalUserId":"random-wyavw5364zZSFGSegyjyiudddddd"
#         }
#     }


def create_applicant_request(client, applicant_request_type= basic_check):
    end_url = '/resources/accounts/-/applicantRequests'
    request_method = 'POST'
    parameters = None
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }

    applicant_request_type['applicant']['externalUserId'] = client.sumsub_external_user_id
    body = applicant_request_type
    body = json.dumps(body)
    request = requests.Request(request_method, url=(api_url+end_url), headers= headers, data = body, params = parameters)
    response = sign_and_send_request(request)

    if response.status_code == 200:
        response = response.json() 
        Application.objects.create(
            client = client,
            status = 'requestCreated',
            )
    elif response.status_code == 204: #means it has already been created at sumsub
        try:
            Application.objects.get(client = client)
        except Application.DoesNotExist:   
            Application.objects.create(client = client, status ='requestCreated')


def reset_applicant(applicant_id):
    end_url = '/resources/applicants/{applicant_id}/reset'
    request_method = 'POST'
    parameters = None
    headers = {
        }
    body = {'applicantId': applicant_id}
    request = requests.Request(request_method, url=(api_url+end_url), headers= headers, data = body, params = parameters)
    response = sign_and_send_request(request)


def get_applicant_data(applicantId):
    """To get the detailed applicant data that was extracted after the review process. 
    E.G ID doc details, address details..."""
    end_url = f'/resources/applicants/{applicantId}'
    request_method = 'GET'

    request = requests.Request(request_method, url=(api_url+end_url))
    response = sign_and_send_request(request)
    return response.json()

def sign_and_send_request(request: requests.Request) -> requests.Request:
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    request_path = prepared_request.url.replace(api_url,'')
    body = prepared_request.body
    if body:
        data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + request_path.encode('utf-8') + body.encode('utf-8')
    else:
        data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + request_path.encode('utf-8')
    # hmac needs bytes
    signature = hmac.new(
        APP_TOKEN_SECRET.encode('utf-8'),
        data_to_sign,
        digestmod=hashlib.sha256
    )
    prepared_request.headers['X-App-Token'] = APP_TOKEN_KEY
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
    s = requests.Session()
    response = s.send(prepared_request)
    return response


def process_notification(request):
    header = request.headers
    body = request.body.decode()

    #record all notifications raw for debugging in case of need
    RawSumSubNotification.objects.create(header = header, body = body)
    
    #add authentication method
    notification = json.loads(body)
    
    notification_type = notification['type']
    notification_types = (
        'applicantCreated',  #as name suggests when an applicnt is created
        'applicantPending', # When a user has uploaded all documents and the checking is pengding  
        'applicantOnHold',  #Processing of the application is on hold for an agreed reason
        'applicantPrechecked',# Primary data processing is completed
        'applicantReviewed', #review completed
        ) 

    applicant_id = notification['applicantId']
    inspection_id = notification['inspectionId']  #inspection ID that contains a result of the applicant
    correlation_id = notification['correlationId']  #an ID to debug in case of unexpected errors (should be provided to Sum&Substance)
    externalUser_id = notification['externalUserId']
    notification_type = notification['type']
    review_status = notification['reviewStatus']

    #models that will have values only when there is a review result
    review_answer = None
    review_reject_type = None
    moderation_comment = None
    client_comment = None
    reject_labels = None

    #review result only present when a review has actually been conducted. Can be present in pending state (applicantPending) too if a retry is required.
    if 'reviewResult' in notification: 
        client = Client.objects.get(sumsub_external_user_id = externalUser_id)
        #dict of review result fields that vary depending on the review answer
        review_result = notification['reviewResult']

        review_answer = review_result['reviewAnswer']
        if review_answer == 'RED':
            review_reject_type = review_result['reviewRejectType']
            reject_labels = review_result['rejectLabels']
            #convert it to text to be able to store in a textfield
            reject_labels = json.dumps(reject_labels)
            #moderation comment not always present
            if 'moderationComment' in review_result:
                moderation_comment = review_result['moderationComment']
            if 'clientComment' in review_result:
               client_comment = review_result['clientComment']
            #turn verifications that sumsub does into false.
            client.id_verified = False
            client.liveness_verified = False
            client.address_verified = False
            client.video_verified = False
            #client.source_of_funds_verified = False
            #client.source_of_funds_limit = False
            #client.company_verified = False
            telegram.send_sumsub_manual_intervention_required_message.delay(f'<b>Verification RED for {client.identifier()}. Review Reject Type: {review_reject_type}</b>')
        if review_answer == 'GREEN': #thought about adding: and review_status == 'completed' but unecessary
            """We get the first item in the list as it is expected to be the only one. Their api can return several 
            incase get_applicant is called with external_id. That is not possible in our case since our function uses 
            their unique applicant Id and even our external Ids are unique."""
            applicant_data = get_applicant_data(applicant_id)['list']['items'][0] 
            #we proceed to update 3 tables and check consistency of the data they provide. Need a flag for inconsistent data.
            #Start with the Person model and get the info from the root of applicant_info
            try:
                update_or_create_id_docs(applicant_data, client) #updates client.id_verified and client.address_verified
            except Exception as e:
                telegram.send_critical_error_message.delay(f'Sumsub - error creating Id Docs for {client.uuid}')
            try:
                person = update_or_create_person(applicant_data, client)
            except Exception as e:
                telegram.send_critical_error_message.delay(f'Sumsub - error creating Person for {client.uuid}')
            client.liveness_verified = is_liveness_verified(applicant_data)
            if client.localbitcoins_real_name:
                client.name_match_checked = do_names_match(client, person)
            else:
                client.name_match_checked = True
            ##############
            name_components = [person.first_name, person.middle_name, person.last_name]
            client.real_name = ''
            for name_component in name_components:
                if name_component != None:
                    client.real_name = (client.real_name + ' ' + name_component).lstrip()
            #selfie have to see if they verify it. For now just send a message
        client.save()
        telegram.send_user_verified_message(f'{client.identifier()} verification result: {review_answer}')
            #send notification to lbc module or to indicate a check has been completed 
    

    Application.objects.filter(client__sumsub_external_user_id = externalUser_id).update(
        applicant_id = applicant_id,
        inspection_id = inspection_id,
        correlation_id = correlation_id,
        review_status = review_status,
        status = notification_type,
        review_answer = review_answer,
        review_reject_type = review_reject_type,
        moderation_comment = moderation_comment,
        client_comment = client_comment,
        reject_labels = reject_labels,
        )

def get_field_if_present(dictionary, field_name):
    if field_name in dictionary:
       return dictionary[field_name]
    else: 
        return None


def update_or_create_person(applicant_data, client):
    """here manage what is in default and gets updated and what doesn't"""
    #info has all the details of the applicant and their submitted docs with their respective details.
    applicant_info = applicant_data['info']
    #Get the address fields from the first in .addresses as only one is expected
    applicant_address_info = applicant_info['addresses'][0]
    try:
        address, created = Address.objects.update_or_create(
            sub_street = get_field_if_present(applicant_address_info, 'subStreet'),
            street = applicant_address_info['street'],
            state = get_field_if_present(applicant_address_info, 'state'),
            town = applicant_address_info['town'],
            postCode = applicant_address_info['postCode'],
            country = applicant_address_info['country'],  
            )
    except Exception as e:
        print(e)
    try:
        person, created = Person.objects.update_or_create(
            client = client,
            defaults = {
                'first_name' : applicant_info['firstName'],
                'middle_name' : get_field_if_present(applicant_info, 'middleName'),
                'last_name' : applicant_info['lastName'],
                'date_of_birth' : applicant_info['dob'],
                'gender' : applicant_info['gender'],
                'place_of_birth' : get_field_if_present(applicant_info, 'placeOfBirth'),
                'country_of_residence' : get_field_if_present(applicant_info, 'country'),
                'nationality' : get_field_if_present(applicant_info, 'nationality'),
                'country_of_birth' : get_field_if_present(applicant_info, 'countryOfBirth'),
                'state_of_birth' : get_field_if_present(applicant_info, 'stateOfBirth'),
                'address' : address
            }
        )
    except Exception as e:
        print(e)
    return person

def update_or_create_id_docs(applicant_data, client):
    applicant_info = applicant_data['info'] #info has all the details of the applicant and their submitted docs with their respective details.
    id_doc_id_types = ['PASSPORT', 'ID_CARD', 'DRIVERS', 'RESIDENCE_PERMIT']
    #They list both proof of address and standard ID documents under idDocs. We have to process them differently
    for id_doc in applicant_info['idDocs']:
        if id_doc['idDocType'] in id_doc_id_types:
            if id_doc['idDocType'] != 'RESIDENCE_PERMIT':
                #create an error if no last name is in the files
                last_name = id_doc['lastName']
            id_document = IdDoc.objects.update_or_create(
                client = client,
                doc_type = id_doc['idDocType'],
                country = id_doc['country'],
                first_name = id_doc['firstName'],
                middle_name = get_field_if_present(id_doc, 'middleName'),
                last_name = get_field_if_present(id_doc, 'lastName'),
                issue_date = get_field_if_present(id_doc, 'issuedDate'),
                valid_until = id_doc['validUntil'],
                number = id_doc['number'],
                date_of_birth = id_doc['dob'],
                )
            client.id_verified = True
        elif id_doc['idDocType'] == 'UTILITY_BILL':
            proof_of_address = AddressDoc.objects.update_or_create(
                client = client,
                doc_type = id_doc['idDocType'],
                first_name = id_doc['firstName'],
                middle_name = get_field_if_present(id_doc, 'middleName'),
                last_name = get_field_if_present(id_doc, 'lastName'),
                issue_date = id_doc['issuedDate'],
                sub_street = get_field_if_present(id_doc['address'], 'subStreet'),
                street = id_doc['address']['street'],
                state = get_field_if_present(id_doc['address'], 'state'),
                town = id_doc['address']['town'],
                postCode = id_doc['address']['postCode'],
                country = id_doc['address']['country'],
            )
            client.address_verified = True
    return id_document, proof_of_address


def is_liveness_verified(applicant_data):
    #Info, does not show if liveness was performed. The only way to check is through the required id docs.
    applicant_required_id_docs = applicant_data['requiredIdDocs']
    liveness_verified = False
    if 'liveness' in json.dumps(applicant_required_id_docs):
        liveness_verified = True
    return liveness_verified

def do_names_match(client, person):
    """To check if the name extracted from the verification is the same as the name that was provided
    on localbitcoins and other platforms"""
    platform_verified_name = client.localbitcoins_real_name
    verification_name_components = [person.first_name, person.middle_name,person.last_name,]
    # name components
    if not person.middle_name:
        verification_name_components = [person.first_name, person.last_name]
    #Sometimes you have multiple names in each component. Break them down and create a name components list with them.
    verification_name = ''
    for verification_name_component in verification_name_components:
        verification_name = verification_name.replace('-', ' ')
        verification_name += ' ' + verification_name_component
    verification_name = verification_name.lstrip()
    verification_name_components = verification_name.split()
    #As we will be permuting, to avoid getting the process stuck on permforming this calculation. Should never
    #happen but if it does we can see how often and what not to fix it.
    if len(verification_name_components) > 9:
        return False
    #The order of the names can be different so test all of them
    verification_name_match_possibilities = permutations(verification_name_components)
    for name in verification_name_match_possibilities:
        verification_name = (' '.join(name))
        verification_name_edited = verification_name.lower().replace(' ', '')
        platform_verified_name_edited = platform_verified_name.lower().replace(' ', '')
        if verification_name_edited == platform_verified_name_edited:
            return True
        elif platform_verified_name_edited in verification_name_edited:
            return True
        elif verification_name_edited in platform_verified_name_edited:
            return True
    #send telegram message
    telegram.send_sumsub_manual_intervention_required_message.delay(f'<b>Name does not match for {client.identifier()}.</b>\n<i>Platform Name: {platform_verified_name.title()}</i>\n<i>Verification Name: {verification_name_components}</i>')
    #telegram.send_further_verifications_message.delay(f'<b>Name does not match for user {client.uuid}.</b>\n<i>Platform Name: {platform_verified_name.title()}</i>\n<i>Verification Name: {verification_name_components}</i>')
    return False


def set_up_verification_credentials(client):
    if client.sumsub_external_user_id == None:
        client.sumsub_external_user_id = str(client.uuid)
    create_applicant_request(client)
    sdk_token = get_access_token_for_sdk(client.sumsub_external_user_id, token_lifespan_seconds)
    client.sumsub_sdk_access_token = sdk_token
    client.sumsub_sdk_access_token_expiry = timezone.now() + timezone.timedelta(seconds = token_lifespan_seconds)
    client.save()

def renew_verification_token(client):
    sdk_token = get_access_token_for_sdk(client.sumsub_external_user_id, token_lifespan_seconds)
    client.sumsub_sdk_access_token = sdk_token
    client.sumsub_sdk_access_token_expiry = timezone.now() + timezone.timedelta(seconds = token_lifespan_seconds)
    client.save()
    return True


def create_applicant_and_get_verification_url(client):
    set_up_verification_credentials(client)
    return get_verification_url(client)
#get_verification_url_lbc('sidiberd', 'sidiberd', '7225e208-8806-47e4-9f46-32d3e2497d98')
# print(get_verification_url_lbc('01b44932-eea5-4883-95ac-66ecf66a57e1', 'sidiberd'))
#implement function to add required document /resources/applicants/{applicantId}/requiredIdDocs. E.G For proof of funds...
#
#print(get_applicant_data('5e9b72370a975a656d67f9d7'))

#create_applicant_request('momo', applicant_request_type= basic_check)

#sdk_token = get_access_token_for_sdk('momo' ,token_lifespan_seconds = 600 )
#print(f'https://cryptostrat.herokuapp.com/lbc/verify/momo/{sdk_token}')

#print(get_verification_url('sidiberd'))


#scan_address(applicantId='5ed80e030a975a6de48b06be' , currency= 'BTC', direction = 'withdrawal', txn ='' , address = '15VrVsyjoVoANWU5Ye4JbbJscjDRP3ZxyZ')
