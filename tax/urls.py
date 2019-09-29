from django.conf.urls import url

from . import views

app_name = 'tax'
urlpatterns = [
    url(r'add/$', views.TaxCreateView.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.TaxUpdateView.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.TaxDeleteView.as_view(), name='delete'),
    url(r'(?P<pk>[0-9]+)/$', views.TaxDetailView.as_view(), name='detail'),
    url(r'import/$', views.TaxImportView.as_view(), name='import'),
    url(r'export/$', views.TaxExportCSV.as_view(), name='export'),
    url(r'^$', views.TaxListView.as_view(), name='index'),
]
