# Generated by Django 4.1.2 on 2023-02-23 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_profile_email_profile_email_or_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_or_username',
            field=models.CharField(default='', max_length=255),
        ),
    ]
