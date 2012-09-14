# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sigma.candidatures.views',
    url(r'^mes-disciplines/$', 'mes_disciplines', name='mes_disciplines'),
    url(r'^evaluer/(\d+)/$', 'evaluer', name='evaluer'),
    url(r'^supprimer-mon-commentaire/(\d+)/$', 'supprimer_mon_commentaire', name='supprimer_mon_commentaire'),
    url(r'^affecter-experts-dossiers/$', 'affecter_experts_dossiers', name='affecter_experts_dossiers')
)
