# Generated by Django 3.0.6 on 2020-05-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localbitcoins', '0003_auto_20200526_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='bank_account_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='bank_account_number',
            field=models.CharField(default=None, max_length=8),
        ),
        migrations.AddField(
            model_name='transaction',
            name='bank_account_sort_code',
            field=models.CharField(default=None, max_length=6),
        ),
    ]
