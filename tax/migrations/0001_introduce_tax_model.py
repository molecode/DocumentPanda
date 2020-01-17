# Generated by Django 2.2.5 on 2019-09-29 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('income', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Income')),
                ('income_tax', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Income Tax')),
                ('solidarity_tax', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Solidarity Tax')),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], unique=True, verbose_name='Year')),
            ],
            options={
                'ordering': ['year'],
            },
        ),
    ]