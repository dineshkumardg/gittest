# Django settings for Unit Testing. ref: https://docs.djangoproject.com/en/dev/ref/settings/
import inspect
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

class DjangoConfig:
    ' basic Django settings for EMEA (Note:: is incomplete: needs subclassing) '
    CONFIG_NAME = 'TODO_override_me'

    # Note: TODO: remove any of these that are the same as django defaults.
    TIME_ZONE = 'GMT'
    LANGUAGE_CODE = 'en-gb'
    SITE_ID = 1
    USE_I18N = True
    USE_L10N = True
    SECRET_KEY = '!"%^&*() EMEA rule ;) 2013"%^&*()'

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

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
    )

    DEBUG = False
    TEMPLATE_DEBUG = False
    ADMINS = (
        ('EMEA Software Team', 'EMEA.SoftwareTeam@cengage.com'),
    )

    TEMPLATE_CONTEXT_PROCESSORS = TCP + (           # Do this because request is not provided to views in RequestContext instance by default
        'django.core.context_processors.request',   # We also want to maintain the default TEMPLATE_CONTEXT_PROCESSORS (default may change in future versions!!)
    )

    # NOT WORKING??....
    # This should stop django adding the console logger (if it really is...TODO: investigate further! :( )?
    LOGGING_CONFIG = None   # use our own Gaia loggig config instead of django's one.
        
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

    def get_django_settings(self):
        return {x: y for x, y in inspect.getmembers(self) if x[0].isupper()}

    def __str__(self):
        return '\n' + '\n'.join(['\t%s=%s' % (x, y) for (x, y) in inspect.getmembers(self) if not x.startswith('__') and not x == 'check'])
