# Generated by Django 2.2.6 on 2019-11-04 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_add_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='contract_number',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]