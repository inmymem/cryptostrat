from django.urls import path
from .views import notification_parser, NotificationList, TransactionList, SendTransaction
from . import views
urlpatterns = [
    path('nparser', notification_parser, name='notification_parser'),
    path('notifications/', NotificationList.as_view(), name='notification_list'),
    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('transactionss/', views.transaction_list_with_balance, name='transaction_list_with_balance'),
    path('send/', SendTransaction.as_view(), name='send_transaction'),

]