import os
import sys
import inspect
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


try:
    HOSTNAME = socket.gethostname()
except Exception:
    HOSTNAME = 'ukandgaia07'

# Django settings for gaia_web projects: ref: https://docs.djangoproject.com/en/dev/ref/settings/
class _GaiaDjangoDefaults:
    # TODO: remove any of these that are the same as django defaults.
    TIME_ZONE = 'GMT'
    LANGUAGE_CODE = 'en-gb'
    SITE_ID = 1
    USE_I18N = True
    USE_L10N = True
    SECRET_KEY = '!"%^&*()goddess gaia rules all in 2012!"%^&*()'

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.transaction.TransactionMiddleware',  # one commit per http request (or rollback)
    )

    ROOT_URLCONF = 'gaia_web.urls'

    INSTALLED_APPS = (
        'cengage.asset_id',
        'qa',
        'gaia.dom.index',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'rest_framework',
    )

    DEBUG = False
    TEMPLATE_DEBUG = False
    ADMINS = (
        ('EMEA Software Team', 'EMEA.SoftwareTeam@cengage.com'),
    )

    TEMPLATE_DIRS = (
        '/usr/local/gaia/qa/templates/',
    )
    
    TEMPLATE_CONTEXT_PROCESSORS = TCP + (  # Do this because request is not provided to views in RequestContext instance by default
        'django.core.context_processors.request',  # We also want to maintain the default TEMPLATE_CONTEXT_PROCESSORS (default may change in future versions!!)
    )

    WEB_ROOT='/GAIA/WEB_ROOT/gaia'

    MEDIA_ROOT = ''
    MEDIA_URL = 'http://%s/static/gaia/' % HOSTNAME

    STATIC_ROOT = '/var/www/static/'
    STATIC_URL = 'http://%s/static/' % HOSTNAME

    # This should stop django adding the console logger (if it really is...TODO: investigate further! :( )?
    LOGGING_CONFIG = None   # use our own Gaia loggig config instead of django's one.

    def get_django_settings(self):
        return {x: y for x, y in inspect.getmembers(self) if x[0].isupper()}


class STHASettings(_GaiaDjangoDefaults):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'STHA', # ***
            'USER': 'gaia',    
            'PASSWORD': 'g818',
            'HOST': '',
            'PORT': '5433',
        }
    }

class CHOSettings(_GaiaDjangoDefaults):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'cho',
            'USER': 'gaia',    
            'PASSWORD': 'g818',
            'HOST': '',
            'PORT': '5432',	# note: was 5433
        }
    }

    TEMPLATE_DIRS = ( # TEMPORARY settings for UAT ONLY!
        '/home/gaia/GIT_REPOS/gaia/src/qa/templates',
    )

    MEDIA_ROOT = '' # Absolute filesystem path to the directory that will hold user-uploaded files. # UNUSED
    MEDIA_URL = 'http://%s/static/' % HOSTNAME

    WEB_ROOT    = '/GAIA/cho/web_root'
    STATIC_ROOT = '/GAIA/cho/web_root/'
    STATIC_URL = 'http://%s/cho/' % HOSTNAME


class _ModelsOnlySettings(_GaiaDjangoDefaults):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '_TMP_DEV_MODELS_ONLY_DB',
            'USER': 'gaia',    
            'PASSWORD': 'g818',
            'HOST': '',
            'PORT': '5433'
        }
    }


class TUSH_PCSettings(_GaiaDjangoDefaults):
    MEDIA_URL = 'http://%s:8887/static/gaia/' % HOSTNAME

    WEB_ROOT='c:/inetpub/wwwroot/gaia'
    STATIC_ROOT = WEB_ROOT
    STATIC_URL = 'http://%s/gaia/' % HOSTNAME

    TEMPLATE_DIRS = ('/GIT_REPOS/gaia/src/qa/templates/',)

    DEBUG = True
    TEMPLATE_DEBUG = True
    ADMINS = (('Tushar Wagle', 'tushar.wagle@cengage.com'),)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/GAIA/TUSH_PC.db',
            'USER': '',    
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }


class TUSH_NEWS_PCSettings(TUSH_PCSettings):
    #WEB_ROOT='c:/inetpub/wwwroot/gaia' #*** NOTE: NEEDS TO CHANGE to gaia/STHA
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/GAIA/TUSH_NEWS_PC.db',
            'USER': '',    
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }


class TUSH_LinuxSettings(_GaiaDjangoDefaults):
    MEDIA_URL = 'http://%s/static/gaia/' % HOSTNAME
    STATIC_URL = 'http://%s/static/' % HOSTNAME

    WEB_ROOT='/home/tushar/GAIA_WORKING_DATA/WEB_ROOT'
    STATIC_ROOT = WEB_ROOT
    TEMPLATE_DIRS = ('/home/tushar/GIT_REPOS/gaia/src/qa/templates/',)

    DEBUG = True
    TEMPLATE_DEBUG = True
    ADMINS = (('Tushar Wagle', 'tushar.wagle@cengage.com'),)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/home/tushar/GAIA_WORKING_DATA/tush_dev.db',
            'USER': '',    
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }


class JamesLinuxDjangoSettings(_GaiaDjangoDefaults):
    MEDIA_URL = 'http://%s/static' % HOSTNAME

    STATIC_ROOT = '/home/jsears/GAIA_WORKING_DATA/WEB_ROOT'
    STATIC_URL = 'http://%s/static/' % HOSTNAME

    WEB_ROOT='/home/jsears/GAIA_WORKING_DATA/WEB_ROOT'
    TEMPLATE_DIRS = ('/home/jsears/GIT_REPOS/gaia/src/qa/templates/',)

    DEBUG = True
    TEMPLATE_DEBUG = True
    ADMINS = (('James Sears', 'james.sears@cengage.com'),)

    #DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': '/home/jsears/GAIA_WORKING_DATA/cho/sqllite.db',
    #        'USER': '',
    #        'PASSWORD': '',
    #        'HOST': '',
    #        'PORT': '',
    #    }
    #}
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'cho',
            'USER': 'gaia',
            'PASSWORD': 'gaia',
            'HOST': '127.0.0.1',
            'PORT': '5433'
        }
    }


class UnittestSettings(_GaiaDjangoDefaults):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    if sys.platform == 'win32':
        TEMPLATE_DIRS = ('/GIT_REPOS/gaia/src/qa/templates/',)
    else:
        home = os.environ['HOME']
        TEMPLATE_DIRS = (os.path.join(home, '/GIT_REPOS/gaia/src/qa/templates/'), )
