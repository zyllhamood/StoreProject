# Generated by Django 4.2 on 2023-04-29 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_product_hide_alter_profile_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhoEditSerial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('email_or_username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
    ]
