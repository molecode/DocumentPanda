from django.conf.urls import url

from . import views

app_name = 'invoice'
urlpatterns = [
    url(r'(?P<report_pk>[0-9]+)/$', views.InvoiceDetailView.as_view(), name='detail'),
    url(r'(?P<report_pk>[0-9]+)/download$', views.download, name='download'),
    url(r'(?P<report_pk>[0-9]+)/preview$', views.preview, name='preview'),
    url(r'(?P<report_pk>[0-9]+)/add/$', views.InvoiceCreateView.as_view(), name='add'),
    url(r'(?P<report_pk>[0-9]+)/update/$', views.InvoiceUpdateView.as_view(), name='update'),
    url(r'(?P<report_pk>[0-9]+)/delete/$', views.InvoiceDeleteView.as_view(), name='delete'),
    url(r'$', views.InvoiceListView.as_view(), name='list'),
]
