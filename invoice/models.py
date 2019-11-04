from django.db import models
from django.utils.translation import ugettext_lazy as _

from reports.models import MonthReport


class Invoice(models.Model):
    """
    This model holds the needed information for an invoice for one report.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    invoice_number = models.CharField(max_length=32, unique=True)
    month_report = models.OneToOneField(MonthReport,
                                        verbose_name=_('Month report'),
                                        on_delete=models.PROTECT)
    your_full_name = models.CharField(max_length=255)
    your_street = models.CharField(max_length=512)
    your_city = models.CharField(max_length=512)
    customer_name = models.CharField(max_length=255)
    customer_street = models.CharField(max_length=512)
    customer_city = models.CharField(max_length=512)
    contract_number = models.CharField(max_length=128)
    invoice_date = models.DateField()
    invoice_period_begin = models.DateField()
    invoice_period_end = models.DateField()
    activity = models.CharField(max_length=512)
    email = models.EmailField()
    turnover_tax_number = models.CharField(max_length=32)
    bank_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=255)
    bic = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512, blank=True)

    class Meta:
        ordering = ['-month_report__year', '-month_report__month']

    def __str__(self):
        return f'{self.invoice_number} - {self.month_report.customer.name}'
