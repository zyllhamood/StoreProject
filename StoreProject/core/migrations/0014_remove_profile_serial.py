# Generated by Django 4.1.2 on 2023-02-22 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_profile_serial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='serial',
        ),
    ]
