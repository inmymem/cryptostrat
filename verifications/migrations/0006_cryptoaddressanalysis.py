# Generated by Django 3.0.6 on 2020-06-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifications', '0005_auto_20200609_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoAddressAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=60)),
                ('risk_score', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('dark_market_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('dark_service_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('exchange_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('gambling_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('illegal_service_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('marketplace_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('miner_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('mixer_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('payment_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('ransom_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('scam_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('stolen_coins_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('trusted_exchange_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('wallet_signal', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('last_updated_global', models.IntegerField()),
                ('last_updated_fast', models.IntegerField()),
            ],
        ),
    ]
