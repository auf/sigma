from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.references.models import Etablissement

urlpatterns = patterns('',
            (r'^json/(?P<etablissement_id>\d+)/$', 'sigma.www.views.etablissement.json'),           
)
