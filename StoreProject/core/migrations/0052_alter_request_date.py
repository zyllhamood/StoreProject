# Generated by Django 4.2.1 on 2023-08-23 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 23, 15, 48, 58, 359268)),
        ),
    ]