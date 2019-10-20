from django.db import models
from django.utils.translation import ugettext_lazy as _

from reports.models import MonthReport


class BankAccount(models.Model):
    """
    This model holds the needed information for a bank account.
    """
    bank_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=255)
    bic = models.CharField(max_length=255)


class Invoice(models.Model):
    """
    This model holds the needed information for an invoice for one report.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    invoice_number = models.CharField(max_length=32, unique=True)
    month_report = models.ForeignKey(MonthReport,
                                     verbose_name=_('Month report'),
                                     on_delete=models.PROTECT)
    my_address = models.TextField()
    customer_address = models.TextField()
    invoice_date = models.DateField()
    invoice_period_begin = models.DateField()
    invoice_period_end = models.DateField()
    email = models.EmailField()
    turnover_tax_number = models.CharField(max_length=32)
    bank_account = models.ForeignKey(BankAccount,
                                     verbose_name=_('Bank account'),
                                     on_delete=models.PROTECT)


