# Generated by Django 3.0.6 on 2020-05-29 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localbitcoins', '0005_auto_20200529_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('i', 'Initialized'), ('r', 'Released'), ('f', 'Finalized'), ('p', 'Paid'), ('pv', 'Pending Verification'), ('pv2', 'Pending Verification'), ('pv3', 'Pending Verification'), ('pp', 'Pending Payment'), ('d', 'Dispute'), ('c', 'Cancelled')], default='i', max_length=3),
        ),
    ]
