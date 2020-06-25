from django.db import models
from django.utils import timezone
from localbitcoins.models import User
from clients.models import Client
# Create your models here.


class RawSumSubNotification(models.Model):
    header = models.TextField()
    body = models.TextField()


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, editable = False, null = True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, editable = False, null = True)
    applicant_id = models.CharField(max_length=50, null=True, unique=True)
    inspection_id = models.CharField(max_length=50, null=True, blank=True)  #inspection ID that contains a result of the applicant
    correlation_id = models.CharField(max_length=50, null=True,blank=True)  #an ID to debug in case of unexpected errors (should be provided to Sum&Substance)
    review_status = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    review_answer = models.CharField(max_length=10, null=True, blank=True)
    review_reject_type = models.CharField(max_length=10, null=True, blank=True)
    moderation_comment = models.TextField(null=True, blank=True)
    client_comment = models.TextField(null=True, blank=True)
    reject_labels = models.TextField(null=True, blank=True)

    access_token_for_sdk = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.client.uuid) +'_sumsub'


class IdDoc(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, editable= False, null = True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, editable = False, null = True)
    doc_type = models.CharField(max_length=30)
    country = models.CharField(max_length=3)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank = True)
    last_name = models.CharField(max_length=50, null = True)
    issue_date = models.DateField(null=True,)
    valid_until = models.DateField()
    number = models.CharField(max_length=50)
    date_of_birth = models.DateField()


class Address(models.Model):
    sub_street = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100)        
    state = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50)
    postCode = models.CharField(max_length=30)
    country = models.CharField(max_length=3)

class AddressDoc(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, editable= False, null = True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, editable = False, null = True)
    doc_type = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank = True)
    last_name = models.CharField(max_length=50, null = True)
    issue_date = models.DateField()
    sub_street = models.CharField(max_length=100, null=True, blank=True, default = 'hi')
    street = models.CharField(max_length=100, default = 'hi')        
    state = models.CharField(max_length=50, null=True, blank=True, default = 'hi')
    town = models.CharField(max_length=50, default = 'hi')
    postCode = models.CharField(max_length=30,default = 'hi')
    country = models.CharField(max_length=3, default = 'hi')


class Person(models.Model):
    user = models.OneToOneField(User, on_delete= models.SET_NULL, editable= False, null = True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, editable = False, null = True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    country_of_residence = models.CharField(max_length=3, null=True, blank=True)
    nationality = models.CharField(max_length=3, null=True, blank=True)
    country_of_birth = models.CharField(max_length=3, null=True, blank=True)
    state_of_birth = models.CharField(max_length=50, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete= models.CASCADE)
    
    def get_real_name(self):
        real_name = ''
        name_components = [self.first_name, self.middle_name, self.last_name]
        for name_component in name_components:
            if name_component != None:
                real_name = (real_name + ' ' + name_component).lstrip()
        return real_name


class CryptoTransactionAnalysis(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, editable = False, null= True)
    created_at = models.DateTimeField(auto_now_add=True, editable = False)
    txid = models.CharField(max_length = 64, editable= False)
    address = models.CharField(max_length = 64, editable = False) #this is the deposit address unique to every client
    risk_score = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    
    dark_market_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    dark_service_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    exchange_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    gambling_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    illegal_service_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    marketplace_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    miner_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    mixer_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    payment_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    ransom_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    scam_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    stolen_coins_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    trusted_exchange_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    wallet_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    atm_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    risky_exchange_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)

    def analysis_result(self):
        result = 'Red'
        if self.risk_score > 0.7:
            result = 'Red'
        elif self.risk_score >= 0.25:
            result = 'Yellow'
        elif self.risk_score < 0.25:
            result = 'Green'
        return result


class CryptoAddressAnalysis(models.Model):
    #user = 
    created_at = models.DateTimeField(auto_now_add=True, editable = False)
    address = models.CharField(max_length = 64, editable = False)
    risk_score = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)

    dark_market_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    dark_service_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    exchange_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    gambling_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    illegal_service_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    marketplace_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    miner_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    mixer_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    payment_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    ransom_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    scam_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    stolen_coins_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    trusted_exchange_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    wallet_signal = models.DecimalField(max_digits= 3, decimal_places=2, null = True, editable = False)
    
    last_updated_global = models.IntegerField(null = True, editable = False) #when they last updated it using their global analyis
    last_updated_fast = models.IntegerField(null = True, editable = False) #when they last updated it using their fast analyis

    #Based on the RS, the funds can be accepted (RS below 25%), sent back to the sender (RS over 70%) automatically, or conveyed for additional investigation with Crystal Pro or Express (see below).
    def analysis_result(self):
        result = 'Red'
        if self.risk_score > 0.7:
            result = 'Red'
        elif self.risk_score >= 0.25:
            result = 'Yellow'
        elif self.risk_score < 0.25:
            result = 'Green'
        return result
        #check if need to use float

        