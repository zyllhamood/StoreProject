# Generated by Django 4.1.6 on 2023-02-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_dis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dis',
            field=models.TextField(),
        ),
    ]
