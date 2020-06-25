from django.db import models
import uuid
from clients.verification_limits import st1_limit, st2_limit, st0_and_st1_one_transaction_limit
from django.utils import timezone
from verifications.verification_links import get_verification_url

# Create your models here.
class Client(models.Model):
    #keep the autoincrementing user id
    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    real_name = models.CharField(max_length=50, null = True, blank = True)
    company_name = models.CharField(max_length=50, null= True, blank = True)
    email = models.CharField(max_length=200, null = True, unique= True, blank= True)
    phone_number = models.CharField(max_length=20, null = True, unique= True, blank= True)
    telegram_username = models.CharField(max_length=20, null = True, unique= True, blank= True)

    localbitcoins_username = models.CharField("Username", unique= True, max_length= 30, editable = True, null= True, blank= True)
    localbitcoins_real_name = models.CharField("Real Name",max_length=50, null = True, blank= True)
    localbitcoins_feedback_score = models.IntegerField("Feedback Score", null= True, blank= True)
    localbitcoins_trade_count = models.IntegerField("Trade Count", null= True, blank= True)
    localbitcoins_country_code_phone_number = models.CharField("Phone Number Country Code", max_length= 5, null= True, blank= True)
    localbitcoins_last_country_code_ip = models.CharField("Last IP Country Code",max_length= 5, null= True, blank= True)

    sumsub_external_user_id = models.CharField(max_length=50, default = None, null= True, unique = True, blank= True)
    sumsub_sdk_access_token = models.CharField(max_length=50, default = None, null= True, blank= True)
    sumsub_sdk_access_token_expiry = models.DateTimeField(default = None, null = True, blank= True)
    
    name_match_checked  = models.BooleanField(default= False, blank= True) #check if the name given in LBC matches the name in the verification
    id_verified = models.BooleanField(default= False, blank= True)
    liveness_verified = models.BooleanField(default= False, blank= True)
    address_verified = models.BooleanField(default= False, blank= True)
    video_verified = models.BooleanField(default= False, blank= True)
    source_of_funds_verified = models.BooleanField(default= False, blank= True)
    source_of_funds_limit = models.IntegerField(default= 10001, null= True, blank= True)
    company_verified = models.BooleanField(default= False, blank= True)

    btc_deposit_address = models.CharField(max_length = 64, editable = True, null= True, blank= True)

    

    def __str__(self):
        if self.localbitcoins_username:
            return self.localbitcoins_username + ' - LBC'
        elif self.phone_number:
            return self.phone_number
        return str(self.uuid)
    class Meta:
        ordering = ('localbitcoins_username', 'phone_number', 'uuid')

    def lbc_username(self):
        return self.localbitcoins_username

    def identifier(self):
        if self.localbitcoins_username != None:
            return f'LBC user: {self.localbitcoins_username}'
        elif self.phone_number != None:
            return f'user Phone Number: {self.phone_number}'
        else:
            return f'user UUID: {str(self.uuid)}'

    def sumsub_token_active(self):
        if not self.sumsub_external_user_id:
            return None
        elif not self.sumsub_sdk_access_token:
            return False
        elif self.sumsub_sdk_access_token_expiry > timezone.now():
            return True
        elif self.sumsub_sdk_access_token_expiry < timezone.now():
            return False
    
    def sumsub_verification_link(self):
        return get_verification_url(self)
        
    def get_total_volume(self):
        total_volume = 0
        transactions = self.transaction_set.all()
        for transaction in transactions:
            if transaction.status != 'c':
                total_volume += transaction.amount_fiat
        return total_volume


    def total_sell_volume(self):
        total_volume = 0
        transactions = self.transaction_set.filter(action = 'S')
        for transaction in transactions:
            if transaction.status != 'c':
                total_volume += transaction.amount_fiat
        return total_volume


    def total_buy_volume(self):
        total_volume = 0
        transactions = self.transaction_set.filter(action= 'B')
        for transaction in transactions:
            if transaction.status != 'c':
                total_volume += transaction.amount_fiat
        return total_volume


    def get_verification_tier(self):
        tier = 0
        if all([self.name_match_checked, self.id_verified, self.liveness_verified, self.address_verified, self.video_verified, self.source_of_funds_verified]):
            tier = 3
        elif all([self.name_match_checked, self.id_verified, self.liveness_verified, self.address_verified, self.video_verified]):
            tier = 2
        elif all([self.name_match_checked, self.id_verified, self.liveness_verified, self.address_verified]):
            tier = 1
        return tier


    def get_number_of_transactions(self):
        return(len(self.transaction_set.filter(status='f')))


class Transaction(models.Model):
    platform = models.CharField(choices = ( ('LBC', 'Localbitcoins'), ('OFF', 'Offsite')), max_length=3, blank=False, editable = False, default= 'OFF')
    client = models.ForeignKey(Client, on_delete= models.CASCADE)
    action = models.CharField(choices=( ('B', 'Buy'), ('S', 'Sell') ), max_length=1, blank=False, editable = False)
    reference = models.CharField(max_length=30, unique = True, null=True)
    
    amount_fiat = models.FloatField(editable = False)
    amount_btc = models.FloatField(editable = False)
    fee_btc = models.FloatField(editable = False)
    exchange_price = models.FloatField(editable = False, null= True)
    
    
    client_bank_account_name = models.CharField(max_length= 50, default = None, null = True)
    client_bank_account_number = models.CharField(max_length=8, default = None, null = True)
    client_bank_account_sort_code = models.CharField(max_length=6, default = None, null = True)
    bank_account_name = models.CharField(max_length= 50, default = None)
    bank_account_number = models.CharField(max_length=8, default = None)
    bank_account_sort_code = models.CharField(max_length=6, default = None)
     
    localbitcoins_contact_id = models.IntegerField(unique=True, editable = False, null = True)
    
    btc_txid = models.CharField(max_length = 64, editable= False, null= True, blank= True)
    btc_address = models.CharField(max_length = 64, editable = True, null= True, blank= True)

    
    status = models.CharField(choices = ( ('i', 'Initialized'),('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pr', 'Pending Release'), ('pv1', 'Pending Verification - T1'), ('pv2', 'Pending Verification - T2'), ('pv3', 'Pending Verification - T3'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')), default='i', max_length=3 ) #finalzed means message sent
    
    created_at = models.DateTimeField(null=True, blank=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    
    pre_transaction_verification_tier = models.IntegerField(editable = False, default = 0)

    def get_reference(self):
        if self.platform == 'LBC':
            return ('X' + str(10000 + self.id))
        elif self.platform == 'OFF':
            return ('F' + str(10000 + self.id))


    def get_sell_required_verification_tier(self):
        total_volume = self.client.total_sell_volume()
        required_verification_tier = 7 #should never happen
        if total_volume >= self.client.source_of_funds_limit and self.client.source_of_funds_verified== True:
            required_verification_tier = 6
        elif total_volume >= st2_limit:
            required_verification_tier = 3
        elif total_volume >= st1_limit or self.amount_fiat >= st0_and_st1_one_transaction_limit:
            required_verification_tier = 2
        elif total_volume < st1_limit:
            required_verification_tier = 1
        return required_verification_tier

    def get_bank_account(self):
        return {'name': self.bank_account_name, 'number': self.bank_account_number, 'sort_code': self.bank_account_sort_code}
    
    def get_st1_limit(self):
        return st1_limit
    def get_st2_limit(self):
        return st2_limit
    def get_st0_and_st1_one_transaction_limit(self):
        return(st0_and_st1_one_transaction_limit)
