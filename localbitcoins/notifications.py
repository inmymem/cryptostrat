from .lbcapi import api
from . import lbc
import requests
import json
from celery.decorators import task
import telegram.bot as telegram
import os
from celery import shared_task
import time
from .lbc import conn_call, get_messages
from .lbc_process import mark_transaction_as_paid


notifications_endpoint = 'https://cryptostrat.herokuapp.com/lbc/'

if (os.environ['DEBUG'] == 'True'):
    if os.environ['LOCAL'] == 'True':
        notifications_endpoint = 'http://127.0.0.1:8000/lbc/'
    else:
        notifications_endpoint = 'https://csukdev.herokuapp.com/lbc/'


hmac_key = os.environ.get('LBC_HMAC_KEY')
hmac_secret = os.environ.get('LBC_HMAC_SECRET')


def get_notifications():
    notifications = conn_call('GET', 'notifications', None, None).json()['data']
    notifications_as_class = []
    for notif in notifications:
        try:
            contact_id = notif['contact_id']
        except KeyError:
            contact_id = None
        notifications_as_class.append(lbc.notification(notif['url'], 
                                                       notif['created_at'], 
                                                       contact_id, 
                                                       notif['read'], 
                                                       notif['msg'],
                                                       notif['id']))
    return notifications_as_class

# def locally_mark_feedback_notifications(lbc_notifications): #when a trade is released manually, the feedback_request notification gets read instantly so this function is needed to change the status of those trades for whom the feedback has not been sent yet. Can remove it when trades are automated.
#     for notif in lbc_notifications:
#         if notif.type == 'feedback_request':
#             notification_time = datetime.datetime.strptime(notif.created_at,  "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
#             current_time = datetime.datetime.utcnow()
#             seconds_since = (current_time - notification_time).seconds
#             if seconds_since < 45:
#                 feedback_sent = False
#                 print('checking message', notif.type, seconds_since)
#                 messages = get_messages(notif.contact_id)
#                 for msg in messages:
#                     msg = msg['msg']
#                     if 'is released and should be in your wallet' in msg:
#                         feedback_sent = True
#                 notif.read = feedback_sent
#     return lbc_notifications

def get_unread_notifications(notifications):
    unread_notifications = []
    for notif in notifications:
        if notif.read == False:
            unread_notifications.append(notif)
    return unread_notifications

#model where we send to endpoint and model where we call function from lbc_process
def process_unread_notifications(unread_notifications):
    for notif in unread_notifications:
        if notif.type == 'new_offer':
            body = {'contact_id': notif.contact_id}
            body = json.dumps(body)
            requests.post(notifications_endpoint, data = body)
            mark_notification_as_read.delay(notif.notification_id)
            #process_new_offer(notif)
        if notif.type == 'payment_complete':
            mark_notification_as_read.delay(notif.notification_id)
            mark_transaction_as_paid(notif.contact_id)
        #if notif.type == 'new_message':
            #get_messages(notif.contact_id)
            
            #unprocessed_contact = get_contact(notif.contact_id)
            #contact = process_contact(unprocessed_contact)
            #text = f'{broker_account} - Payment marked complete #{notif.contact_id} ({contact.amount} {contact.currency} by {contact.client.username})'
            #telegram.send_message(telegram_lbc_payment_complete_group, text)
            #mark_notification_as_read(notif.notification_id) #### if you cover all types put in outer loop
        #if notif.type == 'feedback_request':
            #unprocessed_contact = get_contact(notif.contact_id)
            #contact = process_contact(unprocessed_contact)
            #username = contact.client.username
            #if contact.is_selling == True and client.advertiser_username == client.broker_account_username:
            #    trade_type = 'sell'
            #client_profile = find_client(username, clients_database)
            #if client_profile == None:
            #    num_of_trades = 0
            #else:
            #    num_of_trades = client_profile.get_number_of_trades()
            #print(num_of_trades)
            #if trade_type == 'sell':
            #    if num_of_trades < 2:
            #        send_message(notif.contact_id, messages().released_new)
            #        send_message(notif.contact_id, messages().post_release_new)
            #    if num_of_trades >= 2:
            #        send_message(notif.contact_id, messages().released_regular)
            #        send_message(notif.contact_id, messages().post_release_regular)
            #    print('number of trades = ', num_of_trades)
            
def process_new_offer(notif):
    body = {'contact_id': notif.contact_id}
    body = json.dumps(body)
    requests.post(notifications_endpoint, data = body)
    mark_notification_as_read(notif.notification_id)
    #unprocessed_contact = get_contact(notif.contact_id)
    #print(unprocessed_contact)
    #contact = process_contact(unprocessed_contact)
    #is_send_details = send_details(contact)
    #text = f'{broker_account} - New offer #{notif.contact_id} ({contact.amount} {contact.currency} by {contact.client.username})'
    #telegram.send_message(telegram_lbc_new_offer_group, text)
     #### if you cover all types put in outer loop
def get_contact(contact_id):
    contact = conn_call('GET', 'contact_info', None, contact_id).json()['data']
    return contact

@shared_task
def mark_notification_as_read(notification_id):
    conn_call('POST', 'notifications/mark_as_read' , None, notification_id)



def update_notifications():
    lbc_notifications = get_notifications()
    #lbc_notifications = locally_mark_feedback_notifications(lbc_notifications)  #needed for feedback, find a better mechanism
    unread_notifications = get_unread_notifications(lbc_notifications)
    process_unread_notifications(unread_notifications)
