from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Tax


class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['year', 'income', 'income_tax', 'solidarity_tax']

    income = forms.DecimalField(
                label=_('Income'),
                localize=True,
                max_digits=10,
                decimal_places=2
             )

    income_tax = forms.DecimalField(
                    label=_('Income tax'),
                    localize=True,
                    max_digits=10,
                    decimal_places=2
                 )

    solidarity_tax = forms.DecimalField(
                        label=_('Solidarity tax'),
                        localize=True,
                        max_digits=10,
                        decimal_places=2
                     )
