# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-26 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthreport',
            options={'ordering': ['-year', '-month']},
        ),
        migrations.AlterField(
            model_name='monthreport',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12, verbose_name='Month'),
        ),
    ]