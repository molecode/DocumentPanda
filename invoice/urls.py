from django.urls import re_path

from . import views

app_name = 'invoice'
urlpatterns = [
    re_path(r'(?P<report_pk>[0-9]+)/$', views.InvoiceDetailView.as_view(), name='detail'),
    re_path(r'(?P<report_pk>[0-9]+)/download$', views.download, name='download'),
    re_path(r'(?P<report_pk>[0-9]+)/preview$', views.preview, name='preview'),
    re_path(r'(?P<report_pk>[0-9]+)/add/$', views.InvoiceCreateView.as_view(), name='add'),
    re_path(r'(?P<report_pk>[0-9]+)/update/$', views.InvoiceUpdateView.as_view(), name='update'),
    re_path(r'(?P<report_pk>[0-9]+)/delete/$', views.InvoiceDeleteView.as_view(), name='delete'),
    re_path(r'$', views.InvoiceListView.as_view(), name='list'),
]
