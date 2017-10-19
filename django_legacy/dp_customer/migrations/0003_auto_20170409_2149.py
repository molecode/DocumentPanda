# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dp_customer', '0002_auto_20170409_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='Customer ID'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Customer name'),
        ),
    ]
