from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add/$', views.ReportsCreateView.as_view(), name='add'),
    url(r'year/(?P<year>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'year/(?P<year>[0-9]+)/(?P<customer>[0-9]+)/$', views.ReportsListView.as_view(), name='year_report'),
    url(r'(?P<pk>[0-9]+)/update/$', views.ReportsUpdateView.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.ReportsDeleteView.as_view(), name='delete'),
    url(r'^$', views.ReportsRedirectview.as_view(), name='index'),
]
