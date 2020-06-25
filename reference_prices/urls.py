from django.urls import path
from . import views

urlpatterns = [
    path('gbp', views.btcgbp_price_reference, name='gbp')
]