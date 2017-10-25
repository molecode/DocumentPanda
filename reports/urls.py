from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add/$', views.ReportsCreateView.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.ReportsUpdateView.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.ReportsDeleteView.as_view(), name='delete'),
    url(r'(?P<pk>[0-9]+)/$', views.ReportsDetailView.as_view(), name='detail'),
    url(r'^$', views.ReportsListView.as_view(), name='list'),
]