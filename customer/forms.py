from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'customer_id', 'contract_number', 'invoice_name',
                  'invoice_street', 'invoice_city', 'default_fee']

    default_fee = forms.DecimalField(label=_('Project fee per hour'),
                                     localize=True,
                                     max_digits=5,
                                     decimal_places=2)