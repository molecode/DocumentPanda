from django.conf.urls import url

from . import views

app_name = 'reports'
urlpatterns = [
    url(r'add/fee$', views.FeeReportsCreateView.as_view(), name='add_fee'),
    url(r'add/fix$', views.FixedPriceReportsCreateView.as_view(), name='add_fix'),
    url(r'(?P<pk>[0-9]+)/update/fee$', views.FeeReportsUpdateView.as_view(), name='update_fee'),
    url(r'(?P<pk>[0-9]+)/update/fix$', views.FixedPriceReportsUpdateView.as_view(), name='update_fix'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.ReportsDeleteView.as_view(), name='delete'),
    url(r'year/(?P<year>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'year/(?P<year>[0-9]+)/(?P<customer>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'import/$', views.ReportImportView.as_view(), name='import'),
    url(r'export/$', views.ReportExportCSV.as_view(), name='export'),
    url(r'^$', views.ReportsRedirectView.as_view(), name='index'),
]

