import datetime
from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from customer.models import Customer


class CurrencyMixin(object):
    """Mixin for getting values with currency"""
    def value_with_currency(self, value):
        val = getattr(self, value)
        if val:
            return '{} {}'.format(val, MonthReport.CURRENCY)
        else:
            return val

    @property
    def netto_with_currency(self):
        """Get the netto with currency."""
        return self.value_with_currency('netto')

    @property
    def vat_with_currency(self):
        """Get the VAT with currency."""
        return self.value_with_currency('vat')

    @property
    def brutto_with_currency(self):
        """Get the brutto with currency."""
        return self.value_with_currency('brutto')

    @property
    def fee_with_currency(self):
        """Get the fee with currency."""
        return self.value_with_currency('fee')


class MonthReport(CurrencyMixin, models.Model):
    """
    This model holds the needed information for a monthly report.
    The needed information are only the hours of work and the fee of the project.
    Setting the fee here in this model is optional, it will override the fee
    which is set at customer level.
    """
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

    # TODO -- timo -- Should be not constant
    CURRENCY = '€'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer,
                                 verbose_name=_('Customer'),
                                 related_name='month_report',
                                 on_delete=models.PROTECT)
    fee = models.DecimalField(_('Project fee per hour'),
                              max_digits=5,
                              decimal_places=2,
                              blank=True,
                              null=True)
    month = models.IntegerField(_('Month'),
                                choices=MONTH_CHOICES,
                                default=datetime.datetime.now().month)
    year = models.IntegerField(_('Year'),
                               choices=[(year, year) for year in range(2000, datetime.datetime.now().year+1)],
                               default=datetime.datetime.now().year)
    hours = models.DecimalField(_('Working hours'),
                                max_digits=6,
                                decimal_places=2)
    slug = models.SlugField()

    class Meta:
        unique_together = (('customer', 'month', 'year'),)
        ordering = ['-year', '-month']

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}'.format(self.year, self.month))
        if not self.fee:
            self.fee = self.customer.default_fee
        super(MonthReport, self).save(*args, **kwargs)

    @property
    def netto(self):
        """Get the netto amount of money of this month."""
        if self.hours == 0 or self.fee == 0:
            return 0
        return round(self.fee * self.hours, 2)

    @property
    def vat(self):
        """Get the VAT of this month."""
        return round(self.netto * Decimal(0.19), 2)

    @property
    def brutto(self):
        """Get the brutto amount of money of this month."""
        return self.netto + self.vat

    def hours_per_week(self): #TODO -- timo -- 4.33 durch tatsaechliche Wochenanzahl des Monats ersetzen
        """Get the hours of work of this month."""
        return round(self.hours / Decimal(4.33), 2)

    @classmethod
    def get_last_report(cls):
        try:
            return cls.objects.order_by('id')[0]
        except IndexError:
            return None

    def __add__(self, other):
        if self.fee == 0 or other.fee == 0:
            self.fee = self.fee + other.fee
        else:
            self.fee = (self.fee + other.fee) / 2
        self.hours += other.hours
        return self

    def __str__(self):
        customer_name = ' - {}'.format(self.customer.name) if hasattr(self, 'customer') else ''
        return '{}/{:0>2} - {} - {} Euro'.format(self.year,
                                                 self.month,
                                                 _('Netto'),
                                                 self.netto,
                                                 customer_name)
