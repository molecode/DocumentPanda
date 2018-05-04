from django.conf.urls import url

from . import views

app_name = 'reports'
urlpatterns = [
    url(r'add/$', views.ReportsCreateView.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.ReportsUpdateView.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.ReportsDeleteView.as_view(), name='delete'),
    url(r'(?P<year>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'(?P<year>[0-9]+)/(?P<customer>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'import/$', views.ReportImportView.as_view(), name='import'),
    url(r'export/$', views.ReportExportCSV.as_view(), name='export'),
    url(r'^$', views.ReportsRedirectView.as_view(), name='index'),
]

