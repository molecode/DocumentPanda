from django import forms
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Customer


class CustomerListView(ListView):
    model = Customer


class CustomerDetailView(DetailView):
    model = Customer


class FormViewW3Mixin(object):
    def get_form(self, form_class=None):
        form = super(FormViewW3Mixin, self).get_form(form_class)
        for _, form_field in form.fields.items():
            form_field.widget.attrs = {'class': 'w3-input'}
        return form


class CustomerCreateView(FormViewW3Mixin, CreateView):
    model = Customer
    template_name = 'common/form.html'
    fields = ['name', 'customer_id', 'default_fee']
    success_url = reverse_lazy('customer:list')


class CustomerUpdateView(FormViewW3Mixin, UpdateView):
    model = Customer
    template_name = 'common/form.html'
    fields = ['name', 'customer_id', 'default_fee']
    success_url = reverse_lazy('customer:list')


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('customer:list')
