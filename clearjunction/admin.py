from django.contrib import admin
from .models import Fiat_transaction
# Register your models here.

@admin.register(Fiat_transaction)
class Fiat_transactionAdmin(admin.ModelAdmin):
    #date_hierarchy = 'timestamp' can't use since you set it as a charfield. Will have to investigate if it is possible to change to datefield later
    list_display = ('transactionType','name', 'sortCode', 'iban', 'accountNumber', 'operationAmount', 'currency', 'returned', 'operStatus', 'complianceStatus', 'release')
    
#admin.site.register(Fiat_transaction,Fiat_transactionAdmin)