# Generated by Django 3.0.6 on 2020-06-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localbitcoins', '0008_auto_20200530_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='exchange_price',
            field=models.FloatField(editable=False, null=True),
        ),
    ]
