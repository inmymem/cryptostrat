from django.forms import ModelForm, ValidationError
from clients.models import Client, Transaction
from verifications.sumsub import set_up_verification_credentials

class ClientAddForm(ModelForm):
    class Meta:
        model = Client
        fields = (
            'company_name',
            'localbitcoins_username',
            'email',
            'phone_number', 
            'telegram_username',
            )
    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Must have at least one identifier filled
    #     localbitcoins_username = cleaned_data.get('localbitcoins_username')
    #     if localbitcoins_username == None:
    #         raise ValidationError('Fill at least one field.')
    def save(self, commit = True): 
        client = super().save(commit = False)
        client.save()
        set_up_verification_credentials(client) 
        # if client.sumsub_sdk_access_token == None:
        #     raise ValidationError('Unable to create sumsub profile')
        return client

class ClientChangeForm(ModelForm):
    class Meta:
        model = Client
        fields = (
            #'real_name',
            'company_name',
            'email',
            'phone_number',
            'telegram_username',
            'localbitcoins_username',
            # 'localbitcoins_real_name',
            # 'localbitcoins_feedback_score',
            # 'localbitcoins_trade_count',
            # 'localbitcoins_country_code_phone_number',
            # 'localbitcoins_last_country_code_ip',
            # 'sumsub_external_user_id',
            # 'sumsub_sdk_access_token',
            # 'sumsub_sdk_access_token_expiry',
            'name_match_checked',
            # 'id_verified',
            # 'liveness_verified',
            # 'address_verified',
            'video_verified',
            'source_of_funds_verified',
            'source_of_funds_limit',
            'company_verified',
            'btc_deposit_address',
            )


class TransactionLBCChangeForm(ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'client_bank_account_name',
            'client_bank_account_number',
            'client_bank_account_sort_code',
        )
    # def __init__(self, *args, **kwargs): 
    #     super().__init__(*args, **kwargs)                       
    #     self.fields['platform'].disabled = True

    # readonly_fields =(
    #     'platform',
    #     'action',
    #     'client',
    #     'reference',
    #     'amount_fiat',
    #     'amount_btc',
    #     'fee_btc',
    #     'exchange_price',
    #     'bank_account_name',
    #     'bank_account_number',
    #     'bank_account_sort_code',
    #     'localbitcoins_contact_id',
    #     'status',
    #     'created_at',
    #     'payment_completed_at',
    #     'closed_at',
    #     'pre_transaction_verification_tier'
    # )

    
    # btc_txid = models.CharField(max_length = 64, editable= False, null= True, blank= True)
    # btc_address = models.CharField(max_length = 64, editable = True, null= True, blank= True)

    
    # status = models.CharField(choices = ( ('i', 'Initialized'),('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pr', 'Pending Release'), ('pv1', 'Pending Verification - T1'), ('pv2', 'Pending Verification - T2'), ('pv3', 'Pending Verification - T3'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')), default='i', max_length=3 ) #finalzed means message sent
    
    # created_at = models.DateTimeField(null=True, blank=True)
    # payment_completed_at = models.DateTimeField(null=True, blank=True)
    # closed_at = models.DateTimeField(null=True, blank=True)
    
    
    # pre_transaction_verification_tier = models.IntegerField(editable = False, default = 0)