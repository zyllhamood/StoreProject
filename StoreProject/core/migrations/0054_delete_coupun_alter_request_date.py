# Generated by Django 4.2.1 on 2023-09-07 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_coupun_alter_request_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupun',
        ),
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 7, 15, 11, 53, 229534)),
        ),
    ]
