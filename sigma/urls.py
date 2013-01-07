# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import handler500, handler404  # NOQA
from django.views.generic.simple import direct_to_template

from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^candidatures/', include('sigma.candidatures.urls')),
    # url(r'^boursiers/', include('sigma.boursiers.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^wcs/', include('sigma.wcs.urls')),
    (r'^search/', 'sigma.search.views.basic_search'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$',  direct_to_template, {
            'template': '500.html',
            }),
        url(r'^404/$',  direct_to_template, {
            'template': '404.html',
            }),
    )
    
urlpatterns += patterns(
    '',
    url(r'^', include(admin.site.urls)),
)
