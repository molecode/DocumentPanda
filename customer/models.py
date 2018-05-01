from django.db import models
from django.utils.translation import ugettext_lazy as _

class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(_('Customer name'), max_length=255, unique=True)
    customer_id = models.IntegerField(_('Customer ID'), unique=True)
    default_fee = models.DecimalField(_('Project fee per hour'), max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['customer_id']

    def __str__(self):
        return '{} - {} - {}'.format(self.customer_id, self.name, self.default_fee)
