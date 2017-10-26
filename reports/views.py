from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import MonthReport


class ReportsListView(ListView):
    model = MonthReport

    def get_queryset(self, *args, **kwargs):
        reports = MonthReport.objects.select_related('customer')
        year = self.kwargs.get('year', None)
        if year:
            return reports.filter(year=year)
        return reports

class ReportsDetailView(DetailView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')


class ReportsCreateView(CreateView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')
    template_name = 'common/form.html'
    fields = ['customer', 'month', 'year', 'hours', 'fee']
    success_url = reverse_lazy('reports:list')


class ReportsUpdateView(UpdateView):
    model = MonthReport
    template_name = 'common/form.html'
    fields = ['customer', 'month', 'year', 'hours', 'fee']
    success_url = reverse_lazy('reports:list')


class ReportsDeleteView(DeleteView):
    model = MonthReport
    queryset = MonthReport.objects.select_related('customer')
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('reports:list')