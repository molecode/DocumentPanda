from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Customer


class CustomerListView(ListView):
    model = Customer


class CustomerDetailView(DetailView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'common/form.html'
    fields = ['name', 'customer_id', 'default_fee', 'active']
    success_url = reverse_lazy('customer:list')


class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'common/form.html'
    fields = ['name', 'customer_id', 'default_fee', 'active']
    success_url = reverse_lazy('customer:list')


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('customer:list')
