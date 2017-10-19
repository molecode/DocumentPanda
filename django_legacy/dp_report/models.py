import datetime
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dp_customer.models import Customer


class MonthReport(models.Model):
    MONTH_CHOICES = (
        (1, _('January')),
        (2, _('February')),
        (3, _('March')),
        (4, _('April')),
        (5, _('May')),
        (6, _('June')),
        (7, _('July')),
        (8, _('August')),
        (9, _('September')),
        (10, _('October')),
        (11, _('November')),
        (12, _('December')),
    )

    customer = models.ForeignKey(Customer,
                                 verbose_name=_('Customer'),
                                 related_name='month',
                                 on_delete=models.PROTECT)
    fee = models.DecimalField(_('Project fee'),
                              max_digits=5,
                              decimal_places=2,
                              blank=True,
                              null=True)
    month = models.IntegerField(_('Month'),
                                choices=MONTH_CHOICES,
                                default=datetime.datetime.now().month)
    year = models.IntegerField(_('Year'),
                               choices=[(year, year) for year in range(2012, datetime.datetime.now().year+1)],
                               default=datetime.datetime.now().year)
    hours = models.DecimalField(_('Working hours'),
                                max_digits=6,
                                decimal_places=2)

    class Meta:
        unique_together = (('customer', 'month', 'year'),)

    @property
    def netto(self):
        if self.hours == 0 or self.fee == 0:
            return 0
        return round(self.fee * self.hours, 2)

    @property
    def umsatzsteuer(self): #TODO -- translation
        return round(self.netto * Decimal(0.19), 2)

    @property
    def brutto(self):
        return self.netto + self.umsatzsteuer

    def hours_per_week(self): #TODO -- 4.33 durch tatsaechliche Wochenanzahl des Monats ersetzen
        return round(self.hours / Decimal(4.33), 2)

    def __str__(self):
        return '{}/{} - {} - {}: {} Euro'.format(self.year,
                                                 self.month,
                                                 self.customer.name,
                                                 _('Netto'),
                                                 self.netto)
