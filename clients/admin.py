from django.contrib import admin
from .models import Client, Transaction
from django.http import HttpResponseRedirect
from django.utils import timezone
from verifications.sumsub import set_up_verification_credentials, renew_verification_token
from verifications.verification_links import get_verification_url
from django import forms
from .forms import ClientAddForm, ClientChangeForm, TransactionLBCChangeForm
# Register your models here.

class TransactionInline(admin.TabularInline):
    model = Transaction
    fields = ('platform', 'action', 'reference', 'localbitcoins_contact_id', 'amount_fiat', 'amount_btc', 'fee_btc', 'exchange_price', 'status')
    readonly_fields = ('platform', 'action', 'reference','localbitcoins_contact_id', 'action', 'amount_fiat', 'amount_btc', 'fee_btc', 'exchange_price')
    # localbitcoins_contact_id = models.IntegerField(unique=True, editable = False, null = True)
    # btc_txid = models.CharField(max_length = 64, editable= False, null= True, blank= True)
    # btc_address = models.CharField(max_length = 64, editable = True, null= True, blank= True)
    # status = models.CharField(choices = ( ('i', 'Initialized'),('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pv1', 'Pending Verification - T1'), ('pv2', 'Pending Verification - T2'), ('pv3', 'Pending Verification - T3'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')), default='i', max_length=3 ) #finalzed means message sent
    # created_at = models.DateTimeField(null=True, blank=True)
    # payment_completed_at = models.DateTimeField(null=True, blank=True)
    # closed_at = models.DateTimeField(null=True, blank=True)
    # pre_transaction_verification_tier = models.IntegerField(editable = False, default = 0)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    
    list_display = ('real_name', 'lbc_username', 'phone_number', 'total_sell_volume','total_buy_volume','name_match_checked', 'id_verified', 'liveness_verified', 'address_verified', 'video_verified', 'source_of_funds_verified', 'uuid')
    # inlines = [TransactionInline,]
    search_fields = ('real_name', 'localbitcoins_username')
    list_filter = ('id_verified',)
    list_editable = ()
    list_display_links = ('real_name', 'lbc_username', 'phone_number')
    change_form_template = 'admin/custom_change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return ClientAddForm
        else:
            form = ClientChangeForm
            #reset disabled fields as they get saved for every rquest and can cause issues
            for field in form.base_fields:
                form.base_fields[field].disabled = False
            disabled_fields = ()
            if obj.company_name: # editing an existing object
                disabled_fields += ('company_name',)
            if obj.email: # editing an existing object
                disabled_fields += ('email',)
            if obj.phone_number: # editing an existing object
                disabled_fields += ('phone_number',)
            if obj.telegram_username: # editing an existing object
                disabled_fields += ('telegram_username',)
            if obj.localbitcoins_username: # editing an existing object
                disabled_fields += ('localbitcoins_username',)
            for field in disabled_fields:
                form.base_fields[field].disabled = True
            # if not request.user.is_superuser:
            # if the need every arises to have superuser able to modify those fields use this; add them to the form, and delete them from readonly
            #     disabled_fields += (
            #         'real_name'
            #     )
            return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (TransactionInline,)
        self.readonly_fields = (
            'uuid', 
            'real_name', 
            'total_buy_volume', 
            'total_sell_volume', 
            'sumsub_verification_link', 
            'sumsub_token_active',
            'id_verified',
            'liveness_verified',
            'address_verified',
            'localbitcoins_real_name',
            'localbitcoins_feedback_score',
            'localbitcoins_trade_count',
            'localbitcoins_country_code_phone_number',
            'localbitcoins_last_country_code_ip',
            'sumsub_external_user_id',
            'sumsub_sdk_access_token',
            'sumsub_sdk_access_token_expiry',
            )
        self.fieldsets = (
            ('Profile', {
                'fields': (
                    ('real_name', 'company_name'),
                    ('email', 'phone_number', 'telegram_username'),
                    ('id_verified', 'liveness_verified', 'address_verified',),
                    ('name_match_checked', 'video_verified', 'source_of_funds_verified',),
                    'source_of_funds_limit',
                    ('total_buy_volume', 'total_sell_volume',)
                    ),
                'classes': ('extrapretty'),
            }),
            ('Localbitcoins', {
                'fields': (
                    'localbitcoins_username',
                    'localbitcoins_real_name', 
                    'localbitcoins_feedback_score', 
                    'localbitcoins_trade_count', 
                    'localbitcoins_country_code_phone_number', 
                    'localbitcoins_last_country_code_ip',
                    ),
                'classes': ('wide', 'extrapretty'),
                'description': 'LBC Profile'
            }),
            ('SumSub', {
                'fields': (
                    ('sumsub_external_user_id', 'sumsub_sdk_access_token'),
                    'sumsub_sdk_access_token_expiry',
                    ('sumsub_verification_link','sumsub_token_active',)
                    ),
                'classes': ('collapse', 'extrapretty'),
            }),
        )
        return super().change_view(request, object_id, form_url)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = ()
        self.readonly_fields = ()
        self.fieldsets = (
            ('Personal Information', {
                'fields': (
                    ('phone_number', 'email', 'company_name',),
                    ( 'telegram_username',),
                    ),
            }),
            ('Localbitcoins', {
                'fields': (
                    'localbitcoins_username',
                )
            })
        )
        return super().add_view(request, form_url = '')

    def response_change(self, request, obj):
        if 'renew_verification_token' in request.POST:
            renewed = renew_verification_token(obj)
            if renewed == True:
                self.message_user(request, "Successfully renewed the verification link.")
            else:
                self.message_user(request, "Failed to renew the verification link.")
            return HttpResponseRedirect(".")
        if 'create_application' in request.POST:
            set_up_verification_credentials(obj)
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('platform', 'action', 'client', 'amount_fiat', 'reference', 'status')
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return ClientAddForm
        else:
            if obj.platform == 'LBC':
                return TransactionLBCChangeForm
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        else:
            if obj.platform == 'LBC':
                readonly_fields = (
                    'platform',
                    'action',
                    'client',
                    'reference',
                    'amount_fiat',
                    'amount_btc',
                    'fee_btc',
                    'exchange_price',
                    'margin',
                    'profit',
                    'bank_account_name',
                    'bank_account_number',
                    'bank_account_sort_code',
                    'localbitcoins_contact_id',
                    'status',
                    'created_at',
                    'payment_completed_at',
                    'closed_at',
                    'pre_transaction_verification_tier'
                    )
            return self.readonly_fields + readonly_fields

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return ()
        else:
            if obj.platform == 'LBC':
                fieldsets = (
                    ('General Info', {
                        'fields': (
                            ('platform',),
                            ('action',),
                            ('client', 'reference'),
                            ('reference', 'localbitcoins_contact_id'),
                            ('amount_fiat', 'amount_btc', 'fee_btc',),
                            ('exchange_price', 'margin', 'profit',),
                        ),
                    }),
                    ('Status Details', {
                        'fields': (
                            ('status',),
                            ('created_at',),
                            ('payment_completed_at',),
                            ('closed_at',),
                        ),
                    }),
                    ('Cryptostrat Bank Account Details', {
                        'fields': (
                            ('bank_account_name', 'bank_account_number', 'bank_account_sort_code')
                        ),
                        'classes': ('collapse',)
                    }),
                    ('Client Bank Account Details', {
                        'fields': (
                            ('client_bank_account_name', 'client_bank_account_number', 'client_bank_account_sort_code')
                        ),
                        'classes': ('collapse in',)
                    }),
                )
                return self.fieldsets + fieldsets
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url)
    # list_filter = ('action', 'platform', 'status',)
    # readonly_fields = ('platform',)
    # autocomplete_fields = ('client',)
    # #ignore below as better to validate upon save
    # # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    # #     if db_field.name == "client":
    # #         kwargs["queryset"] = Client.objects.filter(id_verified = True)
    # #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    # def get_form(self, request, obj= None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     #form.base_fields['client']= forms.ModelChoiceField(queryset=Client.objects.all())
    #     disabled_fields = (
    #         'reference',
    #     )
    #     for field in disabled_fields:
    #         form.base_fields[field].disabled = True
    #     return form
    # None

    # #fieldsets = (
    #     ('Transaction Details', {
    #         'fields': (
    #             'reference',
    #             'amount_fiat'
    #         )

    #     }),
    # )

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'real_name', 'trade_count', 'total_sell_volume','total_buy_volume','name_match_checked', 'id_verified', 'liveness_verified', 'address_verified', 'video_verified', 'source_of_funds_verified')
#     inlines = [TransactionInline,]
#     readonly_fields = ('total_sell_volume','total_buy_volume',)
#     #readonly_fields
#     def get_form(self, request, obj= None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             disabled_fields = ['id_verified', 'liveness_verified', 'address_verified', 'feedback_score', 'trade_count', 'country_code_phone_number', 'last_country_code_ip']
#             for field in disabled_fields:
#                 form.base_fields[field].disabled = True
#         return form