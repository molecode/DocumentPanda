import csv
import datetime
from io import TextIOWrapper
from functools import reduce

from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import ListView, RedirectView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

from customer.models import Customer
from customer.views import FormViewW3Mixin

from .models import MonthReport, YearReport
from .forms import FixedPriceMonthReportForm, FeeMonthReportForm
from tax.models import Tax
from common.forms import UploadForm


class ReportsRedirectView(RedirectView):
    """
    Redirects to the year with the latest reports.
    Normally this should be the current year.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        last_report = MonthReport.objects.first()
        last_year = last_report.year if last_report else timezone.now().year
        return reverse_lazy('reports:year_report', kwargs={'year': last_year})


class DashboardView(TemplateView):
    """
    Show a overview of accumulated reports
    """
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        first_year = int(self.request.GET.get("from", 0))
        last_year = int(self.request.GET.get("to", 0))
        year_reports = []
        tax_reports = []
        average_reports_value = 0
        average_reports_hours_value = 0
        average_income_value = 0
        average_profit_value = 0

        try:
            if not first_year:
                first_year = MonthReport.objects.last().year
            if not last_year:
                last_year = MonthReport.objects.first().year

            total_first_year = MonthReport.objects.last().year
            total_last_year = MonthReport.objects.first().year
            context['total_first_year'] = total_first_year
            context['total_last_year'] = total_last_year
            context['total_years'] = [year for year in range(total_first_year, total_last_year + 1)]

            if first_year <= last_year:
                for year in range(first_year, last_year + 1):
                    month_reports = MonthReport.objects.filter(year=year)
                    year_report = YearReport(year, month_reports)
                    year_reports.append(year_report)

                    tax_report = Tax.objects.filter(year=year)
                    if tax_report:
                        tax_reports.append(tax_report[0])
                    else:
                        tax_reports.append(0)

                for report in year_reports:
                    average_reports_value += report.brutto
                    # Magic number 209: These are the average working days per year.
                    # 365 days of a year minus weekends and holiday days
                    # minus 30 vacations days minus 14 sick days
                    average_reports_hours_value += report.hours / 209
                average_reports_value = average_reports_value / len(year_reports)
                average_reports_hours_value = average_reports_hours_value / len(year_reports)

                for report in tax_reports:
                    if isinstance(report, Tax):
                        average_income_value += report.income
                        average_profit_value += report.get_profit()
                    else:
                        average_income_value += report
                        average_profit_value += report
                average_income_value = average_income_value / len(tax_reports)
                average_profit_value = average_profit_value / len(tax_reports)
            else:
                messages.error(self.request, "'from' cannot be bigger than 'to' value.")
        except AttributeError as error:
            pass

        context['average_income'] = [float(round(average_income_value, 2))] * len(tax_reports)
        context['average_profit'] = [float(round(average_profit_value, 2))] * len(tax_reports)
        context['average_reports'] = [float(round(average_reports_value, 2))] * len(year_reports)
        context['average_reports_hours'] = round(average_reports_hours_value, 2)
        context['year_reports'] = year_reports
        context['tax_reports'] = tax_reports

        return context


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


class ReportExportCSV(View):
    """
    Export the given reports as csv.
    """
    def get(self, *args, **kwargs):
        month_reports = MonthReport.objects.select_related('customer')
        file_name = 'document_panda_reports'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)

        writer = csv.writer(response)
        writer.writerow(['customer', 'month', 'year', 'hours', 'fee'])
        for month_report in month_reports:
            writer.writerow([month_report.customer.customer_id, month_report.month, month_report.year, month_report.hours, month_report.fee])

        return response


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
    template_name = 'common/form.html'

    def get_success_url(self):
        return reverse_lazy('reports:year_report', kwargs={'year': self.object.year, 'customer': self.object.customer.id})


class FeeReportsCreateView(ChangeReportMixin, CreateView):
    form_class = FeeMonthReportForm

    def get_initial(self):
        return {'month': datetime.datetime.now().month,
                'year': datetime.datetime.now().year}


class FixedPriceReportsCreateView(ChangeReportMixin, CreateView):
    form_class = FixedPriceMonthReportForm

    def get_initial(self):
        return {'month': datetime.datetime.now().month,
                'year': datetime.datetime.now().year}


class FeeReportsUpdateView(ChangeReportMixin, UpdateView):
    form_class = FeeMonthReportForm


class FixedPriceReportsUpdateView(ChangeReportMixin, UpdateView):
    form_class = FixedPriceMonthReportForm


class ReportsDeleteView(ChangeReportMixin, DeleteView):
    template_name = 'common/confirm_delete.html'
    model = MonthReport
    fields = ['customer', 'month', 'year', 'fixed_price', 'vat_percent']