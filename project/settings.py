# -=- encoding: utf-8 -=-
import os
import reusableapps
import sigma.www

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

SITE_ID = 42

DATABASE_ENGINE = 'mysql'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'sigma'
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'patati42'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Chicago'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'src', 'sigma.www', 'sigma', 'www','media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'project.urls'


INSTALLED_APPS = ('django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django_tables',     
    'pagination',                  
    'django_roa'
    'auf_roa_authentification.lib',
    'sigma.references',
    'sigma.www',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source'
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(sigma.www.__file__), "templates"),
)

DATA_DIRS = (
    os.path.join(os.path.dirname(sigma.www.__file__), "data"),
)

AUTH_PROFILE_MODULE = "sigma.www.profiles.UserProfile"

# C'est le nom d'utilisateur de l'administrateur du site, il sera automatiquement créé 
# lorsqu'on essayeras de se connecter pour la première fois
ADMIN_LOGIN = "admin"

# C'est le mot de passe de l'administrateur, il est ici encrypté en format sha1
ADMIN_PASSWORD = 'sha1$7dc98$a58a4588b734faa0198f5ba8aae80c5030de5dc6'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

# Don't share this with anybody.
SECRET_KEY = 'i=_8%9t9wbdm*&)ugzn3ms&mues9afprzd&8cgfm!6402eo2$='

DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'fr_FR'

LANGUAGES = (
        ('fr', 'French'),
)
 
# Utilise afin de bypasser l'authentification par mot de passe
AUTHENTICATION_BACKENDS = (
    'auf_roa_authentification.lib.backends.CascadeBackend',
    'sigma.www.authentification.SettingsBackend',
)
AUTH_PASSWORD_REQUIRED = True
AUTOMATIC_ADMIN_CREATE = True

# Pour ROA
ROA_MODELS = True   # set to False if you'd like to develop/test locally
ROA_FORMAT = 'django'
ROA_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
ROA_DJANGO_ERRORS = True # useful to ease debugging if you use test server

ROA_MODEL_NAME_MAPPING = (
    ('remoteauth.', 'auth.'),
)
ROA_BASE_URL = 'https://authentification.auf.org/auth/'
SERIALIZATION_MODULES = {
    'django' : 'auf_roa_authentification.lib.serializers',
}
