# Generated by Django 4.1.2 on 2023-02-22 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_profile_first_name_remove_profile_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='added_on',
        ),
    ]
