from django.contrib import admin
from django.forms import ModelForm
from .models import User, Transaction
# Register your models here.

class TransactionInline(admin.TabularInline):
    model = Transaction
    fields = ('user','contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc', 'status', 'reference')
    readonly_fields = ('user','contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'real_name', 'trade_count', 'total_sell_volume','total_buy_volume','name_match_checked', 'id_verified', 'liveness_verified', 'address_verified', 'video_verified', 'source_of_funds_verified')
    inlines = [TransactionInline,]
    readonly_fields = ('total_sell_volume','total_buy_volume',)
    #readonly_fields
    def get_form(self, request, obj= None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            disabled_fields = ['id_verified', 'liveness_verified', 'address_verified', 'feedback_score', 'trade_count', 'country_code_phone_number', 'last_country_code_ip']
            for field in disabled_fields:
                form.base_fields[field].disabled = True
        return form

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ('user','contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc', 'status', 'reference')
    list_display = ('user','contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc', 'status', 'reference')
    readonly_fields = ('user','contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc')

