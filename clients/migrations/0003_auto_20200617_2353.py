# Generated by Django 3.0.6 on 2020-06-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_sumsub_external_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='sumsub_external_user_id',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
