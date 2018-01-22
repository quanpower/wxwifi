# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Created:16-10-27 上午11:43

# Django settings for smartlinkcloud project.
import os

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BASE_DIR = PROJECT_ROOT

DEBUG = True

ADMINS = (
    ('William', '252527676@qq.com'),
)

# Default to dummy email backend. Configure dev/production/local backend
# as per https://docs.djangoproject.com/en/dev/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'smartlinkcloud',
    #     'USER': 'quanpower',
    #     'PASSWORD': 'caojing1010',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DATE_FORMAT = 'j F Y'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(BASE_DIR, "common_static"),
    '/root/wxwifi/wxwifi/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# ** You would never normally put the SECRET_KEY in a public repository,
# ** however this is a demo app so we're using the default settings.
# ** Don't use this key in any non-demo usage!
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wq21wtjo3@d_qfjvd-#td!%7gfy2updj2z+nev^k$iy%=m4_tr'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wxwifi.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wxwifi.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    # 'rest_framework',
    #
    # 'wagtail.wagtailcore',
    # 'wagtail.wagtailadmin',
    # 'wagtail.wagtaildocs',
    # 'wagtail.wagtailsnippets',
    # 'wagtail.wagtailusers',
    # 'wagtail.wagtailimages',
    # 'wagtail.wagtailembeds',
    # 'wagtail.wagtailsearch',
    # 'wagtail.wagtailredirects',
    # 'wagtail.wagtailforms',
    # 'wagtail.wagtailsites',
    # 'wagtail.contrib.wagtailapi',
    # # for wagtailmenus
    # 'wagtail.contrib.modeladmin',
    # # for puput
    # 'wagtail.contrib.wagtailsitemaps',
    # 'wagtail.contrib.wagtailroutablepage',


    'wifi',
)

# This will avoid duplicate inclusion of Wagtail’s URLs when you include Puput’s URLs.
PUPUT_AS_PLUGIN = True

# Add wagtail.contrib.wagtailsearchpromotions to INSTALLED_APPS
# if we're on Wagtail 1.1 or later.
# NB this is a quick-and-dirty version check that won't work with
# full generality (double-digit versions, alpha/beta releases)

# from wagtail.wagtailcore import __version__
# if __version__.split('.') > ['1', '0']:
#     INSTALLED_APPS = list(INSTALLED_APPS) + ['wagtail.contrib.wagtailsearchpromotions']
#

EMAIL_SUBJECT_PREFIX = '[smartlinkcloud] '

INTERNAL_IPS = ('127.0.0.1', '101.200.158.2')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR,'templates').replace('\\', '/'),
            os.path.join(BASE_DIR,'templates2').replace('\\', '/'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
            'debug': DEBUG,
        },
    },
]

# django-compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# WAGTAIL SETTINGS

WAGTAIL_SITE_NAME = u'智联云'

# WECHAT SETTINGS

APPID = 'wxa5a680ce9bf84e3a'
SECRET = '50bea6550b224a30f412de287a07c0a8'
ENCODINGAESKEY = 'YOyKXEWnDuF1hUw2dWdB0PHZxg4QrpBWC1AMiipxafc'
TOKEN = 'SmartLinkCloud'

OPENID = 'ohIv0wAqv3fIcitg4OyyIpULnhcU'

REDIRECT_URI = 'http://www.smartlinkcloud.com/wechat/public/oauth2'
CHAT_ROOM_LOGIN_REDIRECT_URI = 'http://www.smartlinkcloud.com/chat_room/login'
SCOPE = 'snsapi_userinfo' # or 'snsapi_base'
STATE = '6027'

WECHAT_PAY_MCH_ID = '1340292801'
WECHAT_PAY_APIKEY = 'u1AynAl7iLrYJaIM11Xo9Uvro71PqyFw'
WECHAT_PAY_MCH_CERT_PATH = os.path.join(os.path.dirname(__file__), "cert/apiclient_cert.pem")
WECHAT_PAY_MCH_KEY_PATH = os.path.join(os.path.dirname(__file__), "cert/apiclient_key.pem")

COMPONENT_APPID = 'wx9e4e87e10afe0fba'
COMPONENT_APPSECRECT = 'f38c20516a3c5103a1faab349524a87d'
COMPONENT_TOKEN = 'SmartLinkCloud'
