import requests
from celery import shared_task
import time
import os

telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
debug_notifications_group_id = -434122948
user_verified_group_id = -434122948
further_verification_required_group_id = -434122948
new_offer_group_id = -1001329478045
bank_payments_group_id = -428213526,
localbitcoins_payment_complete_group_id = -1001419326868
manual_intervention_required_group_id = -487511643
critical_error_group_id = -437694867

if (os.environ['DEBUG'] == 'True'):
    debug_notifications_group_id = -434122948
    user_verified_group_id = -434122948
    further_verification_required_group_id = -434122948
    new_offer_group_id = -1001329478045
    bank_payments_group_id = -428213526,
    localbitcoins_payment_complete_group_id = -1001419326868
    manual_intervention_required_group_id = -487511643
    critical_error_group_id = -437694867

def request(GET_POST, method, parameters= None):
    if GET_POST.upper() == 'GET':
        if parameters == None:
            data = requests.get(f'https://api.telegram.org/bot{telegram_bot_token}/{method}')
        else:
            data = requests.get(f'https://api.telegram.org/bot{telegram_bot_token}/{method}', params=parameters)
    elif GET_POST.upper() == 'POST':
        data = requests.post(url = f'https://api.telegram.org/bot{telegram_bot_token}/{method}', params=parameters)
    else:
        return(print('Unsupported requests method. It needs to be GET or POST'))
    if data.status_code == 200:
        return data
    else:
        print('Error encountered in telegram requests')
        print(parameters)
        print(data.content)
        time.sleep(2)
        return request(GET_POST, method, parameters)
    
    
class user:
    def __init__(self, 
                 user_id,
                 username
                ):
        self.id = user_id
        self.username = username
        
        
class command:
    def __init__(self, 
                 from_id,
                 from_username,
                 chat_id,
                 date,
                 instruction,
                 parameters
                ):
        self.from_id = from_id
        self.from_username = from_username
        self.chat_id = chat_id
        self.date = date
        self.instruction = instruction
        self.parameters = parameters
        
        
def get_commands(allowed_users, allowed_chats):
    updates = request('GET', 'getUpdates').json()
    if updates['ok'] == False:
        print('error getting telegram update')
        return get_updates()
    else:
        commands = []
        is_command = False
        updates = updates['result']
        last_update = None
        for update in updates:
            is_message = 'message' in update
            if is_message:
                message = update['message']
                try:
                    message_text = message['text']
                except KeyError:
                    last_update = update['update_id']
                    request('GET', 'getUpdates', {'offset': (last_update)+1}).json()
                    'breaking'
                    break
                is_command = message_text.startswith('/')
                if is_command:
                    text = message['text'][1:]
                    text = text.split(" ", 1)
                    instruction = text[0]
                    paramaters = None
                    if len(text) > 1:
                        paramaters = text[1]
                    command = command(message['from']['id'],
                                               message['from']['username'],
                                               message['chat']['id'],
                                               message['date'],
                                               text[0],
                                               paramaters
                                              )
                    #check allowed user usernames,id, and chat id.
                    user_allowed = is_user_allowed(command.from_id, command.from_username,allowed_users)
                    chat_allowed = is_chat_allowed(command.chat_id, allowed_chats)
                    if  user_allowed and chat_allowed:
                        commands.append(command)
            last_update = update['update_id']
        if last_update is not None:
            request('GET', 'getUpdates', {'offset': (last_update)+1}).json()
        return commands
    
    
def is_user_allowed(user_id, username, allowed_users):
    user_allowed = False
    for user in allowed_users:
        if user.username == username and user.id == user_id:
            user_allowed = True
    return user_allowed


def is_chat_allowed(chat_id, allowed_chats):
    chat_allowed = False
    for chat in allowed_chats:
        if chat_id == chat:
            chat_allowed = True
    return chat_allowed



def send_message(chat_id, text):
    #to adhere to htmlmarkdown text format
    text = text.replace("&", "&amp") #.replace("<", "&lt").replace(">", "&gt")
    request('POST', 'sendMessage', {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'})

def parameters_check_int(command):
    try:
        command.parameters = int(command.parameters)
    except ValueError:
        send_message(command.chat_id, 'Error! Invalid parameters')
        return None
    except TypeError:
        send_message(command.chat_id, 'Error! Parameters required')
        return None
    return command


def parameters_check_float(command):
    try:
        command.parameters = round(float(command.parameters),2)
    except ValueError:
        send_message(command.chat_id, 'Error! Invalid parameters')
        return None
    except TypeError:
        send_message(command.chat_id, 'Error! Parameters required')
        return None
    return command

#updates = request('GET', 'getUpdates', None).json()
#send_message(debug_notifications_group_id, 'test1')
@shared_task
def send_debug_message(text):
    send_message(debug_notifications_group_id, text)
@shared_task
def send_user_verified_message(text):
    send_message(user_verified_group_id, text)
@shared_task
def send_further_verifications_message(text):
    send_message(further_verification_required_group_id , text)

@shared_task
def send_new_offer_message(text):
    send_message(new_offer_group_id , text)

@shared_task
def send_new_payment_message(text):
    send_message(bank_payments_group_id, text)

@shared_task
def send_localbitcoins_payment_complete_message(text):
    send_message(localbitcoins_payment_complete_group_id, text)

@shared_task
def send_manual_intervention_required_message(platform, trade_action, username, trade_id, update, required_intervention):
    if trade_action == 'S':
        trade_action = 'Sell'
    elif trade_action == 'B':
        trade_action = 'Buy'
    text = (f'<b>{platform} ({trade_action} | {username} | {trade_id})</b>\n{update} \n{required_intervention}')
    send_message(manual_intervention_required_group_id, text)
@shared_task
def send_sumsub_manual_intervention_required_message(text):
    send_message(manual_intervention_required_group_id, text)
@shared_task
def send_general_manual_intervention_required_message(text):
    send_message(manual_intervention_required_group_id, text)
@shared_task
def send_critical_error_message(text):
    send_message(critical_error_group_id, text)

#to get new chat ids
# data = request('GET', 'getUpdates')
# print(data.json())