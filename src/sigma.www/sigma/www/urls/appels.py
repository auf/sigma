from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import Appel

urlpatterns = patterns('',
           # Listing general
           (r'^$', 'sigma.www.views.appel.liste'),

           # Ajout d'un appel d'offre
           (r'^add/$', 'sigma.www.views.appel.add'),

           # Edition d'un appel d'offre
           (r'^edit/(?P<object_id>\d+)/$', 'sigma.www.views.appel.edit'),

           # Affichage complet d'un appel d'offre
           (r'^detail/(?P<object_id>\d+)/$', 'sigma.www.views.appel.detail'),

           # Gestion du statut d'un appel d'offre
           (r'^statut/(?P<object_id>\d+)/$', 'sigma.www.views.appel.edit_statut'),
           (r'^delete/(?P<object_id>\d+)/$', 'sigma.www.views.appel.delete'),

           # Obtention de donnees pour les requetes ajax
           (r'^json/(?P<object_id>\d+)/$', 'sigma.www.views.appel.json'),                    
           (r'^json/field_dependencies/$', 'sigma.www.views.appel.json_field_dependencies'), 
           (r'^json/$', 'sigma.www.views.appel.json'),

           # Expertation de donnees 
           (r'^export/(?P<object_id>\d+)/$', 'sigma.www.views.appel.export'),
           (r'^export/(?P<statut>\S+)/$', 'sigma.www.views.appel.export'),
           (r'^export/$', 'sigma.www.views.appel.export'),        
    
           (r'^export_can/(?P<object_id>\d+)/(?P<statut>\S+)/$', 'sigma.www.views.appel.export_can'),
           (r'^export_can/(?P<object_id>\d+)/$', 'sigma.www.views.appel.export_can'),

           (r'^export_lettres/(?P<object_id>\d+)/(?P<statut>\S+)/$', 'sigma.www.views.appel.export_lettres'),
           (r'^export_lettres/(?P<object_id>\d+)/$', 'sigma.www.views.appel.export_lettres'),            

           # Gestion des objets lies
           (r'^criteria/$', 'sigma.www.views.appel.criteria'),

           # Recherche
           (r'^(?P<criteria>[a-zA-Z_]+)/(?P<value>[0-9a-zA-Z]+)/$', 'sigma.www.views.appel.liste'),
)
