from django.urls import path
from . import views
urlpatterns = [
    path('nparser', views.sumsub_applicant_created, name='sumsub_create'),
    path('notifications/', views.NoritifcationsList.as_view(), name='sumsub_notifications'),
    path('request_link/', views.renew_verification_link_request, name='renew_verification_link_request_page'),
    path('crypto_address/', views.crypto_address_analysis, name = 'crypto_address_analysis_page'),
    path('crypto_transaction/', views.crypto_transaction_analysis, name = 'crypto_transaction_analysis_page'),
    path('<str:identifier>/', views.verification_page, name= 'verification_page'),
    path('test/<str:identifier>/', views.test_verification_page, name= 'test_verification_page'),
]