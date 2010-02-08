from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import ProjetPoste

projet_postes_info = { 
    "queryset" : ProjetPoste.objects.all(),
    }

urlpatterns = patterns('',
           (r'^$', 'sigma.www.views.projet.list'),
           (r'^detail/(?P<object_id>\d+)/$', 'sigma.www.views.projet.detail'),
           (r'^categorie/json/(?P<object_id>\d+)/$', 'sigma.www.views.projet.categorie_json'),
           (r'^export/(?P<object_id>\d+)/$', 'sigma.www.views.projet.export'),   
           (r'^export/$', 'sigma.www.views.projet.export'),
           (r'^export_search/(?P<value>[0-9a-zA-Z]+)/$', 'sigma.www.views.projet.export_search'),                    
)
