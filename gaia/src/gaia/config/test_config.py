from testing.gaia_django_test import GaiaDjangoTest
_test = GaiaDjangoTest()
_test.setUp()


import unittest
from gaia.config.config_errors import GaiaConfigurationError
from gaia.config.config import get_config, _Config
from gaia.config.project_mixins import STHAProject, CHOProject
from gaia.config.platform_mixins import UkandgaiaPlatform, Ukandgaia07Platform


class TestConfig(unittest.TestCase):

    def _check_settings(self, config):
        # all of these MUST be available..
        self._check_basic_settings(config)
        self._check_django_settings(config)
        self._check_get_django_settings(config)

    def _check_basic_settings(self, config):
        config.CONFIG_NAME
        config.web_image_ftype

        config.project_code
        config.content_set_name
        config.av_content_set_name
        config.schema_fpath

        config.image_file_ext 
        config.image_attrs

        config.perl_fpath
        config.xmllint_fpath
        config.identify_fpath
        config.convert_fpath
        config.zip_fpath

        config._schema_dir
        config.working_dir
        config.inbox
        config.outbox
        config.log_dir
        config.egest_working_dir

        config.content_providers
        config.max_requests_outstanding
        config.response_threshold
        config.poll_interval

        config.dom_adapter_factory

        self.assertTrue(isinstance(config.content_providers, dict))

    def _check_django_settings(self, config):
        config.DATABASES
        config.DEBUG
        config.INSTALLED_APPS
        config.LANGUAGE_CODE
        config.MEDIA_ROOT
        config.MEDIA_URL
        config.MEDIA_URL
        config.MIDDLEWARE_CLASSES
        config.ROOT_URLCONF
        config.SECRET_KEY
        config.SITE_ID
        config.STATICFILES_FINDERS
        config.STATIC_ROOT
        config.STATIC_URL
        config.TEMPLATE_DEBUG
        config.TEMPLATE_DIRS
        config.TEMPLATE_LOADERS
        config.TIME_ZONE
        config.USE_I18N
        config.USE_L10N

        config.WEB_ROOT # this isn't a standard django setting, but is used in gaia_web.
        config.CONFIG_NAME

    def _check_get_django_settings(self, config):
        settings = config.get_django_settings()

        self.assertTrue('WEB_ROOT' in settings)
        self.assertTrue('DATABASES' in settings)

    def test_get_config_NOT_EXISTS(self):
        self.assertRaises(GaiaConfigurationError, get_config, '_not_exists_')

    def test_get_config_STHA(self):
        config = get_config('STHA')
        
        self.assertTrue(issubclass(config.__class__, _Config))
        self.assertTrue(issubclass(config.__class__, STHAProject))
        self.assertTrue(issubclass(config.__class__, UkandgaiaPlatform))

        self._check_settings(config)

    def test_get_config_CHO(self):
        config = get_config('CHO')
        
        self.assertTrue(issubclass(config.__class__, _Config))
        self.assertTrue(issubclass(config.__class__, CHOProject))
        self.assertTrue(issubclass(config.__class__, Ukandgaia07Platform))

        self._check_settings(config)


class TestConfigDevEnvs(unittest.TestCase):
    'Use this to check your development environment config setup'

    # DEV: Add a test like this to test your development config in your environment..
    def test_check_TUSH_PC(self):
        config = get_config('TUSH_PC')
        config.check()

    def test_check_TUSH_NEWS_PC(self):
        config = get_config('TUSH_NEWS_PC')
        config.check()

    def test_check_TUSH_LINUX(self):
        config = get_config('TUSH_LINUX')
        config.check()

    def test_check_JAMES_LINUX(self):
        config = get_config('JAMES_LINUX')
        config.check()
        
    def test_check_SYSTEM_TEST(self):
        config = get_config('SYSTEM_TEST')
        config.check()
        
    def test_check_DEMO(self):
        config = get_config('DEMO')
        config.check()

    def test_check_CHO(self):   # not sure why this is here (it's not a development config, it's a live one!?)
        config = get_config('CHO')
        config.check()

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestConfig),
    ])

_test.tearDown()#?

if __name__ == "__main__":
    unittest.main()
