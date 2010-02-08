from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import ChampsCategorie

urlpatterns = patterns('',
           (r'^blocs/json/(?P<projet_id>\d+)/$', 'sigma.www.views.blocs.blocs_json'),
)
