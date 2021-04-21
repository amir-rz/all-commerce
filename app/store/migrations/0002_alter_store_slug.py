# Generated by Django 3.2 on 2021-04-21 21:01

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True),
        ),
    ]
