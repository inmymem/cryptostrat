# Generated by Django 3.0.6 on 2020-05-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localbitcoins', '0007_auto_20200530_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('i', 'Initialized'), ('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pv1', 'Pending Verification - T1'), ('pv2', 'Pending Verification - T2'), ('pv3', 'Pending Verification - T3'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')], default='i', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='source_of_funds_limit',
            field=models.IntegerField(blank=True, default=10001, null=True),
        ),
    ]
