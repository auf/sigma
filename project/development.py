# -*- encoding: utf-8 -*-

from project.settings import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Décommentez ces lignes pour activer la debugtoolbar
#INTERNAL_IPS = ('127.0.0.1',)
#INSTALLED_APPS += ('debug_toolbar',)
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += ('django_extensions',)

# auf.django.auth

AUTH_PASSWORD_REQUIRED = False

# django-sendfile

SENDFILE_BACKEND = 'sendfile.backends.development'
