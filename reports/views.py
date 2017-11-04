from decimal import Decimal
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from customer.models import Customer

from .models import MonthReport


class ReportsRedirectview(RedirectView):
    """
    Redirects to the year with the latest reports.
    Normally this should be the current year.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        last_report = MonthReport.get_last_report()
        last_year = last_report.year if last_report else timezone.now().year
        return reverse_lazy('reports:year_report', kwargs={'year': last_year})


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
        if 'customer' in self.kwargs:
            context['current_customer'] = Customer.objects.get(id=self.kwargs['customer'])

        # create year report
        context['year_report'] = YearReport(self.kwargs['year'], self.object_list)

        return context


class ChangeReportMixin(object):
    """Mixin for every modify ReportView: create, update, delete."""
    model = MonthReport
    fields = ['customer', 'month', 'year', 'hours', 'fee']

    def get_success_url(self):
        return reverse_lazy('reports:year_report', kwargs={'year': self.object.year})


class ReportsCreateView(ChangeReportMixin, CreateView):
    template_name = 'common/form.html'


class ReportsUpdateView(ChangeReportMixin, UpdateView):
    template_name = 'common/form.html'


class ReportsDeleteView(ChangeReportMixin, DeleteView):
    template_name = 'common/confirm_delete.html'


class YearReport:
    """
    This class represents a report for one year. It holds the summed up month and quarter values
    and also the total amount.
    """
    def __init__(self, year, month_queryset):
        self.year = year
        self.months = self.create_months_from_queryset(month_queryset)
        self.quarters = self.create_quarters()
        self.netto, self.brutto, self.vat, self.fee, self.hours = self.calculate_values()

    def create_months_from_queryset(self, month_queryset):
        months = {i: MonthReport(month=i, year=self.year, hours=0, fee=Decimal(0.00)) for i in range(1, 13)}
        for month_report in month_queryset:
            months[month_report.month] += month_report
        return [y for x, y in months.items()]

    def calculate_values(self):
        netto = brutto = vat = fee = hours = Decimal(0.00)
        for quarter in self.quarters:
            netto += quarter.netto
            brutto += quarter.brutto
            vat += quarter.vat
            fee += quarter.fee if quarter.fee else Decimal(0.00)
            hours += quarter.hours
        return netto, brutto, vat, round(fee/12, 2), hours

    def create_quarters(self):
        quarters = []
        for i in range(1, 5):
            quarters.append(self.Quarter(i, self.months))
        return quarters

    class Quarter:
        """
        This class represents a quarter of the year with all needed summed amounts.
        """
        def __init__(self, quarter_number, months):
            if quarter_number < 1 or quarter_number > 4:
                raise
            self.quarter_number = quarter_number
            self.months = self.filter_quarter(months)
            self.netto, self.brutto, self.vat, self.fee, self.hours = self.calculate_values()

        def filter_quarter(self, months):
            return months[3*self.quarter_number-3:3*self.quarter_number]

        def calculate_values(self):
            netto = Decimal(0.00)
            brutto = Decimal(0.00)
            vat = Decimal(0.00)
            fee = Decimal(0.00)
            hours = Decimal(0.00)
            for month in self.months:
                netto += month.netto
                brutto += month.brutto
                vat += month.vat
                fee += month.fee if month.fee else Decimal(0.00)
                hours += month.hours
            return netto, brutto, vat, round(fee/3, 2), hours

        def __str__(self):
            return '{}. {}'.format(self.quarter_number, _('Quarter'))
