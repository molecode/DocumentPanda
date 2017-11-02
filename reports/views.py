from django.utils import timezone
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
        context['years'] = sorted(set(MonthReport.objects.values_list('year', flat=True)), reverse=True)
        # Get a list of all customer of this year
        year = self.kwargs.get('year')
        customers = MonthReport.objects.select_related('customer').filter(year=year)
        customers = customers.values('customer__id', 'customer__name')
        # Eliminate duplicates
        context['customers'] = list({customer['customer__id']: customer for customer in customers}.values())
        if 'customer' in self.kwargs:
            context['current_customer'] = Customer.objects.get(id=self.kwargs['customer'])
        return context


class ChangeReportMixin(object):
    """Mixin for every Report which is been modified: create, update, delete."""
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
