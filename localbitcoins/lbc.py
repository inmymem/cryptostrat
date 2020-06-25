import os
from .lbcapi import api
import time
import telegram.bot as telegram
from celery import shared_task

hmac_key = os.environ.get('LBC_HMAC_KEY')
hmac_secret = os.environ.get('LBC_HMAC_SECRET')
broker_account_name = os.environ.get('LBC_ACCOUNT_USERNAME')
conn = api.hmac(hmac_key, hmac_secret)

class notification:
    def __init__(self, url, created_at, contact_id, read, message, notification_id):
        self.url = url
        self.created_at = created_at
        self.contact_id = contact_id
        self.read = read
        self.message = message
        self.notification_id = notification_id
        self.type = self.notification_type()
    def notification_type(self):
        if 'You have recently traded with' in self.message:
            return 'feedback_request'
        if 'You have a new offer' in self.message:
            return 'new_offer'
        if 'new message from' in self.message:
            return 'new_message'
        if 'payment marked complete' in self.message:
            return 'payment_complete'
        if 'new admin message' in self.message:
            return 'admin_message'
        if 'Action required with' in self.message:
            return 'action_required'
#############add add type (buy or sell)
class account:
    def __init__(self, 
                 username,
                 created_at,
                 identity_verified_at,
                 trading_partners_count,
                 confirmed_trade_count_text,
                 trade_volume_text,
                 trusted_count,
                 blocked_count,
                 has_feedback,
                 feedback_score,
                 feedback_count,
                 has_common_trades,
                 my_feedback,
                 real_name_verifications_trusted,
                 real_name_verifications_untrusted,
                 real_name_verifications_rejected
                ):
        self.username = username
        self.created_at = created_at
        self.identity_verified_at = identity_verified_at
        self.trading_partners_count = trading_partners_count
        self.confirmed_trade_count_text = confirmed_trade_count_text
        self.trade_volume_text = trade_volume_text
        self.trusted_count = trusted_count
        self.blocked_count = blocked_count
        self.has_feedback = has_feedback
        self.feedback_score = feedback_score
        self.feedback_count = feedback_count
        self.has_common_trades = has_common_trades
        self.my_feedback = my_feedback
        self.real_name_verifications_trusted = real_name_verifications_trusted
        self.real_name_verifications_untrusted = real_name_verifications_untrusted
        self.real_name_verifications_rejected = real_name_verifications_rejected
    def id_verified_days(self):
        if self.identity_verified_at != None:
            verified_on = datetime.datetime.strptime(self.identity_verified_at, '%Y-%m-%dT%H:%M:%S+00:00')
            current_time = datetime.datetime.utcnow()
            days_since = (current_time - verified_on).days
            return days_since
        elif self.identity_verified_at == None:
            return 0
class contact:
    def __init__(self, 
                 payment_method,
                 advertiser_username,
                 trade_type,
                 advertisement_id,
                 is_buying,
                 is_selling,
                 payment_completed_at,
                 released_at,
                 created_at,
                 reference_code,
                 bank_account,
                 contact_id,
                 currency,
                 amount,
                 amount_btc,
                 client,
                 broker_account_username
                ):
        self.payment_method = payment_method
        self.advertiser_username = advertiser_username
        self.trade_type = trade_type
        self.advertisement_id = advertisement_id
        self.is_buying = is_buying
        self.is_selling = is_selling
        self.payment_completed_at = payment_completed_at
        self.released_at = released_at
        self.created_at = created_at
        self.reference_code = reference_code
        self.bank_account = bank_account
        self.contact_id = contact_id
        self.currency = currency
        self.amount = amount
        self.amount_btc = amount_btc
        self.client = client
        self.broker_account_username = broker_account_username
class client:
    def __init__(self,
                 username,
                 feedback_score,
                 trade_count,
                 countrycode_by_ip,
                 countrycode_by_phone_number,
                 real_name,
                 company_name,
                ):
        self.username = username
        self.feedback_score = feedback_score
        self.trade_count = trade_count
        self.countrycode_by_ip = countrycode_by_ip
        self.countrycode_by_phone_number = countrycode_by_phone_number
        self.real_name = real_name
        self.company_name = company_name

