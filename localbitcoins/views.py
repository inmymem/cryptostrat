from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from . import lbc_process
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def new_contact(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode())
        contact_id = body['contact_id']
        lbc_process.process_new_contact(contact_id)
        return HttpResponse(status=200, content=contact_id)


    if request.method == 'GET':
        #after debugging disabled leave it to show page not found
        return redirect('home')

# def verification_page(request, username, access_token_for_sdk):
#     return render(request, 'front/sumsub_verification.html', {'username': username, 'access_token_for_sdk':access_token_for_sdk})

# def verification_page_lbc(request, lbc_username):
#     client = Client.objects.get(localbitcoins_username = lbc_username)
#     print(client.sumsub_sdk_access_token)
#     return render(request, 'front/sumsub_verification.html', {'username': client.uuid, 'access_token_for_sdk': client.sumsub_sdk_access_token})