from django.urls import path
from . import views
urlpatterns = [
    path('', views.new_contact, name= 'new_contact'),
    #path('verify/<str:username>/<str:access_token_for_sdk>/', views.verification_page, name= 'verification_page'),
    #path('verify/lbc/<str:lbc_username>/', views.verification_page_lbc, name= 'localbitcoins_verification_page'),

]