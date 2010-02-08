from django.conf.urls.defaults import *

urlpatterns = patterns('',
           (r'^.*$', 'sigma.www.views.general.search'),
           (r'^(?P<search_type>[a-zA-Z]+)/(?P<criteria>[a-z]+)/(?P<value>[1-9]+)/$', 'sigma.www.views.general.search')
) 
