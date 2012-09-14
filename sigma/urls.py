# -*- encoding: utf-8 -*
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import handler500, handler404  # NOQA
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include(admin.site.urls)),
    url(r'^candidatures/', include('sigma.candidatures.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^wcs/', include('sigma.wcs.urls')),
)
