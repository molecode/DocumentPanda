from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(_('Customer name'), max_length=255, unique=True)
    customer_id = models.IntegerField(_('Customer ID'), unique=True)
    default_fee = models.DecimalField(_('Project fee per hour'), max_digits=5, decimal_places=2)
    contract_number = models.CharField(_('Contract number'), max_length=128, blank=True)
    invoice_name = models.CharField(_('Invoice name of the customer'), max_length=255, blank=True)
    invoice_street = models.CharField(_('Invoice street of the customer'), max_length=255, blank=True)
    invoice_city = models.CharField(_('Invoice city of the customer'), max_length=255, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['customer_id']

    def __str__(self):
        return '{} - {} - {}'.format(self.customer_id, self.name, self.default_fee)
