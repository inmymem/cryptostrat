from .lbcapi import api
from .lbc import get_contact, send_message, broker_account_name, set_as_trusted, set_as_trusted_with_feedback
import requests
import json
from reference_prices.models import ReferencePrice
from verifications.sumsub import create_applicant_and_get_verification_url
import telegram.bot as telegram
import time
from . import messages
from django.db.models import Q
from itertools import permutations
from clients.models import Client, Transaction

bank_account = {'name': 'M5 Fintech LTD', 'number': '29901023', 'sort_code': '041307'}
def process_new_contact(contact_id):
    contact = get_contact(contact_id)
    #conditions that need to be checked before proceeding
    is_broker = (broker_account_name == contact['advertisement']['advertiser']['username'])
    not_cancelled = (None == contact['canceled_at'])
    if is_broker: #and not_cancelled:
        buying = contact['is_buying']
        selling = contact['is_selling']

        #Case where we are selling
        if selling == True and buying == False:
            process_sell_transaction(contact)
        if selling == False and buying == True:
            process_buy_transaction(contact)
def process_buy_transaction(contact):
    client = update_or_create_client(contact)
    transaction, transaction_created = update_or_create_transaction(contact, client, action = 'B', bank_account = bank_account)
    if transaction.status == 'i' and transaction_created:
        #we make sure the transaction is created to not send duplicate notifications if LBC is slow
        telegram.send_new_offer_message.delay(f'Cryptostrat - New Buy offer #{transaction.localbitcoins_contact_id} ({transaction.amount_fiat} GBP by {client.localbitcoins_username})')
        verification_tier = client.get_verification_tier()
        if verification_tier == 0:
            print('Hello')
            verification_url = create_applicant_and_get_verification_url(client)
            messages.send_bt0_to_bt1_verification_required.delay(transaction.localbitcoins_contact_id, verification_url)
            transaction.status = 'pv1'
            transaction.save()
        if verification_tier >= 1:
            sending_to_verified_name = do_names_match(client.real_name, transaction.client_bank_account_name)
            if not sending_to_verified_name:
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'3rd party payment \nVerified name: {client.real_name} | Requested payment name: {transaction.client_bank_account_name}', required_intervention = 'Verify name and manage trade depending on situation. Name_match_checked has been set to False for this user. Do not forget to set back to True if you verify the user.')
                client.name_match_checked = False
                client.save()
                transaction.status = 'pv1'
                transaction.save()
            elif sending_to_verified_name:
                messages.send_bt1_initial_message.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New Buy offer- User is T{verification_tier} verified', required_intervention = 'Send payment')
                transaction.status = 'pp'
                transaction.save()


def update_or_create_client(contact):
    buying = contact['is_buying']
    selling = contact['is_selling']
    if selling == True and buying == False:
        client, created = Client.objects.update_or_create(
            localbitcoins_username = contact['buyer']['username'],
            defaults = {
                'company_name' : contact['buyer']['company_name'],
                'localbitcoins_feedback_score' : int(contact['buyer']['feedback_score']),
                'localbitcoins_trade_count' : int( contact['buyer']['trade_count'].replace('+', '').replace(' ', '')),
                'localbitcoins_country_code_phone_number' : contact['buyer']['countrycode_by_phone_number'],
                'localbitcoins_last_country_code_ip' : contact['buyer']['countrycode_by_ip'],
            } 
        )
        if created:
            client.localbitcoins_real_name = contact['buyer']['real_name']
            client.sumsub_external_user_id = str(client.uuid)
            client.save()
    if buying == True and selling == False:
        client, created = Client.objects.update_or_create(
            localbitcoins_username = contact['seller']['username'],
            defaults = {
                'localbitcoins_feedback_score' : int(contact['seller']['feedback_score']),
                'localbitcoins_trade_count' : int( contact['seller']['trade_count'].replace('+', '').replace(' ', '')),
                'localbitcoins_country_code_phone_number' : None,
                'localbitcoins_last_country_code_ip' : None,
            }     
        )
        if created:
            client.localbitcoins_real_name = contact['account_details']['receiver_name'] #not in contact contact['seller']['real_name'] so get it from account name they ask us to send to, Find more elegant solution.
            client.company_name = None
            client.sumsub_external_user_id = str(client.uuid)
            client.save()

    return client  
