# Generated by Django 4.1.2 on 2023-03-02 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_product_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video',
            field=models.URLField(default=''),
        ),
    ]