# Generated by Django 4.2.1 on 2023-05-28 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_productspaid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('paid_method', models.CharField(max_length=500)),
                ('note', models.TextField(blank=True)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]