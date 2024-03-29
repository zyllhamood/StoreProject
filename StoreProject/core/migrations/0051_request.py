# Generated by Django 4.2.1 on 2023-08-23 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_product_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('method', models.CharField(default='', max_length=25)),
                ('url', models.CharField(default='', max_length=1000)),
                ('headers', models.TextField(default='')),
                ('data', models.TextField(blank=True, default='')),
                ('status_code', models.CharField(default='', max_length=10)),
                ('response', models.TextField(default='')),
                ('cookies', models.TextField(default='')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 8, 23, 15, 48, 20, 620228))),
            ],
        ),
    ]
