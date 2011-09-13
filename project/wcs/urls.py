# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('wcs.views',
    url(r'^admin/importer/(.*)/$', 'importer_dossiers', name='importer_dossiers'),
)
