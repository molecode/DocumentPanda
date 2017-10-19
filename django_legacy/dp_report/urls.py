from django.conf.urls import url

from dp_report import views

urlpatterns = [
    # url(r'^$', views.YearListView.as_view(), name='yearly_report_total'),
    url(r'^(?P<year>[\d]*)/$', views.YearTotalListView.as_view(), name='yearly_report_total'),
    url(r'^(?P<year>[\d]+)/(?P<customer_id>[\d]+)/$', views.YearListView.as_view(), name='yearly_report'),
]