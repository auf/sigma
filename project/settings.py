# -*- encoding: utf-8 -*-

import os
import socket
from conf import *


DATABASE_OPTIONS = {
   'init_command': 'SET storage_engine=INNODB;',
}

PROJET_TITRE = "SIGMA"

# Rapports d'erreurs
EMAIL_SUBJECT_PREFIX = '[SIGMA - %s] ' % socket.gethostname()
ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Canada/Montreal'

LANGUAGE_CODE = 'fr-ca'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_PRIVE_ROOT = os.path.join(os.path.dirname(__file__), 'media_prive')

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'auf.django.skin',
    'auf.django.auth',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'south',
    'reversion',
    'auf.django.admingroup',
    'auf.django.workflow',
    'form_utils',
    'sigma',
    'suivi',
    'auf.django.export',
    'wcs',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'auf.django.skin.context_processors.auf',
)

AUTHENTICATION_BACKENDS = (
    'auf.django.auth.backends.CascadeBackend',
)

AUTH_PROFILE_MODULE = "sigma.userprofile"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_MENU = 'project.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

DATE_INPUT_FORMATS = ["%d-%m-%Y"]
