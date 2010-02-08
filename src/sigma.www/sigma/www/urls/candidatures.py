from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import Candidature

urlpatterns = patterns('',
            # Listing general
            (r'^$', 'sigma.www.views.candidature.liste'),

            # Ajout d'une candidature ou modification d'une candidature incomplete
            (r'^add/(?P<appel_id>\d+)/$', 'sigma.www.views.candidature.add'),
            (r'^add/(?P<appel_id>\d+)/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.add'),

            # Sauvegarde et validation d'un ajout
            (r'^save/(?P<appel_id>\d+)/$', 'sigma.www.views.candidature.save'),
            (r'^validate/(?P<appel_id>\d+)/$', 'sigma.www.views.candidature.validate'),

            # Sauvegarde et validation d'une modification
            (r'^save/(?P<appel_id>\d+)/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.save'),
            (r'^validate/(?P<appel_id>\d+)/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.validate'),
           
            (r'^edit/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.edit'),
            (r'^detail/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.detail'),

            # Gestion du statut d'une candidature
            (r'^delete/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.delete'),            
            (r'^undo/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.undo'),
            (r'^statut/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.edit_statut'),
                       
            # Obtention de donnes pour les requetes ajax
            (r'^json/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.json'),
            (r'^json/field_dependencies/$', 'sigma.www.views.candidature.json_field_dependencies'), 
            (r'^json/warning_messages/(?P<object_id>\d+)/(?P<action>[a-zA-Z]+)/$', 'sigma.www.views.candidature.json_warning_messages'),
            (r'^json/$', 'sigma.www.views.candidature.json'),
                       
            # Gestion de l'exportation
            (r'^lettretype/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.lettretype'),
            (r'^export/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.export'),
            (r'^export/$', 'sigma.www.views.candidature.export'),           
            (r'^export_search/(?P<value>[0-9a-zA-Z]+)/$', 'sigma.www.views.candidature.export_search'),

            # Gestion des objets lies
            (r'^expert/delete/(?P<object_id>\d+)/(?P<candidature_expert_id>\d+)/$', 'sigma.www.views.candidature.delete_expert'),
            (r'^expert/add/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.add_expert'),
            (r'^expert/note/(?P<object_id>\d+)/(?P<candidature_expert_id>\d+)/$', 'sigma.www.views.candidature.noter'),
            (r'^pieces/(?P<object_id>\d+)/$', 'sigma.www.views.candidature.piece'),

            # Recherche
            (r'^(?P<criteria>[a-zA-Z]+)/(?P<value>[0-9a-zA-Z]+)/$', 'sigma.www.views.candidature.liste'),
)
