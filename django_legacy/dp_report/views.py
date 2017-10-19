from datetime import datetime
from decimal import Decimal
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from dp_customer.models import Customer

from .models import MonthReport


class YearListView(ListView):
    model = MonthReport
    template_name = 'report/year_list.html'

    def get_queryset(self):
        return MonthReport.objects.filter(customer__customer_id=int(self.kwargs['customer_id'])).filter(year=int(self.kwargs['year']))

    def get_context_data(self, **kwargs):
        context = super(YearListView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(customer_id=self.kwargs['customer_id'])
        context['year'] = YearReport(customer, self.kwargs['year'], context['object_list'])
        return context


class YearTotalListView(ListView):
    model = MonthReport
    context_object_name = 'months'
    template_name = 'report/year_total_list.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = int(kwargs.get('year')) if 'year' in kwargs else datetime.now().year

    def get_queryset(self):
        return MonthReport.objects.filter(year=self.year)

    def get_context_data(self, **kwargs):
        context = super(YearTotalListView, self).get_context_data(**kwargs)
        context['year'] = self.year
        return context


class YearReport:
    def __init__(self, customer, year, month_queryset):
        self.customer = customer
        self.year = year
        self.months = self.create_months_from_queryset(month_queryset)
        self.quarters = self.create_quarters()
        self.netto, self.brutto, self.umsatzsteuer, self.fee, self.hours = self.calculate_values()

    def create_months_from_queryset(self, month_queryset):
        months = {i: MonthReport(customer=self.customer, month=i, year=self.year, hours=0) for i in range(1, 13)}
        for month_report in month_queryset:
            months[month_report.month] = month_report
        return [y for x,y in months.items()]

    def calculate_values(self):
        netto = brutto = umsatzsteuer = fee = hours = Decimal(0.00)
        for quarter in self.quarters:
            netto += quarter.netto
            brutto += quarter.brutto
            umsatzsteuer += quarter.umsatzsteuer
            fee += quarter.fee if quarter.fee else Decimal(0.00)
            hours += quarter.hours
        return netto, brutto, umsatzsteuer, round(fee/12, 2), hours

    def create_quarters(self):
        quarters = []
        for i in range(1, 5):
            quarters.append(self.Quarter(i, self.months))
        return quarters

    class Quarter:
        def __init__(self, quarter_number, months):
            if quarter_number < 1 or quarter_number > 4:
                raise
            self.quarter_number = quarter_number
            self.months = self.filter_quarter(months)
            self.netto, self.brutto, self.umsatzsteuer, self.fee, self.hours = self.calculate_values()

        def filter_quarter(self, months):
            return months[3*self.quarter_number-3:3*self.quarter_number]

        def calculate_values(self):
            netto = Decimal(0.00)
            brutto = Decimal(0.00)
            umsatzsteuer = Decimal(0.00)
            fee = Decimal(0.00)
            hours = Decimal(0.00)
            for month in self.months:
                netto += month.netto
                brutto += month.brutto
                umsatzsteuer += month.umsatzsteuer
                fee += month.fee if month.fee else Decimal(0.00)
                hours += month.hours
            return netto, brutto, umsatzsteuer, round(fee/3, 2), hours

        def __str__(self):
            return '{}. {}'.format(self.quarter_number, _('Quarter'))