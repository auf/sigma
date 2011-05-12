# -*- encoding: utf-8 -*
from django.conf.urls.defaults import patterns, include, handler500, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    (r'^$', 'project.views.index'),
    (r'^', include('sigma.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^connexion/$', 'django.contrib.auth.views.login'),
    (r'^deconnexion/$', 'django.contrib.auth.views.logout'),

    # Les pièces sont stockées dans un endroit différent de media
    # car l'accès doit être controlé
    (r'^media_prive/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PRIVE_ROOT}),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
