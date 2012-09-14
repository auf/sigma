# -*- encoding: utf-8 -*-

from sigma.settings import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# auf.django.auth

AUTH_PASSWORD_REQUIRED = False

# django-sendfile

SENDFILE_BACKEND = 'sendfile.backends.development'
