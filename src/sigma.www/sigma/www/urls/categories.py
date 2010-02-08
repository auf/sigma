from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import Categorie

urlpatterns = patterns('',
            (r'^$', 'sigma.www.views.categorie.liste'),
            (r'^detail/(?P<object_id>\d+)/$', 'sigma.www.views.categorie.detail'),
            (r'^export/(?P<object_id>\d+)/$', 'sigma.www.views.categorie.export'),
            (r'^json/(?P<object_id>\d+)/$', 'sigma.www.views.categorie.json'),                     
            (r'^json/$', 'sigma.www.views.categorie.json'),
            (r'^(?P<criteria>[a-zA-Z_]+)/(?P<value>[0-9a-zA-Z]+)/$', 'sigma.www.views.categorie.liste')
)
