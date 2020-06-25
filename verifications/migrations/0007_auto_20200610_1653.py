# Generated by Django 3.0.6 on 2020-06-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifications', '0006_cryptoaddressanalysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='address',
            field=models.CharField(editable=False, max_length=60),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='dark_market_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='dark_service_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='exchange_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='gambling_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='illegal_service_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='last_updated_fast',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='last_updated_global',
            field=models.IntegerField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='marketplace_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='miner_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='mixer_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='payment_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='ransom_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='risk_score',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='scam_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='stolen_coins_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='trusted_exchange_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='cryptoaddressanalysis',
            name='wallet_signal',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=3, null=True),
        ),
    ]
