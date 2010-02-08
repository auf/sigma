from django.conf.urls.defaults import *

urlpatterns = patterns('',
           (r'^$', 'sigma.www.views.general.index'),

)