def process_sell_transaction(contact):
    client = update_or_create_client(contact)
    #collect transaction information
    transaction, transaction_created = update_or_create_transaction(contact, client, action = 'S',bank_account= bank_account)
    #Get which verifications needed, create link, and send it to them with the message.
    if transaction.status == 'i' and transaction_created: #i is initial transaction where nothing has been done yet and make sure it was just created because lbc being slow creates issues
        telegram.send_new_offer_message.delay(f'Cryptostrat - New Sell offer #{transaction.localbitcoins_contact_id} ({transaction.amount_fiat} GBP by {client.localbitcoins_username})')
        verification_tier = client.get_verification_tier()
        total_volume = client.total_sell_volume()
        required_verification_tier = transaction.get_sell_required_verification_tier()
        if verification_tier >= required_verification_tier:
            messages.send_within_limits_starting_message.delay(transaction.localbitcoins_contact_id, client.real_name, transaction.get_bank_account(), transaction.reference)
            transaction.status = 'pp'
            transaction.save()
        elif required_verification_tier == 1:
            if verification_tier == 0:
                verification_url = create_applicant_and_get_verification_url(client)
                messages.send_st0_to_st1_verification_required.delay(transaction.localbitcoins_contact_id, verification_url)
                transaction.status = 'pv1'
                transaction.save()
        elif required_verification_tier == 2:
            if verification_tier == 0 and transaction.amount_fiat >= transaction.get_st0_and_st1_one_transaction_limit():
                verification_url = create_applicant_and_get_verification_url(client)
                messages.send_st0_to_st2_2K_transaction_verification_required.delay(transaction.localbitcoins_contact_id, verification_url)
                transaction.status = 'pv1'
                transaction.save()
            elif verification_tier == 0:
                verification_url = create_applicant_and_get_verification_url(client)
                messages.send_st0_st2_transaction_verification_required.delay(transaction.localbitcoins_contact_id, verification_url)
                transaction.status = 'pv1'
                transaction.save()
            elif verification_tier == 1 and transaction.amount_fiat >= transaction.get_st1_limit():
                messages.send_st1_to_st2_verification_required.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New transaction - User is T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                transaction.status = 'pv2'
                transaction.save()
            elif verification_tier == 1 and transaction.amount_fiat >= transaction.get_st0_and_st1_one_transaction_limit():
                messages.send_st1_to_st2_2K_transaction_verification_required.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New transaction - User is T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                transaction.status = 'pv2'
                transaction.save()
        elif required_verification_tier == 3:
            if verification_tier == 0:
                verification_url = create_applicant_and_get_verification_url(client)
                messages.send_st0_to_st3_transaction_verification_required.delay(transaction.localbitcoins_contact_id, verification_url)
                transaction.status = 'pv1'
                transaction.save()
            if verification_tier == 1:
                messages.send_st1_to_st3_verification_required.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New transaction - User is T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                transaction.status = 'pv2'
                transaction.save()
            if verification_tier == 2:
                messages.send_st2_to_st3_verification_required.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New transaction - User is T{verification_tier} verified', required_intervention = 'Complete T3 verification')
                transaction.status = 'pv3'
                transaction.save()
        elif required_verification_tier == 6:
            telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'New transaction - User is T{verification_tier} verified', required_intervention = 'New proof of funds check required. User is past the proof of funds limit.')
            transaction.status = 'pv3'
            transaction.save()
        elif required_verification_tier == 7:
            pass


              
def process_user_just_verified(username):
    #to implement push mechanism of verification to update a transaction when a new verification is set
    pass

