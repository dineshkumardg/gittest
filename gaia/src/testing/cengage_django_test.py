from testing.django_test import DjangoTest
from testing.unit_test_config import DjangoConfig


class _CengageUnitTestConfig(DjangoConfig):
    INSTALLED_APPS =  (
        'cengage.asset_id',
        ) + DjangoConfig.INSTALLED_APPS  # WARNING: the *order* of this is important!

    # looks like we need these just to keep django happy...
    ROOT_URLCONF = 'NONE.urls'
    TEMPLATE_DIRS = 'no_templates_being_used_here'


class CengageDjangoTest(DjangoTest):
    def setUp(self):
        DjangoTest.setUp(self, _CengageUnitTestConfig())
