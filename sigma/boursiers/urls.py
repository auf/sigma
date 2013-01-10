# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'sigma.boursiers.views',
    url(r'^desiste/$', 'desiste', name='desiste'),
    url(r'^undesiste/$', 'undesiste', name='undesiste'),
    )
