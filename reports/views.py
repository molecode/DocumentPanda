import csv
from decimal import Decimal
from io import TextIOWrapper

from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

from customer.models import Customer
from customer.views import FormViewW3Mixin

from .models import MonthReport, CurrencyMixin, YearReport
from .forms import UploadForm


class ReportsRedirectView(RedirectView):
    """
    Redirects to the year with the latest reports.
    Normally this should be the current year.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        last_report = MonthReport.get_last_report()
        last_year = last_report.year if last_report else timezone.now().year
        return reverse_lazy('reports:year_report', kwargs={'year': last_year})


class ReportImportView(SuccessMessageMixin, FormView):
    template_name = 'reports/import_reports.html'
    form_class = UploadForm
    success_url = reverse_lazy('reports:index')

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
                customer = Customer.objects.get(customer_id=row['customer'])
                month = row['month']
                year = row['year']
                hours = row['hours']
                fee = row['fee']
                month_report = MonthReport(customer=customer, month=month, year=year, hours=hours, fee=fee)
                month_report.save()
                success_counter += 1
            except IntegrityError:
                warnings.append('{} {} {}/{} (line: {})'.format(customer.name,
                                                                _('has an existing report for'),
                                                                row['month'],
                                                                row['year'],
                                                                csv_file.line_num))
            except Customer.DoesNotExist:
                errors.append('{} {} (line: {})'.format(_('There is no customer with ID'),
                                                        row['customer'],
                                                        csv_file.line_num))
        if success_counter > 0:
            messages.success(self.request, _('{} of {} report(s) successfully imported.<br />'.format(success_counter,
                                                                                                total_counter)))
        if warnings:
            messages.warning(self.request, self.get_html_list(warnings))
        if errors:
            messages.error(self.request, self.get_html_list(errors))
        return super(ReportImportView, self).form_valid(form)

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

# class ExportCSV(View):
#     """
#     Export the given reports as csv.
#     """
#     def get(self, *args, **kwargs):
#         reports = MonthReport.objects.select_related('customer').filter(year=self.kwargs['year'])
#         file_name = '{}_{}'.format(kwargs['year'], _('Yearreport'))
#
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)
#
#         writer = csv.writer(response)
#         writer.writerow([_('Month'), _('Netto'), _('Brutto'), _('VAT'), _('Hourly Rate'),
#                          _('Hours per Month'), _('Hours per Week')])
#         year_report = YearReport(self.kwargs['year'], reports)
#         for month in year_report.months:
#             writer.writerow([month.get_month_display(), month.netto, month.brutto,
#                              month.vat, month.fee, month.hours, month.hours_per_week()])
#
#         return response


class ReportsListView(ListView):
    """
    Create a report for the year, either for one customer or total for all customers.
    """
    model = MonthReport
    template_name = 'reports/year_report.html'

    def get_queryset(self, *args, **kwargs):
        reports = MonthReport.objects.select_related('customer')
        if 'customer' in self.kwargs:
            reports = reports.filter(customer=self.kwargs['customer'])
        return reports.filter(year=self.kwargs.get('year'))

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)

        # Using set() here because distinct isn't working with sqlite
        years = sorted(set(MonthReport.objects.values_list('year', flat=True)), reverse=True)
        context['years'] = map(str, years)

        # Get a list of all customer of this year
        year = self.kwargs['year']
        customers = MonthReport.objects.select_related('customer').filter(year=year)
        customers = customers.values('customer__id', 'customer__name')

        # Eliminate duplicates
        context['customers'] = list({customer['customer__id']: customer for customer in customers}.values())

        # Get current customer if there is one
        customer = None
        if 'customer' in self.kwargs:
            customer = Customer.objects.get(id=self.kwargs['customer'])
            context['current_customer'] = customer

        # create year report
        context['year_report'] = YearReport(self.kwargs['year'], self.object_list, customer=customer)

        return context


class ChangeReportMixin(FormViewW3Mixin):
    """Mixin for every modify ReportView: create, update, delete."""
    model = MonthReport
    fields = ['customer', 'month', 'year', 'hours', 'fee']

    def get_success_url(self):
        return reverse_lazy('reports:year_report', kwargs={'year': self.object.year, 'customer': self.object.customer.id})


class ReportsCreateView(ChangeReportMixin, CreateView):
    template_name = 'common/form.html'


class ReportsUpdateView(ChangeReportMixin, UpdateView):
    template_name = 'common/form.html'


class ReportsDeleteView(ChangeReportMixin, DeleteView):
    template_name = 'common/confirm_delete.html'
