from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from .models import ProfileSettings
from common.mixins import FormViewW3Mixin


class ChangeProfileSettingsMixin(FormViewW3Mixin):
    """Mixin for every modifing TaxView: create, update, delete."""
    model = ProfileSettings
    fields = ['full_name', 'street', 'city', 'email',
              'turnover_tax_number', 'bank_name',
              'iban', 'bic', 'currency']
    success_url = reverse_lazy('profile_settings:index')

    def form_valid(self, form):
        messages.success(self.request, _('Settings successfully saved.'))
        return super().form_valid(form)


class ProfileSettingsUpdateView(ChangeProfileSettingsMixin, UpdateView):
    template_name = 'common/form.html'

    def get_object(self, queryset=None):
        return self.model.get_solo()