def conn_call(GET_POST, method, parameters, object_id, debug_message_sent = False):
    if object_id == None and parameters == None:
        data = conn.call(GET_POST, f'/api/{method}/')
    elif object_id != None and parameters == None:
        data = conn.call(GET_POST, f'/api/{method}/{object_id}/')
    elif object_id == None and parameters != None:
        data = conn.call(GET_POST, f'/api/{method}/', params = parameters)
    else:
        data = conn.call(GET_POST, f'/api/{method}/{object_id}/', params = parameters)
    if data.status_code == 200:
        return data
    elif data.status_code == 400:
        error = data.content.decode()
        try:
            debug_message = f'LBC:: error {error} \nmethod: {method} \nparameters: {parameters} \nobject id: {object_id}'
            telegram.send_debug_message(debug_message)
            time.sleep(6)
            #return conn_call(GET_POST, method, parameters, object_id, debug_message_sent)
        except:
            debug_message = f'LBC:: error (unable to send error content) \nmethod: {method} \nparameters: {parameters} \nobject id: {object_id}'
            telegram.send_debug_message(debug_message)
            time.sleep(6)
            #return conn_call(GET_POST, method, parameters, object_id, debug_message_sent)
        return 
    else:
        print('\n\n\n\nError encountered in localbitcoins requests. Retrying in 2 seconds!!!!!!')
        time.sleep(6)
        if debug_message_sent == False:
            error = data.content.decode()
            if 'maintenance' in error.lower():
                error = 'LBC is in maintenance mode. Please check!'
            elif 'service temporarily unavailable' in error.lower():
                error= 'LBC service temporarily unavailable. Please check if persists!'
            debug_message = f'LBC: error {error} \nmethod: {method} \nparameters: {parameters} \nobject id: {object_id}'
            telegram.send_debug_message(debug_message)
            debug_message_sent = True
        if method != 'notifications':
            return conn_call(GET_POST, method, parameters, object_id, debug_message_sent)
def get_account(contact):
    username = contact.client.username
    account = conn_call('GET', f'account_info/{username}', None, None).json()['data']
    my_feedback = None
    if account['has_common_trades'] == True:
        my_feedback = account['my_feedback']
    user_account = account(account['username'],
                               account['created_at'],
                               account['identity_verified_at'],
                               account['trading_partners_count'],
                               account['confirmed_trade_count_text'],
                               account['trade_volume_text'],
                               account['trusted_count'],
                               account['blocked_count'],
                               account['has_feedback'],
                               account['feedback_score'],
                               account['feedback_count'],
                               account['has_common_trades'],
                               my_feedback,
                               account['real_name_verifications_trusted'],
                               account['real_name_verifications_untrusted'],
                               account['real_name_verifications_rejected'],
                              )
    return user_account
def get_contact(contact_id):
    contact = conn_call('GET', 'contact_info', None, contact_id).json()['data']
    return contact
def get_pagination_params(data):
    next_params = None
    prev_params = None
    if 'next' in data.json()['pagination']:
        next_p = data.json()['pagination']['next']
        parsed = urlparse(next_p)
        next_params = parse_qs(parsed.query)
    if 'prev' in data.json()['pagination']:
        prev_p = data.json()['pagination']['prev']
        parsed = urlparse(prev_p)
        prev_params = parse_qs(parsed.query)
    return {'next': next_params, 'prev': prev_params}
def process_contact(contact):
    client_username = None
    broker_account_username = None
    bank_account_details = None
    if contact['is_buying'] == True:
        client = client(contact['seller']['username'],
                  contact['seller']['feedback_score'],
                  contact['seller']['trade_count'],
                  None,
                  None,
                  None,
                  None
                 )
        broker_account_username = contact['buyer']['username']
        if contact['buyer']['username'] ==  contact['advertisement']['advertiser']['username']:
            bank_account_details =  bank_account(contact['account_details']['receiver_name'], 
                                                 contact['account_details']['account_number'],
                                                 contact['account_details']['sort_code'],
                                                 contact['account_details']['reference']),
        else: 
            bank_account_details = None
    else:
        client = client(contact['buyer']['username'],
                  contact['buyer']['feedback_score'],
                  contact['buyer']['trade_count'],
                  contact['buyer']['countrycode_by_ip'],
                  contact['buyer']['countrycode_by_phone_number'],
                  contact['buyer']['real_name'],
                  contact['buyer']['company_name']
                 )
        broker_account_username = contact['seller']['username']
    lbc_contact = contact(contact['advertisement']['payment_method'],
                              contact['advertisement']['advertiser']['username'],
                              contact['advertisement']['trade_type'],
                              contact['advertisement']['id'],
                              contact['is_buying'],
                              contact['is_selling'],
                              contact['payment_completed_at'],
                              contact['released_at'],
                              contact['created_at'],
                              contact['reference_code'],
                              bank_account_details,
                              contact['contact_id'],
                              contact['currency'],
                              contact['amount'],
                              contact['amount_btc'],
                              client,
                              broker_account_username
                             )
    return lbc_contact

