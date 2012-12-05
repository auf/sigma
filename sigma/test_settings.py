from sigma.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testing.db',
    }
}

WCS_SIGMA_URL = 'https://formulaires.auf.org/sigma/'
WCS_SIGMA_USER = ''
WCS_SIGMA_PASS = ''

AUF_REFERENCES_MANAGED = True

# This is used when overriding get_query_set, allows me to get all
# data without filtering. Set to false in case you need to run
# dumpdata for example.
#ENABLE_FILTERED_QUERYSETS = False
