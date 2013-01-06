# -*- encoding: utf-8 -*-

import os
import socket

PROJECT_PATH = os.path.dirname(__file__)
HOME = os.path.dirname(PROJECT_PATH)

PROJET_TITRE = "SIGMA"

# Rapports d'erreurs
EMAIL_SUBJECT_PREFIX = '[SIGMA - %s] ' % socket.gethostname()

ADMINS = () #n'envoie pas de courriel de traceback
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'dynamo': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'
USE_L10N = True
LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
)


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(HOME, 'media')
UPLOADS_ROOT = os.path.join(HOME, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Don't share this with anybody.
SECRET_KEY = 'wbt#ie2bktr9c7o%4cgr&9@%!3ik3#f6lh#6k@fb=l5&*ndr-m'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'sigma.urls'

INSTALLED_APPS = (
    'sigma.custom_admin',
    'admin_tools',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apptemplates',
    'auf.django.auth',
    'auf.django.admingroup',
    'auf.django.export',
    'auf.django.permissions',
    'auf.django.skin',
    'auf.django.references',
    'auf.django.workflow',
    'haystack',
    'form_utils',
    'south',
    'raven.contrib.django',
    'sigma.management',
    'sigma.core',
    'sigma.boursiers',
    'sigma.candidatures',
    'sigma.wcs',
    'sigma.dynamo',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'auf.django.skin.context_processors.auf',
)

AUTHENTICATION_BACKENDS = (
    'auf.django.auth.backends.CascadeBackend',
    'auf.django.permissions.AuthenticationBackend',
)

AUTH_PROFILE_MODULE = "candidatures.userprofile"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader', # so we can use {% extends "module:template.html" %}
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_MENU = 'sigma.custom_admin.menu.MainMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'sigma.custom_admin.dashboard.IndexDashboard'

HELP_TEXT_DATE = "format: jj/mm/aaaa"

# django-sendfile

SENDFILE_BACKEND = 'sendfile.backends.simple'

# auf.django.permissions

AUF_PERMISSIONS_RULES = 'sigma.permissions.rules'

# auf.django.auth

AUTH_PASSWORD_REQUIRED = True

# django.contrib.staticfiles

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(HOME, 'sitestatic')

from sigma.conf import *  # NOQA

# Force innoDb
DATABASES['default']['OPTIONS'] = {
    "init_command": "SET storage_engine=InnoDB",
}

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#         'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
#     },
# }

HAYSTACK_SITECONF = 'sigma.search_site'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(__file__), 'whoosh_index')
