# Generated by Django 3.2 on 2021-04-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_store_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_score',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2, null=True),
        ),
    ]
