from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import Expert

urlpatterns = patterns('',
	    (r'^$', 'sigma.www.views.expert.liste'),
            (r'^add/$', 'sigma.www.views.expert.add'),
            (r'^edit/(?P<object_id>\d+)/$', 'sigma.www.views.expert.edit'),
            (r'^detail/(?P<object_id>\d+)/$', 'sigma.www.views.expert.detail'),
            (r'^export/(?P<object_id>\d+)/$', 'sigma.www.views.expert.export'),
            (r'^json/(?P<region_id>\d+)/(?P<discipline_id>\d+)/$', 'sigma.www.views.expert.json'),           
)
