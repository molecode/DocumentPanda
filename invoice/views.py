import os
import calendar
from datetime import date

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from reports.models import MonthReport
from .models import Invoice
from .pdf import create_pdf

from profile_settings.models import ProfileSettings
from common.mixins import FormViewW3Mixin


def download(request, report_pk):
    report = get_object_or_404(MonthReport, pk=report_pk)
    return FileResponse(open(report.invoice.file_path, 'rb'), as_attachment=True)


def preview(request, report_pk):
    report = get_object_or_404(MonthReport, pk=report_pk)
    return FileResponse(open(report.invoice.file_path, 'rb'))


class InvoiceListView(ListView):
    model = Invoice


class InvoiceDetailView(DetailView):
    model = Invoice

    def get_object(self, queryset=None):
        report_pk = int(self.kwargs['report_pk'])
        try:
            invoice = self.get_queryset().get(month_report=report_pk)
        except Invoice.DoesNotExist:
            invoice = None
        return invoice

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            redirect_to = reverse_lazy('invoice:add', kwargs={'report_pk': self.kwargs['report_pk']})
        else:
            redirect_to = reverse_lazy('invoice:update', kwargs={'report_pk': self.kwargs['report_pk']})
        return redirect(redirect_to)


class ChangeInvoiceMixin(FormViewW3Mixin):
    model = Invoice
    fields = ['activity', 'your_full_name', 'your_street', 'your_city',
              'customer_name', 'customer_street', 'customer_city',
              'invoice_number', 'contract_number', 'invoice_date',
              'invoice_period_begin', 'invoice_period_end', 'email',
              'turnover_tax_number', 'bank_name', 'iban', 'bic']
    success_url = reverse_lazy('invoice:list')

    def get_object(self, queryset=None):
        report_pk = int(self.kwargs['report_pk'])
        report = MonthReport.objects.select_related('customer').get(pk=report_pk)
        return self.get_queryset().get(month_report=report)


class InvoiceDeleteView(ChangeInvoiceMixin, DeleteView):
    template_name = 'common/confirm_delete.html'


class InvoiceUpdateView(ChangeInvoiceMixin, UpdateView):
    template_name = 'invoice/update_form.html'

    def get_success_url(self):
        if 'download' in self.request.POST:
            report = self.object.month_report
            return reverse_lazy('invoice:download', kwargs={'report_pk': report.pk})
        return reverse_lazy('invoice:list')


class InvoiceCreateView(ChangeInvoiceMixin, CreateView):
    template_name = 'invoice/create_form.html'

    def _get_report(self):
        report_pk = int(self.kwargs['report_pk'])
        return MonthReport.objects.select_related('customer').get(pk=report_pk)

    def get_success_url(self):
        report = self.object.month_report
        if 'download' in self.request.POST:
            return reverse_lazy('invoice:download', kwargs={'report_pk': report.pk})
        return reverse_lazy('reports:year_report', kwargs={'year': report.year, 'customer': report.customer.id})

    def form_valid(self, form):
        report = self._get_report()
        customer = report.customer

        settings = ProfileSettings.get_solo()

        if not settings.email:
            settings.email = form.cleaned_data['email']
        if not settings.street:
            settings.address = form.cleaned_data['your_street']
        if not settings.city:
            settings.address = form.cleaned_data['your_city']
        if not settings.full_name:
            settings.full_name = form.cleaned_data['your_full_name']
        if not settings.turnover_tax_number:
            settings.turnover_tax_number = form.cleaned_data['turnover_tax_number']
        if not settings.bank_name:
            settings.bank_name = form.cleaned_data['bank_name']
        if not settings.iban:
            settings.iban = form.cleaned_data['iban']
        if not settings.bic:
            settings.bic = form.cleaned_data['bic']
        settings.save()

        if not customer.invoice_street:
            customer.invoice_street = form.cleaned_date['customer_street']
        if not customer.invoice_city:
            customer.invoice_city = form.cleaned_date['customer_city']
        if not customer.contract_number:
            customer.contract_number = form.cleaned_data['contract_number']
        customer.save()

        form.instance.month_report_id = report.pk
        success_url = super().form_valid(form)
        create_pdf(self.object)
        return success_url

    def get_initial(self):
        initial = super().get_initial()

        settings = ProfileSettings.get_solo()
        initial['your_full_name'] = settings.full_name
        initial['email'] = settings.email
        initial['your_street'] = settings.street
        initial['your_city'] = settings.city
        initial['turnover_tax_number'] = settings.turnover_tax_number
        initial['bank_name'] = settings.bank_name
        initial['iban'] = settings.iban
        initial['bic'] = settings.bic

        report = self._get_report()
        customer = report.customer

        initial['customer_name'] = customer.invoice_name
        initial['customer_street'] = customer.invoice_street
        initial['customer_city'] = customer.invoice_city
        initial['contract_number'] = customer.contract_number
        month = f'0{report.month}' if report.month < 10 else report.month
        initial['invoice_number'] = f'{customer.customer_id}-{report.year}-{month}'
        initial['invoice_date'] = date.today()
        last_month = date(year=report.year, month=report.month, day=1)
        initial['invoice_period_begin'] = last_month
        last_day = calendar.monthrange(report.year, report.month)[1]
        initial['invoice_period_end'] = last_month.replace(day=last_day)
        return initial
