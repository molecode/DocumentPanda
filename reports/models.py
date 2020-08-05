import datetime
import calendar
from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from profile_settings.models import ProfileSettings
from customer.models import Customer


class MonthReport(models.Model):
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
                                choices=MONTH_CHOICES)
    year = models.IntegerField(_('Year'),
                               choices=[(year, year) for year in range(2000, datetime.datetime.now().year+1)])
    hours = models.DecimalField(_('Working hours'),
                                max_digits=6,
                                decimal_places=2)
    slug = models.SlugField()
    vat_percent = models.DecimalField(_('VAT in %'), max_digits=4, decimal_places=2, default=19)

    class Meta:
        unique_together = (('customer', 'month', 'year'),)
        ordering = ['-year', '-month']

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}'.format(self.year, self.month))
        if not self.fee:
            self.fee = self.customer.default_fee
        super(MonthReport, self).save(*args, **kwargs)

    @property
    def brutto(self):
        """Get the brutto amount of money of this month."""
        if self.hours == 0 or self.fee == 0:
            return 0
        return round(self.fee * self.hours, 2)

    @property
    def vat(self):
        """Get the VAT of this month."""
        return round(self.brutto / Decimal(100) * self.vat_percent, 2)

    @property
    def brutto_vat(self):
        """Get the brutto + VAT amount of money of this month."""
        return self.brutto + self.vat

    @property
    def hours_per_day(self):
        """Get the hours per day."""
        business_days = len([x for x, y in calendar.Calendar().itermonthdays2(int(self.year), self.month) if x != 0 and y not in [4,5]])
        return round(self.hours / Decimal(business_days), 2)

    @property
    def hours_per_week(self):
        """Get the hours per week."""
        weeks = calendar.monthrange(int(self.year), self.month)[1] / Decimal(7)
        return round(self.hours / weeks, 2)

    def __add__(self, other):
        total_hours = self.hours + other.hours
        self.fee = (self.brutto + other.brutto) / total_hours
        self.hours = total_hours
        return self

    def __str__(self):
        customer_name = ' - {}'.format(self.customer.name) if hasattr(self, 'customer') else ''
        return '{}/{:0>2} - {} - {} Euro'.format(self.year,
                                                 self.month,
                                                 _('Brutto'),
                                                 self.brutto,
                                                 customer_name)


class AbstractReport():
    """
    Abstract class for year and quarter reports.
    """
    def __init__(self):
        self.brutto, self.brutto_vat, self.vat, self.fee, self.hours, self.hours_per_day, self.hours_per_week = (Decimal(0.00),)*7
        self.calculate_values()

    def sum_values(self, other):
        self.brutto += other.brutto
        self.brutto_vat += other.brutto_vat
        self.vat += other.vat
        self.fee += other.fee if other.fee else Decimal(0.00)
        self.hours += other.hours
        self.hours_per_day += other.hours_per_day
        self.hours_per_week += other.hours_per_week


class YearReport(AbstractReport):
    """
    This class represents a report for one year. It holds the summed up month and quarter values
    and also the total amount.
    """
    def __init__(self, year, month_queryset, customer=None):
        self.settings = ProfileSettings.get_solo()
        self.customer = customer
        self.year = year
        self.months = self.create_months_from_queryset(month_queryset)
        self.quarters = self.create_quarters()
        self.currency = self.settings.currency
        super().__init__()

    def create_months_from_queryset(self, month_queryset):
        months = {i: MonthReport(month=i, year=self.year, hours=0, fee=Decimal(0.00)) for i in range(1, 13)}
        for month_report in month_queryset:
            if self.customer:
                months[month_report.month] = month_report
            else:
                months[month_report.month] += month_report

        return [y for _, y in months.items()]

    def calculate_values(self):
        for quarter in self.quarters:
            self.sum_values(quarter)
        filled_quarters = self.get_filled_quarters()
        self.fee = round(self.fee/filled_quarters, 2)
        self.hours_per_day = round(self.hours_per_day/filled_quarters, 2)
        self.hours_per_week = round(self.hours_per_week/filled_quarters, 2)

    def get_filled_quarters(self):
        count = 0
        for quarter in self.quarters:
            count += 1 if quarter.fee > 0 else 0
        return count if count > 0 else 1

    def create_quarters(self):
        quarters = []
        for i in range(1, 5):
            quarters.append(self.QuarterReport(i, self.months))
        return quarters

    class QuarterReport(AbstractReport):
        """
        This class represents a quarter of the year with all needed summed amounts.
        """
        def __init__(self, quarter_number, months):
            if quarter_number < 1 or quarter_number > 4:
                raise
            self.quarter_number = quarter_number
            self.months = self.filter_quarter(months)
            super().__init__()

        def filter_quarter(self, months):
            return months[3*self.quarter_number-3:3*self.quarter_number]

        def calculate_values(self):
            for month in self.months:
                self.sum_values(month)
            filled_months = self.get_filled_months()
            self.fee = round(self.fee/filled_months, 2)
            self.hours_per_day = round(self.hours_per_day/filled_months, 2)
            self.hours_per_week = round(self.hours_per_week/filled_months, 2)

        def get_filled_months(self):
            count = 0
            for month in self.months:
                count += 1 if month.fee > 0 else 0
            return count if count > 0 else 1

        def __str__(self):
            return '{}. {}'.format(self.quarter_number, _('Quarter'))