def update_or_create_transaction(contact, client,  action, status = None, bank_account = None, pre_transaction_verification_tier= None):
    #check if transaction was created so that if it is pv already you dont send message twice
    #do not update status as it causes a race condition and status loop
            # removed bank_account = transaction.get_bank_account()
    to_update = {
            'payment_completed_at' : contact['payment_completed_at'],
            'closed_at' : contact['closed_at'],
            }
    if pre_transaction_verification_tier == None:
        pre_transaction_verification_tier = client.get_verification_tier()
    if contact['released_at'] != None:
        to_update['status'] = 'r' #released
        to_update['closed_at'] = contact['released_at']
    elif contact['canceled_at'] != None or (contact['released_at'] == None and contact['closed_at'] != None):
        to_update['status'] = 'c' #cancelled
    elif contact['disputed_at'] != None:
        to_update['status'] = 'd' #dispute
    elif contact['payment_completed_at'] != None and contact['closed_at'] == None:
        if action == 'B' and status == 'pp':
            to_update['status'] = 'p' 
        # if action == 'S':
        #     #paid updated by mark_transaction_as_paid method which is called by the lbc notification. (Commented it as it can get there before the notification and tht would prevent telegram notification sending.)
        #     del to_update['status']
        to_update['payment_completed_at'] = contact['payment_completed_at']
    #elif status == None:
        #status = 'i'   #pending verification
        #del to_update['status']
    if action == 'S' and bank_account:
        to_update['bank_account_name'] = bank_account['name']
        to_update['bank_account_number'] = bank_account['number']
        to_update['bank_account_sort_code'] = bank_account['sort_code']
    if action == 'B':
        #checks for valid account details. LBC does check for integer and length of acc num and sc. Need to implement advanced checks and name checks.
        client_bank_account_number = contact['account_details']['account_number']
        client_bank_account_sort_code = contact['account_details']['sort_code']
        to_update['client_bank_account_name'] = contact['account_details']['receiver_name']
        to_update['client_bank_account_number'] = client_bank_account_number
        to_update['client_bank_account_sort_code'] = client_bank_account_sort_code

        to_update['bank_account_name'] = bank_account['name']
        to_update['bank_account_number'] = bank_account['number']
        to_update['bank_account_sort_code'] = bank_account['sort_code']
        valid = True
        #length
        if len(client_bank_account_number) != 8 or len(client_bank_account_sort_code) != 6:
            valid = False
        try:
            int(client_bank_account_number)
            int(client_bank_account_sort_code)
        except:
            valid = False
        if valid == False:
            telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'Invalid account details provided\nName: {bank_account_name}\nAccount number: {bank_account_number}\n Sort code: {bank_account_sort_code}', required_intervention = 'Get correct details from user')
    transaction, created = Transaction.objects.update_or_create(
        platform = 'LBC',
        client = client,
        action = action,
        amount_fiat = float(contact['amount']),
        amount_btc = float(contact['amount_btc']),
        fee_btc = float(contact['fee_btc']),
        localbitcoins_contact_id = contact['contact_id'],
        created_at = contact['created_at'], 
        pre_transaction_verification_tier = pre_transaction_verification_tier,
        defaults = to_update
        )
    if created:
        transaction.exchange_price = ReferencePrice.objects.get(currency_pair = 'BTCGBP').price
        transaction.reference = transaction.get_reference()
    return transaction, created


def mark_transaction_as_paid(contact_id):
    transaction = Transaction.objects.get(localbitcoins_contact_id= contact_id)
    if transaction.status not in ['f', 'r', 'c', 'p']:
        transaction.status = 'p'
        transaction.save()
        telegram.send_localbitcoins_payment_complete_message.delay(f'<b>Payment marked complete:</b> #{contact_id} ({transaction.amount_fiat} GBP by {transaction.client.localbitcoins_username})')
        telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'Payment marked as complete', required_intervention = 'Check bank account for payment and release coins.')
def do_names_match(verified_name, bank_account_name):
    """To check if the name extracted from the verification is the same as the name that was provided
    on localbitcoins and other platforms"""
    name_matches = False
    verification_name_components = bank_account_name.split()
    #the order of the names can be different so test all of them
    verification_name_match_possibilities = permutations(verification_name_components)
    for name in verification_name_match_possibilities:
        verification_name = (' '.join(name))
        if verification_name.lower().replace(' ', '') == verified_name.lower().replace(' ', ''):
            name_matches = True
            return True
    #send telegram message
    #telegram.send_manual_intervention_required_message.delay(f'<b>Name does not match for user {user.username}.</b>\n<i>Platform Name: {platform_verified_name.title()}</i>\n<i>Verification Name: {verification_name_components}</i>')
    #telegram.send_further_verifications_message.delay(f'<b>Name does not match for user {user.username}.</b>\n<i>Platform Name: {platform_verified_name.title()}</i>\n<i>Verification Name: {verification_name_components}</i>')
    return False


