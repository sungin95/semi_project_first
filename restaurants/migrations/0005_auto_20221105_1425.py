# Generated by Django 3.2.13 on 2022-11-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20221105_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurants',
            old_name='전화번호',
            new_name='restaurant_phone_number',
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='parking',
            field=models.CharField(max_length=50),
        ),
    ]