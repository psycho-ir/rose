import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

COMPRESS_ROOT = os.path.join(BASE_DIR, 'stat')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o**w8ex&cydi*(r26ajcc71^k8kb099)4(36zjr9i&q4v7rex@'

INTERNAL_IPS = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']

DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

# Application definition
INSTALLED_APPS = (
    'customer',
    'dashboard',
    'user_profile',
    'django.contrib.auth',
    'user_management',
    'core_connection',
    'rose_config',
    'start_grant',
    'guarantor',
    'assign',
    'superior',
    'notification',
    'south',
    'compressor',
    'django_scheduler',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    # 'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'notification.context_processor.notification'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'rose.urls'

WSGI_APPLICATION = 'rose.wsgi.application'
from django.db import connections
from django.db import connection

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': 'orcl',
    #     'USER': 'rose',
    #     'PASSWORD': 'rose',
    #     'HOST': '192.168.101.151',
    #     'PORT': '1521',
    #     'ATOMIC_REQUESTS': True
    # },

    'default': {
    'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'rose'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'root'),
        'HOST': '127.0.0.1',
        'ATOMIC_REQUESTS': True
    },

    'core': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'orcl',
        'USER': 's5samens',
        'PASSWORD': 's5samens',
        'HOST': '192.168.101.97',
        'PORT': '1521',
        'OPTIONS': {
            'threaded': True,
            'use_returning_into': False,
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),  # Assuming BASE_DIR is where your manage.py file is
)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

DEFAULT_LOGIN_URL = '/grant/track'
DEFAULT_LOGOUT_URL = '/'

# STATIC resources config

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'stat')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


##### CACHE config ##########
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}