from celery.decorators import task
@task(name="localbitcoins_process_pending_transactions")
def process_pending_transactions():
    pending_verification_transactions = Transaction.objects.filter(Q(status = 'pv1') | Q(status = 'pv2') | Q(status = 'pv3'))
    for transaction in pending_verification_transactions:
        verification_tier = transaction.client.get_verification_tier()
        pre_transaction_verification_tier = transaction.pre_transaction_verification_tier
        if transaction.action == 'B':
            if verification_tier >= 1 and pre_transaction_verification_tier == 0:
                messages.send_bt0_to_bt1_verification_passed.delay(transaction.localbitcoins_contact_id)
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Send payment')
                transaction.status = 'pp'
                transaction.save()
            elif verification_tier >= 1 and pre_transaction_verification_tier > 0:
                telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Send payment')
                transaction.status = 'pp'
                transaction.save()
        elif transaction.action == 'S':
            total_volume = transaction.client.total_sell_volume()
            required_verification_tier = transaction.get_sell_required_verification_tier()
            if required_verification_tier == 1 and verification_tier == 1 and transaction.status == 'pv1':
                if pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st1_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
            elif required_verification_tier == 2 and verification_tier == 1 and transaction.status == 'pv1':
                if pre_transaction_verification_tier == 0 and transaction.amount_fiat >= transaction.get_st1_limit():
                    #intermediary message
                    messages.send_st0_to_st2_transaction_id_verification_passed.delay(transaction.localbitcoins_contact_id)
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                    transaction.status ='pv2'
                    transaction.save()
                elif pre_transaction_verification_tier == 0 and transaction.amount_fiat >= transaction.get_st0_and_st1_one_transaction_limit():
                    #intermediary message
                    messages.send_st0_to_st2_2K_transaction_id_verification_passed.delay(transaction.localbitcoins_contact_id)
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                    transaction.status ='pv2'
                    transaction.save()
            elif required_verification_tier == 2 and verification_tier == 2 and transaction.status == 'pv2':
                if pre_transaction_verification_tier == 0 and transaction.amount_fiat >= transaction.get_st0_and_st1_one_transaction_limit():
                    messages.send_st0_to_st2_2K_transaction_video_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st2_transaction_video_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 1 and transaction.amount_fiat >= transaction.get_st2_limit():
                    messages.send_st1_to_st2_2K_transaction_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 1 and transaction.amount_fiat >= transaction.get_st0_and_st1_one_transaction_limit():
                    messages.send_st1_to_st2_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(), transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
            elif required_verification_tier == 3 and verification_tier == 1 and transaction.status == 'pv1':
                #intermediary message
                if pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st3_transaction_id_verification_passed.delay(transaction.localbitcoins_contact_id)
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Complete T2 verification')
                    transaction.status ='pv2'
                    transaction.save()
            elif required_verification_tier == 3 and verification_tier == 2 and transaction.status == 'pv2':
                #intermediary message
                if pre_transaction_verification_tier == 0 :
                    messages.send_st0_to_st3_transaction_video_verification_passed.delay(transaction.localbitcoins_contact_id)
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Complete T3 verification')
                    transaction.status ='pv3'
                    transaction.save()
                if pre_transaction_verification_tier == 1:
                    messages.send_st1_to_st3_st3_verification_required.delay(transaction.localbitcoins_contact_id)
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Complete T3 verification')
                    transaction.status ='pv3'
                    transaction.save()
            elif required_verification_tier == 3 and verification_tier == 3 and transaction.status == 'pv3':
                if pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st3_transaction_proof_of_funds_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account() ,transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 1:
                    messages.send_st1_to_st3_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 2:
                    messages.send_st2_to_st3_verification_passed.delay(transaction.localbitcoins_contact_id, transaction.client.real_name , transaction.get_bank_account(),transaction.reference)
                    transaction.status ='pp'
                    transaction.save()
                elif pre_transaction_verification_tier == 3:
                    telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now once again T{verification_tier} verified', required_intervention = 'Double check and send them payment details.')
                    transaction.status ='pp'
                    transaction.save()
            
    buy_paid_transactions = Transaction.objects.filter(status = 'p', action = 'B')
    for transaction in buy_paid_transactions:
        verification_tier = transaction.client.get_verification_tier()
        pre_transaction_verification_tier = transaction.pre_transaction_verification_tier
        if pre_transaction_verification_tier == 0:
            transaction.status = 'pr'
            transaction.save()
            #telegram.send_manual_intervention_required_message.delay(platform = 'Localbitcoins', trade_action = transaction.action, username = transaction.client.localbitcoins_username, trade_id = transaction.localbitcoins_contact_id , update = f'User is now T{verification_tier} verified', required_intervention = 'Send payment')
            messages.send_bt0_to_bt1_payment_sent.delay(transaction.localbitcoins_contact_id)
        elif pre_transaction_verification_tier >=1:
            transaction.status = 'pr'
            transaction.save()
            messages.send_bt1_payment_sent_message.delay(transaction.localbitcoins_contact_id)

    released_transactions = Transaction.objects.filter(status = 'r') 
    for transaction in released_transactions:
        verification_tier = transaction.client.get_verification_tier()
        if transaction.action == 'B':
            pre_transaction_verification_tier = transaction.pre_transaction_verification_tier
            if pre_transaction_verification_tier == 0:
                messages.send_bt0_to_bt1_ending_message.delay(transaction.localbitcoins_contact_id)
                set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
            else:
                messages.send_bt1_ending_message.delay(transaction.localbitcoins_contact_id)
            set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
            transaction.status = 'f'
            transaction.save()
        if transaction.action == 'S':
            pre_transaction_verification_tier = transaction.pre_transaction_verification_tier
            if verification_tier == pre_transaction_verification_tier :
                messages.send_within_limits_ending_message.delay(transaction.localbitcoins_contact_id)
                set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
                transaction.status = 'f'
                transaction.save()
            elif verification_tier == 1:
                #if pre_transaction_verification_tier == 0:
                messages.send_st0_to_st1_ending_message.delay(transaction.localbitcoins_contact_id)
                set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
                transaction.status = 'f'
                transaction.save()
            elif verification_tier == 2:
                if pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st2_2K_transaction_ending_message.delay(transaction.localbitcoins_contact_id)
                    set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
                    transaction.status = 'f'
                    transaction.save()
                elif pre_transaction_verification_tier == 1 and transaction.amount_fiat > transaction.get_st0_and_st1_one_transaction_limit():
                    messages.send_st1_to_st2_2K_transaction_ending_message.delay(transaction.localbitcoins_contact_id)
                    transaction.status = 'f'
                    transaction.save()
                elif pre_transaction_verification_tier == 1:
                    messages.send_st1_to_st2_ending_message.delay(transaction.localbitcoins_contact_id)
                    transaction.status = 'f'
                    transaction.save()
            elif verification_tier == 3:
                if pre_transaction_verification_tier == 0:
                    messages.send_st0_to_st3_transaction_ending_message.delay(transaction.localbitcoins_contact_id)
                    set_as_trusted_with_feedback.delay(transaction.client.localbitcoins_username)
                    transaction.status = 'f'
                    transaction.save()
                elif pre_transaction_verification_tier == 1:
                    messages.send_st1_to_st3_ending_message.delay(transaction.localbitcoins_contact_id)
                    transaction.status = 'f'
                    transaction.save()
                elif pre_transaction_verification_tier == 2:
                    messages.send_st2_to_st3_ending_message.delay(transaction.localbitcoins_contact_id)
                    transaction.status = 'f'
                    transaction.save()

    



