# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os

DOMAIN_NAME = 'www.fromrussiatous.com'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'external_auth.auth_backends.NoPassBackend',
)

INSTALLED_APPS = (
    'djangoappengine',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.comments',
    'djangotoolbox',
    'blog',
    'external_auth',
    'testdebug',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

GAE_SETTINGS_MODULES = (
    'gae_comment_settings',
)


# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
STATICFILES_ROOT = os.path.join(os.path.dirname(__file__), '_generated_media')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
)
STATICFILES_URL = '/media/'
MEDIA_URL = '/files/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

SITE_ID = 1

# Activate django-dbindexer if available
try:
    import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('dbindexer',)
except ImportError:
    pass

