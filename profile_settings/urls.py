from django.urls import path

from . import views

app_name = 'profile_settings'
urlpatterns = [
    path(r'', views.ProfileSettingsUpdateView.as_view(), name='index'),
]