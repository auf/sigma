# -*- encoding: utf-8 -*
from django.conf.urls.defaults import \
        patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler500, handler404  # Pyflakes

urlpatterns = patterns(
    '',
    (r'^$', 'project.views.index'),
    (r'^', include('sigma.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^connexion/$', 'django.contrib.auth.views.login'),
    (r'^deconnexion/$', 'django.contrib.auth.views.logout'),
)
if hasattr(settings, 'WCS_SIGMA_URL'):
    urlpatterns += patterns('', (r'^', include('wcs.urls')),)
