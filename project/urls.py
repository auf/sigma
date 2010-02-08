
from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'packages': ('sigmaww', 'ajax_filtered_fields'),
}

handler500 = 'sigma.www.views.general.handler500'
handler404 = 'sigma.www.views.general.handler500'

urlpatterns = patterns('',
           (r'^admin/(.*)', admin.site.root),
           (r'^$', include('sigma.www.urls.general')),
           (r'^appels/', include('sigma.www.urls.appels')),
           (r'^candidatures/', include('sigma.www.urls.candidatures')),
           (r'^categories/', include('sigma.www.urls.categories')),
           (r'^projets/', include('sigma.www.urls.projets')),
           (r'^experts/', include('sigma.www.urls.experts')),
           (r'^etablissements/', include('sigma.www.urls.etablissements')),            
           (r'^champs/', include('sigma.www.urls.champs')),
           (r'^blocs/', include('sigma.www.urls.blocs')),
           (r'^search/', include('sigma.www.urls.search')),
           (r'^accounts/', include('sigma.www.urls.accounts')),
           (r'^notes/', include('sigma.www.urls.notes')),
           (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
           (r'^dynamic-media/jsi18n/$', 'django.views.i18n.javascript_catalog'), 
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )
