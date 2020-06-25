from django.db import models

# Create your models here.

class Fiat_transaction(models.Model):
    clientOrder = models.CharField(max_length=50)
    orderReference = models.CharField(max_length=50)
    timestamp = models.CharField(max_length=25)
    amount = models.FloatField() #amount after fees
    operationAmount = models.FloatField(null=True)#amount of the transaction before fees (e.g amount clients sent)
    currency = models.CharField(max_length=4)
    status = models.CharField(max_length=50)
    returned = models.BooleanField(null=True)
    operStatus = models.CharField(max_length=50)
    complianceStatus = models.CharField(max_length=50)
    paymentMethod = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    iban = models.CharField(max_length=30, null=True)
    sortCode = models.CharField(max_length=6)
    accountNumber = models.CharField(max_length=8)
    bankSwiftCode = models.CharField(max_length=30, null=True)
    transactionType = models.CharField("In/OUT", max_length=15)

    def release(self):
        return True
    release.boolean = True
    
class CJ_notification(models.Model):
    header = models.TextField()
    body = models.TextField()
    valid = models.BooleanField()

#CJ_notification.objects.all().delete()