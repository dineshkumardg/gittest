import os
import logging
import inspect
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from gaia.utils.image_attributes import JpegImageAttributes
import project.cho.gaia_dom_adapter.factory


class SystemTestConfig:
    '''
    source system_test/common/config.sh prior to running from within eclipse
    '''
    def __init__(self):
        try:
            HOSTNAME = socket.gethostname()
        except Exception:
            HOSTNAME = '0.0.0.0'

        self.transfer_batch_size = os.environ['EGEST_TRANSFER_BATCH_SIZE']

        # TODO sort out similar names due to conflicts elsewhere :-(
        self._schema_dir = os.environ['LOCAL_SRC_DIR_SCHEMA']
        self.schema_dir = os.environ['LOCAL_SRC_DIR_SCHEMA']
        self._working_dir = os.environ['LOCAL_WORKING_DATA_DIR']
        self.working_dir = os.environ['LOCAL_WORKING_DATA_DIR']

        self.log_dir = os.environ['LOCAL_WORKING_DATA_DIR_LOGS']
        self.inbox = os.environ['LOCAL_WORKING_DATA_DIR_INBOX']
        self.outbox = os.environ['LOCAL_WORKING_DATA_DIR_OUTBOX']
        self.giftbox = os.environ['LOCAL_WORKING_DATA_DIR_GIFTBOX']
        self.imagebox = os.environ['LOCAL_WORKING_DATA_DIR_IMAGEBOX']
        self.transfer_prep_dir = os.environ['LOCAL_WORKING_DATA_DIR_TRANSFERPREPDIR']
        self.egest_working_dir = os.environ['LOCAL_WORKING_DATA_DIR_EGEST_WORKING_DIR']

        self.project_code = os.environ['PROJECT_CODE']
        self.content_set_name = os.environ['PROJECT_CODE'].upper()

        self.schema_name = os.environ['CONFIG_SCHEMA_NAME']
        self.image_file_ext = os.environ['CONFIG_IMAGE_FILE_EXT']

        self.ADMINS = ((os.environ['CONFIG_ADMINS']),)

        if os.environ['REMOTE_PROVIDER_USE_MULTIPLE'] == "2":
            self.content_providers = {os.environ['REMOTE_PROVIDER_01_ID']: {'server': os.environ['REMOTE_PROVIDER_01_FTP_HOST'], 'uid': os.environ['REMOTE_PROVIDER_01_FTP_UID'], 'pwd': os.environ['REMOTE_PROVIDER_01_FTP_PWD']},
                                      os.environ['REMOTE_PROVIDER_02_ID']: {'server': os.environ['REMOTE_PROVIDER_02_FTP_HOST'], 'uid': os.environ['REMOTE_PROVIDER_02_FTP_UID'], 'pwd': os.environ['REMOTE_PROVIDER_02_FTP_PWD']},
            }
        else:
            self.content_providers = {os.environ['REMOTE_PROVIDER_01_ID']: {'server': os.environ['REMOTE_PROVIDER_01_FTP_HOST'], 'uid': os.environ['REMOTE_PROVIDER_01_FTP_UID'], 'pwd': os.environ['REMOTE_PROVIDER_01_FTP_PWD']},
            }

        self.dom_adapter_factory =  project.cho.gaia_dom_adapter.factory.Factory

        self.adapter_class = None
        self.schema_fpath = os.environ['LOCAL_SRC_XSD_CHATHAM_HOUSE']
        self.WEB_ROOT = os.environ['LOCAL_WORKING_DATA_DIR_WEBROOT']

        if os.environ['USEPOSTGRES'] == 'True':
            self.DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': os.environ['LOCAL_DB_NAME'],
                    'USER': os.environ['LOCAL_DB_UID'],
                    'PASSWORD': os.environ['LOCAL_DB_PWD'],
                    'HOST': os.environ['LOCAL_DB_HOST'],
                    'PORT': os.environ['LOCAL_DB_PORT'],
                }
            }
        else:
            self.DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.environ['LOCAL_DB_SQLITE_NAME'],
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            }

        #######################################################################

        self.TIME_ZONE = 'GMT'
        self.LANGUAGE_CODE = 'en-gb'
        self.SITE_ID = 1
        self.USE_I18N = True
        self.USE_L10N = True
        self.SECRET_KEY = '!"%^&*()goddess gaia rules all in 2012!"%^&*()'

        self.STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        )

        self.TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )

        self.MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.transaction.TransactionMiddleware',  # one commit per http request (or rollback)
        )

        self.ROOT_URLCONF = 'gaia_web.urls'

        self.INSTALLED_APPS = ( # the first three are separate models, which all get merged together.
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

        self.DEBUG = True
        self.TEMPLATE_DEBUG = True
        self.ADMINS = (
            ('EMEA Software Team', 'EMEA.SoftwareTeam@cengage.com'),
        )

        self.TEMPLATE_DIRS = (
            os.environ['LOCAL_SRC_DIR_TEMPLATE'],
        )

        self.TEMPLATE_CONTEXT_PROCESSORS = TCP + (
            'django.core.context_processors.request',
        )

        self.WEB_ROOT = os.environ['LOCAL_WORKING_DATA_DIR_WEBROOT']

        self.MEDIA_ROOT = ''
        self.MEDIA_URL = 'http://%s/gaia/media/' % HOSTNAME

        self.STATIC_ROOT = os.environ['LOCAL_WORKING_DATA_DIR_WEBROOT']
        self.STATIC_URL = 'http://%s/gaia/' % HOSTNAME

        self.perl_fpath = '/usr/bin/perl'
        self.xmllint_fpath = '/usr/bin/xmllint'
        self.identify_fpath = '/usr/bin/identify'
        self.convert_fpath = '/usr/bin/convert'
        self.zip_fpath = '/usr/bin/7z'

        self.max_requests_outstanding = int(os.environ['MAX_REQUESTS_OUTSTANDING'])
        self.response_threshold = int(os.environ['RESPONSE_THRESHOLD'])
        self.poll_interval = int(os.environ['POLL_INTERVAL'])

        self.egest_max_requests_outstanding = int(os.environ['EGEST_MAX_REQUESTS_OUTSTANDING'])
        self.egest_response_threshold = int(os.environ['EGEST_RESPONSE_THRESHOLD'])
        self.egest_poll_interval = int(os.environ['EGEST_POLL_INTERVAL'])

        self.ingest_job_sockets = {
            'request': {'send': os.environ['WORKER_SOCKET_OUT'], 'recv': os.environ['WORKER_SOCKET_IN'],},   # push/pull
            'reply':   {'send': os.environ['WORKER_STATUS_OUT'], 'recv': os.environ['WORKER_STATUS_IN'],},           # push/pull
        }

        self.management_sockets = {
            'command':  {'send': os.environ['MANAGER_SOCKET_OUT'], 'recv': os.environ['MANAGER_SOCKET_IN'],},  # pub/sub
            'status':   {'send': os.environ['MANAGER_STATUS_OUT'], 'recv': os.environ['MANAGER_STATUS_IN'],},          # pub/sub
        }

        self.egest_job_sockets = {
            'request':  {'send': os.environ['EGEST_WORKER_SOCKET_OUT'], 'recv': os.environ['EGEST_WORKER_SOCKET_IN'],},  # push/pull
            'reply':    {'send': os.environ['EGEST_WORKER_STATUS_OUT'], 'recv': os.environ['EGEST_WORKER_STATUS_IN'],},          # push/pull
        }

        self.egest_ftp_platform = {}

        self.image_attrs = [JpegImageAttributes(400, 8),
                       JpegImageAttributes(300, 8),
                       JpegImageAttributes(72, 8)]

        self.categories = [
                'Arts and Entertainment',
                'Births',
                'Business and Finance',
                'Business Appointments',
                'Classified Advertising',
                'Court and Social',
                'Deaths',
                'Display Advertising',
                'Editorials/Leaders',
                'Feature Articles (aka Opinion)',
                'Index',
                'Law',
                'Letters to the Editor',
                'Marriages',
                'News',
                'News in Brief',
                'Obituaries',
                'Official Appointments and Notices',
                'Picture Gallery',
                'Politics and Parliament',
                'Property',
                'Publication Matter',
                'Reviews',
                'Sport',
                'Stock Exchange Tables',
                'Weather',
            ]

        self.illustration_types = [
                'Cartoons',
                'Drawing-Painting',
                'Graph',
                'Map',
                'Photograph',
                'Table',
            ]

        self.log_level = logging.DEBUG
        #self.web_image_ftype = 'png'  # would create two extra png files from the 1 jpg
        self.web_image_ftype = 'jpg'  # only creates 1 extra - thumbnail - jpg file (as per production)
        
        # params for retrying the ftp connection
        self.retry_counter = os.environ['RETRY_COUNTER']
        self.retry_timer = os.environ['RETRY_TIMER']

        self.egest_adapters = [('project.cho.egest_adapter.cho_xml_adapter.ChoXmlAdapter',
                                { 'server': os.environ['EGEST_TRANSFER_PLATFORM_LST_HOST'], 
                                 'uid': os.environ['EGEST_TRANSFER_PLATFORM_LST_UID'], 
                                 'pwd': os.environ['EGEST_TRANSFER_PLATFORM_LST_PWD'], 
                                 'initial_dir': os.environ['EGEST_TRANSFER_PLATFORM_LST_RDIR'], 
                                 'retry_counter': self.retry_counter, 
                                 'retry_timer': self.retry_timer, }),
                               ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter', 
                                {'server':  os.environ['EGEST_TRANSFER_PLATFORM_CALLISTO_HOST'], 
                                 'uid': os.environ['EGEST_TRANSFER_PLATFORM_CALLISTO_UID'], 
                                 'pwd': os.environ['EGEST_TRANSFER_PLATFORM_CALLISTO_PWD'], 
                                 'initial_dir': os.environ['EGEST_TRANSFER_PLATFORM_CALLISTO_RDIR'], 
                                 'retry_counter': self.retry_counter, 
                                 'retry_timer': self.retry_timer, })]

        self._schema_dir = os.environ['LOCAL_SRC_DIR_SCHEMA']
        self._working_dir = os.environ['LOCAL_WORKING_DATA_DIR']

        self.search_adapter_class_name = 'gaia.search.adapter.chunk_search_adapter.ChunkSearchAdapter'
        self.search_server = '%s:%s' % (os.environ['SOLR_HOST'], os.environ['SOLR_PORT'])
        self.qa_server = '%s:%s' % (os.environ['CHERRYPY_HOST'], os.environ['CHERRYPY_PORT'])

        self.content_set_name    = os.environ['CALLISTO_CONTENT_SET_NAME']
        self.av_content_set_name = os.environ['CALLISTO_CONTENT_SET_NAME_AV']

    def check(self):
        pass

    def get_django_settings(self):
        return {x: y for x, y in inspect.getmembers(self) if x[0].isupper()}
