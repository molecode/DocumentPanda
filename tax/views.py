import csv
from io import TextIOWrapper

from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Tax
from .forms import TaxForm
from common.forms import UploadForm
from common.mixins import FormViewW3Mixin


class TaxListView(ListView):
    model = Tax


class TaxDetailView(DetailView):
    model = Tax


class ChangeTaxMixin(FormViewW3Mixin):
    """Mixin for every modifing TaxView: create, update, delete."""
    model = Tax
    form_class = TaxForm
    success_url = reverse_lazy('tax:index')


class TaxCreateView(ChangeTaxMixin, CreateView):
    template_name = 'common/form.html'


class TaxUpdateView(ChangeTaxMixin, UpdateView):
    template_name = 'common/form.html'


class TaxDeleteView(ChangeTaxMixin, DeleteView):
    template_name = 'common/confirm_delete.html'


class TaxImportView(SuccessMessageMixin, FormView):
    template_name = 'tax/import_tax.html'
    form_class = UploadForm
    success_url = reverse_lazy('tax:index')

    def form_valid(self, form):
        uploaded_file = TextIOWrapper(form.cleaned_data['file'].file, encoding='ascii')
        csv_file = csv.DictReader(uploaded_file)
        warnings = []
        errors = []
        success_counter = 0
        total_counter = 0
        for row in csv_file:
            try:
                total_counter += 1
                year = row['year']
                income = row['income']
                taxable_income = row['taxable_income']
                income_tax = row['income_tax']
                solidarity_tax = row['solidarity_tax']
                tax = Tax(
                    year=year,
                    income=income,
                    taxable_income=taxable_income,
                    income_tax=income_tax,
                    solidarity_tax=solidarity_tax
                    )
                tax.save()
                success_counter += 1
            except IntegrityError:
                warnings.append('{} {} (line: {})'.format(_('Tax entry exists:'),
                                                               tax.year,
                                                               csv_file.line_num))
        if success_counter > 0:
            messages.success(self.request, _('{} of {} tax entries successfully imported.<br />'.format(success_counter, total_counter)))
        if warnings:
            messages.warning(self.request, self.get_html_list(warnings))
        if errors:
            messages.error(self.request, self.get_html_list(errors))
        return super(TaxImportView, self).form_valid(form)

    @staticmethod
    def get_html_list(message_list):
        if len(message_list) > 1:
            html_snippet = '<ul>'
            for message in message_list:
                html_snippet += '<li>{}</li>'.format(message)
            html_snippet += '</ul>'
        else:
            html_snippet = message_list[0] + '<br />'
        return html_snippet


class TaxExportCSV(View):
    """
    Export tax as csv.
    """
    def get(self, *args, **kwargs):
        tax_set = Tax.objects.all()
        file_name = 'document_panda_tax'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)

        writer = csv.writer(response)
        writer.writerow(['year', 'income', 'taxable_income', 'income_tax', 'solidarity_tax'])
        for tax in tax_set:
            writer.writerow([tax.year, tax.income, tax.taxable_income, tax.income_tax, tax.solidarity_tax])

        return response
