# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sigma.views',
    url(r'^admin/mes-disciplines/$', 'mes_disciplines', name='mes_disciplines'),
    url(r'^admin/evaluer/(\d+)/$', 'evaluer', name='evaluer'),
    url(r'^admin/supprimer-ma-note/(\d+)/$', 'supprimer_ma_note', name='supprimer_ma_note'),
    url(r'^admin/supprimer-mon-commentaire/(\d+)/$', 'supprimer_mon_commentaire', name='supprimer_mon_commentaire'),
)
