# -*- encoding: utf-8 -*-

import os
import socket
from conf import *  # NOQA

PROJET_TITRE = "SIGMA"

# Rapports d'erreurs
EMAIL_SUBJECT_PREFIX = '[SIGMA - %s] ' % socket.gethostname()
ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
UPLOADS_ROOT = os.path.join(os.path.dirname(__file__), 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/django/'

# Don't share this with anybody.
SECRET_KEY = 'wbt#ie2bktr9c7o%4cgr&9@%!3ik3#f6lh#6k@fb=l5&*ndr-m'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.messages',
    'auf.django.auth',
    'auf.django.admingroup',
    'auf.django.coda',
    'auf.django.export',
    'auf.django.skin',
    'auf.django.references',
    'auf.django.workflow',
    'south',
    'form_utils',
    'sigma',
    'suivi',
    'wcs',
    'smart_selects',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'auf.django.skin.context_processors.auf',
)

AUTHENTICATION_BACKENDS = (
    'auf.django.auth.backends.CascadeBackend',
)

AUTH_PROFILE_MODULE = "sigma.userprofile"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_MENU = 'project.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

HELP_TEXT_DATE = "format: jj/mm/aaaa"

# django-sendfile

SENDFILE_BACKEND = 'sendfile.backends.simple'
