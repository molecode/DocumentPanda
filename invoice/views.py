import calendar
from datetime import date

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from reports.models import MonthReport
from .models import Invoice

from common.mixins import FormViewW3Mixin


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


class InvoiceCreateView(FormViewW3Mixin, CreateView):
    model = Invoice
    template_name = 'common/form.html'
    fields = ['my_address', 'customer_address', 'invoice_number', 'invoice_date',
              'invoice_period_begin', 'invoice_period_end', 'email', 'turnover_tax_number', 'bank_account']

    def get_initial(self):
        initial = super().get_initial()

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
