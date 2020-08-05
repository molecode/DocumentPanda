from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import MonthReport


class MonthReportForm(forms.ModelForm):
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

