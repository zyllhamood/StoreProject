# Generated by Django 4.1.6 on 2023-02-08 10:31

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_id_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dis',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
