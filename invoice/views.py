import calendar
from datetime import date

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from reports.models import MonthReport
from .models import Invoice

from profile_settings.models import ProfileSettings
from common.mixins import FormViewW3Mixin


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
            return redirect(redirect_to)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ChangeInvoiceMixin(FormViewW3Mixin):
    model = Invoice
    template_name = 'common/form.html'
    fields = ['your_full_name', 'your_address', 'customer_address', 'invoice_number', 'invoice_date',
              'invoice_period_begin', 'invoice_period_end', 'email', 'turnover_tax_number',
              'bank_name', 'iban', 'bic']
    success_url = reverse_lazy('invoice:list')

    def get_object(self, queryset=None):
        report_pk = int(self.kwargs['report_pk'])
        report = MonthReport.objects.select_related('customer').get(pk=report_pk)
        return self.get_queryset().get(month_report=report)


class InvoiceDeleteView(ChangeInvoiceMixin, DeleteView):
    template_name = 'common/confirm_delete.html'


class InvoiceUpdateView(ChangeInvoiceMixin, UpdateView):
    template_name = 'common/form.html'


class InvoiceCreateView(ChangeInvoiceMixin, CreateView):
    def get_success_url(self):
        report_pk = int(self.kwargs['report_pk'])
        report = MonthReport.objects.select_related('customer').get(pk=report_pk)
        return reverse_lazy('reports:year_report', kwargs={'year': report.year, 'customer': report.customer.id})

    def form_valid(self, form):
        settings = ProfileSettings.get_solo()
        if not settings.email:
            settings.email = form.cleaned_data['email']
        if not settings.address:
            settings.address = form.cleaned_data['your_address']
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
        form.instance.month_report_id = int(self.kwargs['report_pk'])
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()

        settings = ProfileSettings.get_solo()
        initial['your_full_name'] = settings.full_name
        initial['email'] = settings.email
        initial['your_address'] = settings.address
        initial['turnover_tax_number'] = settings.turnover_tax_number
        initial['bank_name'] = settings.bank_name
        initial['iban'] = settings.iban
        initial['bic'] = settings.bic

        report_pk = int(self.kwargs['report_pk'])
        report = MonthReport.objects.select_related('customer').get(pk=report_pk)
        customer = report.customer

        initial['customer_address'] = customer.invoice_address
        month = f'0{report.month}' if report.month < 10 else report.month
        initial['invoice_number'] = f'{customer.customer_id}-{report.year}-{month}'
        initial['invoice_date'] = date.today()
        last_month = date(year=report.year, month=report.month, day=1)
        initial['invoice_period_begin'] = last_month
        last_day = calendar.monthrange(report.year, report.month)[1]
        initial['invoice_period_end'] = last_month.replace(day=last_day)
        return initial
