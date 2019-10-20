from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['my_address', 'customer_address', 'invoice_number', 'invoice_date',
                  'invoice_period_begin', 'invoice_period_end', 'email', 'turnover_tax_number', 'bank_account']

#    default_fee = forms.DecimalField(label=_('Project fee per hour'),
#                                     localize=True,
#                                     max_digits=5,
#                                     decimal_places=2)

