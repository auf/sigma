# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sigma.views',
    url(r'^admin/mes-disciplines/$', 'mes_disciplines', name='mes_disciplines'),
)
