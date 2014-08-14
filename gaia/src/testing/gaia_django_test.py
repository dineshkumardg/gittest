import os
import sys
import inspect
from testing.django_test import DjangoTest
from testing.unit_test_config import DjangoConfig


class _GaiaUnitTestConfig(DjangoConfig):
    ROOT_URLCONF = 'gaia_web.urls'

    INSTALLED_APPS = (
        'qa',
        'gaia.dom.index',
        ) + DjangoConfig.INSTALLED_APPS  # WARNING: the *order* of this is important!

    if sys.platform == 'win32':
        TEMPLATE_DIRS = ('/GIT_REPOS/gaia/src/qa/templates/',)
    else:
        home = os.environ['HOME']
        TEMPLATE_DIRS = (os.path.join(home, 'GIT_REPOS/gaia/src/qa/templates/'), )

    CONFIG_NAME = 'UNIT_TEST'
    WEB_ROOT='/GAIA/WEB_ROOT/gaia'

    CACHE_MIDDLEWARE_SECONDS = 0

    def get_django_settings(self):
        return {x: y for x, y in inspect.getmembers(self) if x[0].isupper()}

class GaiaDjangoTest(DjangoTest):
    def setUp(self):
        DjangoTest.setUp(self, _GaiaUnitTestConfig())

        # this has to come into scope after setup!
        from django.test.utils import setup_test_environment
        setup_test_environment()  # configure templates and email, else Client.context lost
