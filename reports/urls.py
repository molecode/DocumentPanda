from django.urls import re_path

from . import views

app_name = 'reports'
urlpatterns = [
    re_path(r'add/hours$', views.FeeReportsCreateView.as_view(), name='add_hours'),
    re_path(r'add/fix$', views.FixedPriceReportsCreateView.as_view(), name='add_fix'),
    re_path(r'(?P<pk>[0-9]+)/update/fee$', views.FeeReportsUpdateView.as_view(), name='update_fee'),
    re_path(r'(?P<pk>[0-9]+)/update/fix$', views.FixedPriceReportsUpdateView.as_view(), name='update_fix'),
    re_path(r'(?P<pk>[0-9]+)/delete/$', views.ReportsDeleteView.as_view(), name='delete'),
    re_path(r'year/(?P<year>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    re_path(r'year/(?P<year>[0-9]+)/(?P<customer>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    re_path(r'import/$', views.ReportImportView.as_view(), name='import'),
    re_path(r'export/$', views.ReportExportCSV.as_view(), name='export'),
    re_path(r'^$', views.ReportsRedirectView.as_view(), name='index'),
]

