from django.conf.urls import url

from . import views

app_name = 'invoice'
urlpatterns = [
    url(r'(?P<report_pk>[0-9]+)/$', views.InvoiceDetailView.as_view(), name='detail'),
    url(r'(?P<report_pk>[0-9]+)/add/$', views.InvoiceCreateView.as_view(), name='add'),
]
