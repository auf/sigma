# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('suivi.views',
    url(r'^admin/suivi/(\d+)/$', 'suivi', name='suivi'),
)