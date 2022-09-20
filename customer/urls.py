from django.urls import re_path

from . import views

app_name = 'customer'
urlpatterns = [
    re_path(r'add/$', views.CustomerCreateView.as_view(), name='add'),
    re_path(r'(?P<pk>[0-9]+)/update/$', views.CustomerUpdateView.as_view(), name='update'),
    re_path(r'(?P<pk>[0-9]+)/delete/$', views.CustomerDeleteView.as_view(), name='delete'),
    re_path(r'import/$', views.CustomerImportView.as_view(), name='import'),
    re_path(r'export/$', views.CustomerExportCSV.as_view(), name='export'),
    re_path(r'^$', views.CustomerListView.as_view(), name='list'),
]
