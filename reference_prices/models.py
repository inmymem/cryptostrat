from django.db import models

# Create your models here.

class ReferencePrice(models.Model):
    currency_pair = models.CharField(unique=True, max_length=10)
    price = models.FloatField()