from django.shortcuts import render
from django.http import HttpResponse
from .update_prices import update_gbpbtc_price
from .models import ReferencePrice
# Create your views here.

def btcgbp_price_reference(request):
    price = ReferencePrice.objects.get(currency_pair = 'BTCGBP').price
    return HttpResponse(status=200, content=price)
# if request.method == 'POST':
#         process_notification(request)
#         return HttpResponse(status=200, content='success')
#     else:
#         return render(request, 'front/home.html')