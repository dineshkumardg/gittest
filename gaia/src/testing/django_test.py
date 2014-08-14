from django.conf import settings
from django.core.management import call_command
from testing.gaia_test import GaiaTest

class DjangoTest(GaiaTest):
    ''' A base Test class for Django Tests within the Gaia environment

        When you write a django test, you MUST use django_test.setUp()
        before any django imports, and you MUST call tearDown()!
    '''

    def __init__(self): 
        GaiaTest.__init__(self)
        self._is_setup = False

    def setUp(self, config):
        ''' Configure settings and set up/sync a test database
            Does everything needed to get a fresh test environment when not using a django test runner.

            Useful in doctests involving django.
                test = DjangoTest()
                test.setUp()
                config = test.config        # optional
                test_dir = test.test_dir    # optional
                ...do tests...
                test.tearDown()
            
            Note: the database is always flushed.
        '''
        GaiaTest.setUp(self, config)
        self._is_setup = True   #? not sure if we need this!... TODO
        try:
            settings.configure(**self.config.get_django_settings())
        except RuntimeError, e:
            # Settings already configured: sometimes we want/need to change the settings, expecially from gaia to cengage tests
            self.change_settings(**config.get_django_settings())

        # If we don't have a database, create one (syncdb should be innocuous otherwise)
        # See https://docs.djangoproject.com/en/1.4/ref/django-admin/#django-admin-syncdb (Syncdb will not alter existing tables)
        call_command('syncdb', verbosity=0, interactive=False)
        call_command('flush', verbosity=0, interactive=False)

        from django.test.utils import setup_test_environment    # this must be doen here, *after* the settings.configure(above)
        setup_test_environment()    # configure templates and email

    def tearDown(self):
        if self._is_setup:
            from django.test.utils import teardown_test_environment
            teardown_test_environment()
            self._is_setup = False
        
        GaiaTest.tearDown(self)

    def change_settings(self, **kwargs):
        for key, new_value in kwargs.items():
            setattr(settings, key, new_value)

        # Force django syncdb to re-create the database after changing settings
        from django.db.models import loading
        loading.cache.loaded = False     
