from django.conf.urls import url

from . import views

app_name = 'profile_settings'
urlpatterns = [
    url(r'^$', views.ProfileSettingsUpdateView.as_view(), name='index'),
]