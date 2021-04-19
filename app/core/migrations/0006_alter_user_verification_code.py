# Generated by Django 3.2 on 2021-04-19 11:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_user_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.IntegerField(default=69118, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
