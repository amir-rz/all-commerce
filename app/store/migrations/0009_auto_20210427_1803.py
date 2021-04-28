# Generated by Django 3.2 on 2021-04-27 13:33

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20210427_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='category',
        ),
        migrations.AlterField(
            model_name='brand',
            name='created',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='updated',
            field=django_jalali.db.models.jDateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated',
            field=django_jalali.db.models.jDateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=django_jalali.db.models.jDateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='created',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='updated',
            field=django_jalali.db.models.jDateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='created',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='updated',
            field=django_jalali.db.models.jDateField(auto_now=True),
        ),
    ]
