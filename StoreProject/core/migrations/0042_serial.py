# Generated by Django 4.2.1 on 2023-05-11 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_remove_basket_items_basket_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('serial', models.CharField(max_length=1000)),
            ],
        ),
    ]