# Generated by Django 3.2.13 on 2022-11-03 11:40

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='restaurant_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]
