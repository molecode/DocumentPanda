from django.urls import re_path

from . import views

app_name = 'tax'
urlpatterns = [
    re_path(r'add/$', views.TaxCreateView.as_view(), name='add'),
    re_path(r'(?P<pk>[0-9]+)/update/$', views.TaxUpdateView.as_view(), name='update'),
    re_path(r'(?P<pk>[0-9]+)/delete/$', views.TaxDeleteView.as_view(), name='delete'),
    re_path(r'(?P<pk>[0-9]+)/$', views.TaxDetailView.as_view(), name='detail'),
    re_path(r'import/$', views.TaxImportView.as_view(), name='import'),
    re_path(r'export/$', views.TaxExportCSV.as_view(), name='export'),
    re_path(r'^$', views.TaxListView.as_view(), name='index'),
]
