import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

class Tax(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    income = models.DecimalField(_('Income'), max_digits=10, decimal_places=2)
    taxable_income = models.DecimalField(_('Taxable Income'), max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(_('Income Tax'), max_digits=10, decimal_places=2)
    solidarity_tax = models.DecimalField(_('Solidarity Tax'), max_digits=10, decimal_places=2)
    year = models.IntegerField(
               _('Year'),
               choices=[(year, year) for year in range(2000, datetime.datetime.now().year+1)],
               unique=True
           )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return '{} - {} - {}'.format(self.year, self.income, self.get_total_tax())

    def get_total_tax(self):
        return self.income_tax + self.solidarity_tax

    def get_profit(self):
        return self.income - self.get_total_tax()

    def get_profit_per_month(self):
        return self.get_profit() / 12

    def get_tax_percentage(self):
        return 100/self.taxable_income*self.get_total_tax()
