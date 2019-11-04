from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class ProfileSettings(SingletonModel):
    full_name = models.CharField(_('Your full name'), max_length=255, blank=True)
    street = models.CharField(_('Your street'), max_length=512, blank=True)
    city = models.CharField(_('Your city'), max_length=512, blank=True)
    email = models.EmailField(_('Your email'), blank=True)
    turnover_tax_number = models.CharField(_('You turnover tax number'), max_length=255, blank=True)
    bank_name = models.CharField(_('Bank name'), max_length=255, blank=True)
    iban = models.CharField(_('IBAN'), max_length=255, blank=True)
    bic = models.CharField(_('BIC'), max_length=255, blank=True)
    currency = models.CharField(_('Currency'), max_length=10, default='€')

    def __str__(self):
        return self.full_name if self.full_name else 'Profile'
