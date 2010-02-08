from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import ChampsCategorie

urlpatterns = patterns('',
           (r'^bloc/json/(?P<bloc_id>\d+)/$', 'sigma.www.views.champs.champs_json'),
           (r'^appel/json/(?P<bloc_id>\d+)/$', 'sigma.www.views.champs.champs_appel_json'),
)
