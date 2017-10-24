from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add/$', views.CustomerCreateView.as_view(), name='add'),
    url(r'(?P<pk>[0-9]+)/update/$', views.CustomerUpdateView.as_view(), name='update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.CustomerDeleteView.as_view(), name='delete'),
    url(r'(?P<pk>[0-9]+)/$', views.CustomerDetailView.as_view(), name='detail'),
    url(r'^$', views.CustomerListView.as_view(), name='list'),
]