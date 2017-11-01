from django.utils import timezone
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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

    def get_queryset(self, *args, **kwargs):
        reports = MonthReport.objects.select_related('customer')
        last_report = MonthReport.get_last_report()
        last_year = last_report.year if last_report else timezone.now().year
        year = self.kwargs.get('year', last_year)
        return reports.filter(year=year)

    def get_context_data(self, **kwargs):
        context = super(ReportsListView, self).get_context_data(**kwargs)
        context['years'] = sorted(set(MonthReport.objects.values_list('year', flat=True)), reverse=True)
        return context


class ReportsDetailView(DetailView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')


class ReportsCreateView(CreateView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')
    template_name = 'common/form.html'
    fields = ['customer', 'month', 'year', 'hours', 'fee']
    success_url = reverse_lazy('reports:index')


class ReportsUpdateView(UpdateView):
    model = MonthReport
    template_name = 'common/form.html'
    fields = ['customer', 'month', 'year', 'hours', 'fee']
    success_url = reverse_lazy('reports:index')


class ReportsDeleteView(DeleteView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('reports:index')
