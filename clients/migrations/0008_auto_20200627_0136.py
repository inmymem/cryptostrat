# Generated by Django 3.0.7 on 2020-06-27 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20200625_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
