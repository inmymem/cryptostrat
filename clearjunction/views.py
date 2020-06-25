from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .clearjunction import process_notification, get_balance, send_FPS
from django.views.generic import ListView, CreateView, FormView
from .models import CJ_notification, Fiat_transaction
from .forms import SendFPS
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def notification_parser(request):
    if request.method == 'POST':

        return process_notification(request)
    else:
        return render(request, 'front/home.html')

class NotificationList(LoginRequiredMixin, ListView):
    model = CJ_notification
    template_name = 'back/notification_list.html'
    context_object_name = 'notifications'
    ordering = ['-pk']

class TransactionList(LoginRequiredMixin, ListView):
    model = Fiat_transaction
    template_name = 'back/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-pk']
    #paginate_by = 10

class SendTransaction(LoginRequiredMixin, FormView):
    template_name = 'back/send_transaction.html'
    form_class = SendFPS
    
    #once a valid form has been posted, verify that it goes through
    def form_valid(self, form):
        transaction_data = form.cleaned_data
        message = send_FPS(transaction_data)
        return HttpResponse(f'<h4>{message} </h4>')
    
    
@login_required
def transaction_list_with_balance(request):
    #if not request.user.is_authenticated:
        #return redirect('home')
    transactions = Fiat_transaction.objects.all()
    balances = get_balance()
    return render(request, 'back/transaction_list.html', {'transactions': transactions, 'balances': balances})