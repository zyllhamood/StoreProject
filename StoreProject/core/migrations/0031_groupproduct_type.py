# Generated by Django 4.1.7 on 2023-04-04 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupproduct',
            name='type',
            field=models.CharField(default='Tools', max_length=255),
        ),
    ]