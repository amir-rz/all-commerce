# Generated by Django 3.2 on 2021-04-21 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otp_auth_user', '0013_user_is_verified'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]