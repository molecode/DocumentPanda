from django import forms
from django.utils.translation import gettext_lazy as _

from .models import MonthReport


class FeeMonthReportForm(forms.ModelForm):
    class Meta:
        model = MonthReport
        fields = ['customer', 'month', 'year', 'hours', 'fee', 'vat_percent']

    hours = forms.DecimalField(label=_('Working hours'),
                               localize=True,
                               max_digits=6,
                               decimal_places=2)
    fee = forms.DecimalField(label=_('Project fee per hour'),
                             localize=True,
                             max_digits=5,
                             decimal_places=2,
                             required=False)


class FixedPriceMonthReportForm(forms.ModelForm):
    class Meta:
        model = MonthReport
        fields = ['customer', 'month', 'year', 'fixed_price', 'vat_percent']

    fixed_price = forms.DecimalField(label=_('Fixed price'),
                                     localize=True,
                                     max_digits=6,
                                     decimal_places=2)
