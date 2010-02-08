from django.conf.urls.defaults import *
from django.views.generic import list_detail
from sigma.www.models import Note

urlpatterns = patterns('',
	    (r'detail/(?P<object_id>\d+)/$', 'sigma.www.views.note.detail'),
            (r'^edit/(?P<object_id>\d+)/$', 'sigma.www.views.note.edit'),
)