def mark_notification_as_read(notification_id):
    conn_call('POST', 'notifications/mark_as_read' , None, notification_id)

def get_messages(contact_id):
    messages = conn_call('GET', 'contact_messages', None, contact_id).json()['data']['message_list']
    return messages
@shared_task
def send_message(contact_id, message):
    conn_call('POST', 'contact_message_post', {'msg':message}, contact_id)
@shared_task
def set_as_trusted(username):
    conn_call('POST', 'feedback', {'feedback': 'trust'}, username)
@shared_task
def set_as_trusted_with_feedback(username):
    #to seperate functions to not allow for others to track when you last traded with someone
    conn_call('POST', 'feedback', {'feedback': 'trust', 'msg': 'Verified and trusted by Cryptostrat.co.uk'}, username)

def contact_to_general_trade(lbc_contact):
    sell_bank_account = None
    buy_bank_account = None
    if lbc_contact.is_buying == True and lbc_contact.broker_account_username == lbc_contact.advertiser_username:
        buy_bank_account = lbc_contact.bank_account
    if lbc_contact.is_selling == True and lbc_contact.broker_account_username == lbc_contact.advertiser_username:
        sell_bank_account = get_sell_bank_account(lbc_contact.contact_id)
    trade_t = trade(lbc_contact.broker_account_username,
                    lbc_contact.trade_type,
                    lbc_contact.is_buying,
                    lbc_contact.is_selling,
                    lbc_contact.amount,
                    lbc_contact.amount_btc,
                    'LBC',
                    lbc_contact.client,
                    lbc_contact.reference_code,
                    lbc_contact.contact_id,
                    lbc_contact.released_at,
                    sell_bank_account,
                    buy_bank_account
                   )
    return trade_t
def client_to_general_client(lbc_client, client_in, trade):
    if client_in == None:
        sell_accounts = []
        buy_accounts = []
        trades = []
        trades.append(trade)
        sell_accounts.append(trade.sell_bank_account)
        buy_accounts.append(trade.buy_bank_account)
        client_t = client(lbc_client.username,
                          lbc_client.real_name,
                          lbc_client.company_name,
                          False,
                          trades,
                          False,
                          False,
                          False,
                          sell_accounts,
                          buy_accounts
                         )
    else:
        sell_accounts = client_in.sell_bank_accounts
        buy_accounts = client_in.buy_bank_accounts
        trades = client_in.trades
        trades.append(trade)
        sell_account_found = False
        buy_account_found = False
        for sell_account in sell_accounts:
            if trade.sell_bank_account == sell_account:
                sell_account_found = True
        for buy_account in buy_accounts:
            if trade.buy_bank_account == buy_account:
                buy_account_found = True
        if sell_account_found == False:
            sell_accounts.append(trade.sell_bank_account)
        if buy_account_found == False:    
            buy_accounts.append(trade.buy_bank_account)    
        client_t = client(client_in.username,
                          client_in.real_name,
                          client_in.company_name,
                          client_in.company_verification,
                          trades,
                          client_in.picture_verification,
                          client_in.video_verification,
                          client_in.source_of_funds,
                          sell_accounts,
                          buy_accounts
                         )
    return client_t
def get_sell_bank_account(contact_id):
    print(contact_id)
    account_used = None
    messages = get_messages(contact_id)
    for comm in messages:
        message = comm['msg']
        if '38QDUifdZU64t6L1AcEwx5dAFBxkxLUzX4'  in message:
            print('38QDUifdZU64t6L1AcEwx5dAFBxkxLUzX4',contact_id)
        if '36770955' in message:
            account_used = Iota_santander
            #break
        if '38654868' in message:
            account_used = M5Jewellery_lloyds
            #break
        if '93133443' in message:
            account_used = M5Watches_barclays
            #break
    return account_used


def is_send_details(contact):
    if float(contact.amount) >= 4000:
        return False
    client_account = get_account(contact)
    days_since_verified = client_account.id_verified_days()
    if days_since_verified < 150:
        return False
    text = f'Account verified {days_since_verified} days ago'
    telegram.send_message(telegram_lbc_new_offer_group, text)