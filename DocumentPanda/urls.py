"""DocumentPanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView, TemplateView
from reports.views import DashboardView

urlpatterns = [
    url(r'^customer/', include('customer.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^tax/', include('tax.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^$', RedirectView.as_view(url='dashboard'), name='index'),
]

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    ] + urlpatterns
