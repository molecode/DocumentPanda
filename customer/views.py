import csv
from io import TextIOWrapper

from django import forms
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Customer
from .forms import CustomerForm, UploadForm


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


class CustomerImportView(SuccessMessageMixin, FormView):
    template_name = 'customer/import_customer.html'
    form_class = UploadForm
    success_url = reverse_lazy('customer:list')

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
                name = row['name']
                customer_id = row['customer_id']
                fee = row['fee']
                active = row['active']
                customer = Customer(name=name, customer_id=customer_id, default_fee=fee, active=active)
                customer.save()
                success_counter += 1
            except IntegrityError:
                warnings.append('{} {} ({}) (line: {})'.format(_('Customer exists:'),
                                                               customer.name,
                                                               customer.customer_id,
                                                               csv_file.line_num))
        if success_counter > 0:
            messages.success(self.request, _('{} of {} customer successfully imported.<br />'.format(success_counter,
                                                                                                total_counter)))
        if warnings:
            messages.warning(self.request, self.get_html_list(warnings))
        if errors:
            messages.error(self.request, self.get_html_list(errors))
        return super(CustomerImportView, self).form_valid(form)

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


class CustomerExportCSV(View):
    """
    Export customer as csv.
    """
    def get(self, *args, **kwargs):
        customer_set = Customer.objects.all()
        file_name = 'document_panda_customer'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)

        writer = csv.writer(response)
        writer.writerow(['name', 'customer_id', 'fee', 'active'])
        for customer in customer_set:
            writer.writerow([customer.name, customer.customer_id, customer.default_fee, customer.active])

        return response

