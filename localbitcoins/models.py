from django.db import models
import uuid #universally unique identifiers
from clients.verification_limits import st1_limit, st2_limit, st0_and_st1_one_transaction_limit
# Create your models here.

class User(models.Model):
    #keep the autoincrementing user id
    uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    username = models.CharField("localbitcoins username", unique= True, max_length= 30, editable = False)
    real_name = models.CharField(max_length=50, null = True)
    company_name = models.CharField(max_length=50, null= True, blank = True)
    feedback_score = models.IntegerField()
    trade_count = models.IntegerField()
    country_code_phone_number = models.CharField(max_length= 5, null= True, blank= True)
    last_country_code_ip = models.CharField(max_length= 5, null= True, blank= True)
    
    name_match_checked  = models.BooleanField(default= False, blank= True) #check if the name given in LBC matches the name in the verification
    id_verified = models.BooleanField(default= False, blank= True)
    liveness_verified = models.BooleanField(default= False, blank= True)
    address_verified = models.BooleanField(default= False, blank= True)
    video_verified = models.BooleanField(default= False, blank= True)
    source_of_funds_verified = models.BooleanField(default= False, blank= True)
    source_of_funds_limit = models.IntegerField(default= 10001, null= True, blank= True)
    company_verified = models.BooleanField(default= False, blank= True)
    
    def __str__(self):
        return self.username

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


    def get_past_verification_tier(self, action, transaction_amount):
        """To return the verification tier the user was at before the transaction whos amount we pass as an arguement"""
        if action == 'B':
            number_of_previous_transactions = self.get_number_of_transactions()
            if number_of_previous_transactions == 0:
                return 0
            elif number_of_previous_transactions >= 1:
                return 1
        if action == 'S':
            pre_transaction_volume = self.get_total_volume() - transaction_amount
            pre_transaction_sell_volume = self.total_sell_volume() - transaction_amount
            if pre_transaction_volume == 0:
                pre_transaction_verification_tier = 0
            elif pre_transaction_sell_volume < st1_limit:
                pre_transaction_verification_tier = 1
            elif pre_transaction_sell_volume < st2_limit:
                pre_transaction_verification_tier = 2
            elif pre_transaction_sell_volume >= st2_limit:
                pre_transaction_verification_tier = 3
            return pre_transaction_verification_tier
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, editable = False)
    contact_id = models.IntegerField(unique=True, editable = False)
    action = models.CharField(choices=( ('B', 'Buy'), ('S', 'Sell') ), max_length=1, blank=False, editable = False) 
    amount_fiat = models.FloatField(editable = False)
    amount_btc = models.FloatField(editable = False)
    fee_btc = models.FloatField(editable = False)
    status = models.CharField(choices = ( ('i', 'Initialized'),('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pv1', 'Pending Verification - T1'), ('pv2', 'Pending Verification - T2'), ('pv3', 'Pending Verification - T3'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')), default='i', max_length=3 ) #finalzed means message sent
    reference = models.CharField(max_length=30)
    created_at = models.DateTimeField(null=True, blank=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    bank_account_name = models.CharField(max_length= 50, default = None)
    bank_account_number = models.CharField(max_length=8, default = None)
    bank_account_sort_code = models.CharField(max_length=6, default = None)
    exchange_price = models.FloatField(editable = False, null= True)
    pre_transaction_verification_tier = models.IntegerField(editable = False, default = 0)
    #add advertisement id to be able to 
    #iban = models.CharField(max_length=30, null=True) add later if needed


    def get_sell_required_verification_tier(self):
        total_volume = self.user.total_sell_volume()
        required_verification_tier = 7 #should never happen
        if total_volume >= self.user.source_of_funds_limit and self.user.source_of_funds_verified== True:
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