# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-26 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='currency',
            field=models.CharField(default='€', max_length=10, verbose_name='Currency'),
        ),
    ]