@task(name="localbitcoins_refresh_pending_and_disputed_transactions_statuses")
def refresh_pending_and_disputed_transactions_statuses():
    transactions = Transaction.objects.filter(~Q(status = 'c') & ~Q(status = 'f') & ~Q(status = 'r'))
    for transaction in transactions:
        try:
            contact = get_contact(transaction.localbitcoins_contact_id)
            transaction, transaction_created = update_or_create_transaction(contact,
            transaction.client,
            transaction.action,
            status = transaction.status, 
            bank_account = transaction.get_bank_account(),
            pre_transaction_verification_tier= transaction.pre_transaction_verification_tier
            )
        except:
            pass
#process_pending_transactions()
#refresh_pending_and_disputed_trades_statuses()
# process_sell_transaction(get_contact(61897548) )
# print('done')

#c = get_contact(60818618)
#print(c)
# notifications_endpoint = 'https://www.cryptostrat.co.uk/lbc/'
# body = {'contact_id': 61898451}
# body = json.dumps(body)
# x = requests.post(notifications_endpoint, data = body)
# print(x)
# print('hi')



### Fix this error
#[2020-06-18 21:53:32,833: ERROR/ForkPoolWorker-1] Task localbitcoins_refresh_pending_and_disputed_transactions_statuses[31bc1b59-ae4e-4d4a-a401-0e6ea1b2e8dc] raised unexpected: AttributeError("'NoneType' object has no attribute 'json'")
