from django import forms
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Customer
from .forms import CustomerForm


class CustomerListView(ListView):
    model = Customer


class CustomerDetailView(DetailView):
    model = Customer


class FormViewW3Mixin(object):
    def get_form(self, form_class=None):
        form = super(FormViewW3Mixin, self).get_form(form_class)
        for _, form_field in form.fields.items():
            form_field.widget.attrs = {'class': 'w3-input w3-border'}
        return form


class ChangeCustomerMixin(FormViewW3Mixin):
    """Mixin for every modifing CustomerView: create, update, delete."""
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer:list')


class CustomerCreateView(ChangeCustomerMixin, CreateView):
    template_name = 'common/form.html'


class CustomerUpdateView(ChangeCustomerMixin, UpdateView):
    template_name = 'common/form.html'


class CustomerDeleteView(ChangeCustomerMixin, DeleteView):
    template_name = 'common/confirm_delete.html'
