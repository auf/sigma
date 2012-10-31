# -*- encoding: utf-8 -*-

from sigma.settings import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# auf.django.auth

AUTH_PASSWORD_REQUIRED = False

# django-sendfile

SENDFILE_BACKEND = 'sendfile.backends.development'

# Décommentez ces lignes pour activer la debugtoolbar
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
