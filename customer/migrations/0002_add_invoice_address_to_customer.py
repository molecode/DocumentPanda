# Generated by Django 2.2.5 on 2019-10-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='invoice_address',
            field=models.TextField(blank=True, verbose_name='Invoice address of the customer'),
        ),
    ]