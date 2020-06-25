from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .sumsub import process_notification
from .models import RawSumSubNotification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .sumsub import renew_verification_token
from .crypto import analyse_address, analyse_transaction
from datetime import datetime
from clients.models import Client
from django.utils import timezone
# Create your views here.

@csrf_exempt
def sumsub_applicant_created(request):
    if request.method == 'POST':
        process_notification(request)
        return HttpResponse(status=200, content='success')
    else:
        return render(request, 'front/home.html')
class NoritifcationsList(LoginRequiredMixin, ListView):
    model = RawSumSubNotification
    template_name = 'back/notification_list_sumsub.html'
    context_object_name = 'notifications'

def verification_page(request, identifier):
    try:
        uuid_part = ''
        client_identifier = ''
        for character in identifier[::-1]:
            if character == '_':
                uuid_part = uuid_part[::-1]
                client_identifier = identifier.rstrip(uuid_part).rstrip('_')
                break
            uuid_part += character
        if len(uuid_part) == 6:
            #different lengths depending on identifier
            client = Client.objects.get(localbitcoins_username = client_identifier)
        elif len(uuid_part) == 5:
            client = Client.objects.get(phone_number = client_identifier)
        if client.sumsub_sdk_access_token_expiry < timezone.now() or uuid_part not in str(client.uuid):
            raise ValueError('Token Expired')
        return render(request, 'front/sumsub_verification.html', {'external_id': client.sumsub_external_user_id, 'access_token_for_sdk': client.sumsub_sdk_access_token})
    except (Client.DoesNotExist, ValueError, TypeError):
        return render(request, 'front/sumsub_verification.html', {'external_id': None, 'access_token_for_sdk': None})


def test_verification_page(request, identifier):
    try:
        uuid_part = ''
        client_identifier = ''
        for character in identifier[::-1]:
            if character == '_':
                uuid_part = uuid_part[::-1]
                #for some reason .rstrip('_' + uuid_part) does not work
                client_identifier = identifier.rstrip(uuid_part).rstrip('_')
                break
            uuid_part += character
        if len(uuid_part) == 6:
            print(uuid_part)
            #different lengths depending on identifier
            client = Client.objects.get(localbitcoins_username = client_identifier)
        elif len(uuid_part) == 5:
            client = Client.objects.get(phone_number = client_identifier)
        if client.sumsub_sdk_access_token_expiry < timezone.now() or uuid_part not in str(client.uuid):
            raise ValueError('Token Expired')
        return render(request, 'front/sumsub_verification_test.html', {'external_id': client.sumsub_external_user_id, 'access_token_for_sdk': client.sumsub_sdk_access_token})
    except (Client.DoesNotExist, ValueError, TypeError, UnboundLocalError):
        return render(request, 'front/sumsub_verification_test.html', {'external_id': None, 'access_token_for_sdk': None})

@staff_member_required
def renew_verification_link_request(request):
    if request.method == 'POST':
        localbitcoins_username = request.POST.get('username').rstrip().lstrip()
        try:
            client = Client.objects.get(localbitcoins_username = localbitcoins_username)
            renew_verification_token(client)
            return render(request, 'back/renew_verification_link.html', {'username': localbitcoins_username, 'successful': True})
        except Client.DoesNotExist:
            return render(request, 'back/renew_verification_link.html', {'username': localbitcoins_username, 'successful': False})
        #return HttpResponse(status=200, content=f'New verification url for <b>{username}</b>: {verification_url}')
    if request.method == 'GET':
        return render(request, 'back/renew_verification_link.html')

@staff_member_required
def crypto_address_analysis(request):
    if request.method == 'GET':
        return render(request, 'back/crypto_address_analysis.html')
    elif request.method == 'POST':
        address = request.POST.get('address')
        base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        if not address:
            return render(request, 'back/crypto_address_analysis.html', {'error_message': 'Enter an address!'})
        for character in address:
            if character not in base58:
                return render(request, 'back/crypto_address_analysis.html', {'error_message': 'Invalid bitcoin address!'})
        address_analysis = analyse_address(address)
        if address_analysis.last_updated_global != None:
            address_analysis.last_updated_global = datetime.utcfromtimestamp(address_analysis.last_updated_global).strftime('%H:%M:%S %d-%m-%Y')
        if address_analysis.last_updated_fast != None:
            address_analysis.last_updated_fast = datetime.utcfromtimestamp(address_analysis.last_updated_fast).strftime('%H:%M:%S %d-%m-%Y')
        return render(request, 'back/crypto_address_analysis.html', {'analysis': address_analysis})

@staff_member_required
def crypto_transaction_analysis(request):
    if request.method == 'GET':
        return render(request, 'back/crypto_transaction_analysis.html')
    elif request.method == 'POST':
        txid = request.POST.get('txid')
        address = request.POST.get('address')
        if not txid or not address:
            return render(request,'back/crypto_transaction_analysis.html', {'error_message': 'You must provide both a TXID and an ADDRESS!'})
        base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        for character in address:
            if character not in base58:
                return render(request, 'back/crypto_transaction_analysis.html', {'error_message': 'Invalid bitcoin address!'})
        transaction_analysis = analyse_transaction(txid = txid, address = address)
        return render(request, 'back/crypto_transaction_analysis.html', {'analysis': transaction_analysis})