import os

verification_url = 'https://www.cryptostrat.co.uk/verify/'
if (os.environ['DEBUG'] == 'True'):
    verification_url = 'https://csukdev.herokuapp.com/verify/test/'

def get_verification_url(client):
    uuid = str(client.uuid)
    if client.sumsub_external_user_id == None:
        return None
    elif client.localbitcoins_username:
        return f'{verification_url}{client.localbitcoins_username}_{uuid[:6]}'
    elif client.phone_number:
        return f'{verification_url}{client.phone_number}_{uuid[:5]}'
    else:
        return None