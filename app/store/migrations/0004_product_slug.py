# Generated by Django 3.2 on 2021-05-01 11:54

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210501_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=models.CharField(max_length=255), editable=False, populate_from='name'),
        ),
    ]