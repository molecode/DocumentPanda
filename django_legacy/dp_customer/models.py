from django.db import models
from django.utils.translation import ugettext_lazy as _

class Customer(models.Model):
    customer_id = models.PositiveSmallIntegerField(_('Customer ID'), unique=True)
    name = models.CharField(_('Customer name'), max_length=255, unique=True)
    default_fee = models.DecimalField(_('Project fee'), max_digits=5, decimal_places=2)
    notes = models.TextField(_('Notes'), blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.customer_id, self.name)

    class Meta:
        ordering = ['customer_id']
