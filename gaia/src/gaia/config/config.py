import os.path
import inspect
from gaia.config.config_errors import GaiaConfigurationError
from gaia.config.project_mixins import CHOProject, UAT_CHOProject, STHAProject, JamesDevProject, TushLinuxDevProject, TushPcDevProject, TushNewspaperProject
from gaia.config.platform_mixins import Ukandgaia07Platform, UkandgaiaPlatform, TusharPcPlatform, TusharLinuxPlatform, JamesLinuxPlatform
from gaia.config.django_mixins import CHOSettings, STHASettings, TUSH_PCSettings, TUSH_NEWS_PCSettings, TUSH_LinuxSettings, _ModelsOnlySettings, JamesLinuxDjangoSettings, UnittestSettings
from gaia.config.system_test_config import SystemTestConfig
from gaia.utils.try_cmd import try_cmd, CommandError
from gaia.utils.gaia_file import GaiaFile
from gaia.utils.errors_mixin import ErrorsMixin

_config_map = None


def get_config(config_name):
    ' A factory function to return a config/platform for a project. '
    global _config_map

    if not _config_map:
        _config_map = {}
        for configs in _live_configs, _uat_configs, _dev_configs, _special_configs:
            for cls in configs:
                _config_map[cls.CONFIG_NAME] = cls
        pass

    try:
        return _config_map[config_name]()
    except KeyError, e:
        raise GaiaConfigurationError('There is no configuration for "%s" (error="%s")' % (config_name, str(e)), known_config_names=_config_map.keys())


class _Config(ErrorsMixin):
    def __init__(self):
        ErrorsMixin.__init__(self)
        self.schema_fpath = os.path.join(self._schema_dir, self.schema_name)  # note: was dtd_fpath
        self.working_dir = os.path.join(self._working_dir, self.project_code)
        self._set_workspace()
        self._set_defaults()

    def _set_defaults(self):
        if self.image_file_ext in GaiaFile.image_types and self.image_file_ext not in GaiaFile.web_image_types:
            self.web_image_ftype = 'png'
        else:
            self.web_image_ftype = self.image_file_ext

        # The ChunkSearch Adapter provides article-based search with doc_info and is a sensible default.
        # You can override this per-project if something else is required.
        try:
            self.search_adapter_class_name
        except AttributeError:
            self.search_adapter_class_name = 'gaia.search.adapter.chunk_search_adapter.ChunkSearchAdapter'

    def _set_workspace(self):
        ' configure a standard working-space structure '
        self.inbox = os.path.join(self.working_dir, 'inbox')
        self.outbox = os.path.join(self.working_dir, 'outbox')
        self.imagebox = os.path.join(self.working_dir, 'imagebox')  # TODO remove?
        self.log_dir = os.path.join(self.working_dir, 'logs')
        self.egest_working_dir = os.path.join(self.working_dir, 'egest_working_dir')
        self.transfer_prep_dir = os.path.join(self.egest_working_dir, 'transfer_prep')  # TODO

    def __str__(self):
        return '\n' + '\n'.join(['\t%s=%s' % (x, y) for (x, y) in inspect.getmembers(self) if not x.startswith('__') and not x == 'check'])

    def check(self):
        if not os.path.exists(self.schema_fpath):
            self.add_error(GaiaConfigurationError('Schema file "%s" does not exist!' % self.schema_fpath))

        if not os.path.exists(self.working_dir):
            self.add_error(GaiaConfigurationError('Working directory "%s" does not exist!' % self.working_dir))

        if not os.path.exists(self.inbox):
            self.add_error(GaiaConfigurationError('Inbox directory "%s" does not exist!' % self.inbox))

        if not os.path.exists(self.outbox):
            self.add_error(GaiaConfigurationError('Outbox directory "%s" does not exist!' % self.outbox))

        if not os.path.exists(self.egest_working_dir):
            self.add_error(GaiaConfigurationError('Egest Work Area directory "%s" does not exist!' % self.egest_working_dir))

        if not os.path.exists(self.imagebox):
            self.add_error(GaiaConfigurationError('Imagebox directory "%s" does not exist!' % self.imagebox))

        if not os.path.exists(self.log_dir):
            self.add_error(GaiaConfigurationError('Log directory "%s" does not exist!' % self.log_dir))

        if self.search_adapter_class_name is None:
            self.add_error(GaiaConfigurationError('The search_adapter_class_name needs to be set to an appropriate class name!'))

        try:
            try_cmd(self.perl_fpath, '-h')
        except CommandError, e:
            self.add_error(GaiaConfigurationError('The configured perl_fpath "%s" does not point to a perl executable!' % self.perl_fpath))

        try:
            try_cmd(self.xmllint_fpath, '--version')
        except CommandError, e:
            self.add_error(GaiaConfigurationError('The configured xmllint_fpath "%s" does not point to a xmllint executable!' % self.xmllint_fpath))

        try:
            try_cmd(self.identify_fpath, '-version')
        except CommandError, e:
            self.add_error(GaiaConfigurationError('The configured identify_fpath "%s" does not point to a ImageMagick identify executable!' % self.identify_fpath))

        try:
            try_cmd(self.convert_fpath, '-version')
        except CommandError, e:
            self.add_error(GaiaConfigurationError('The configured convert_fpath "%s" does not point to a ImageMagick convert executable (err="%s"!' % (self.convert_fpath, str(e))))

        try:
            try_cmd(self.zip_fpath, '-h')
        except CommandError, e:
            self.add_error(GaiaConfigurationError('The configured zip_fpath "%s" does not point to a 7-Zip 7z executable!' % self.zip_fpath))

        self.raise_if_errors()


class _UatCHOConfig(_Config, UAT_CHOProject, CHOSettings, Ukandgaia07Platform):
    'this is close to live settings, with a few minor tweaks for User Acceptance Testing in the live environment'
    CONFIG_NAME = 'CHO_UAT'


class _LiveCHOConfig(_Config, CHOProject, CHOSettings, Ukandgaia07Platform):
    CONFIG_NAME = 'CHO'


class _LiveSTHAConfig(_Config, STHAProject, STHASettings, UkandgaiaPlatform):
    CONFIG_NAME = 'STHA'


class _TusharPcConfig(_Config, TushPcDevProject, TUSH_PCSettings, TusharPcPlatform):
    CONFIG_NAME = 'TUSH_PC'


class _TusharNewsPcConfig(_Config, TushNewspaperProject, TUSH_NEWS_PCSettings, TusharPcPlatform):
    CONFIG_NAME = 'TUSH_NEWS_PC'


class _TusharLinuxConfig(_Config, TushLinuxDevProject, TUSH_LinuxSettings, TusharLinuxPlatform):
    CONFIG_NAME = 'TUSH'


class _JamesLinuxConfig(_Config, JamesDevProject, JamesLinuxDjangoSettings, JamesLinuxPlatform):
    CONFIG_NAME = 'JAMES_LINUX'


class _UnittestConfig(UnittestSettings):
    ' Special minimal "config" for Django in memory tests'
    CONFIG_NAME = 'UNIT_TEST'
    outbox = ''

    def __str__(self):
        return '\n' + '\n'.join(['\t%s=%s' % (x, y) for (x, y) in inspect.getmembers(self) if not x.startswith('__') and not x == 'check'])


class _SystemTestConfig(SystemTestConfig):
    ''' Special config for System Tests.'''
    CONFIG_NAME = 'SYSTEM_TEST'


class _ModelsOnlyConfig(_ModelsOnlySettings):
    ' This is a special "non-config" config that is only here to dump models '
    CONFIG_NAME = '_MODELS_ONLY'

_live_configs = [_LiveCHOConfig, _LiveSTHAConfig]
_uat_configs = [_UatCHOConfig]
_dev_configs = [_TusharPcConfig, _TusharNewsPcConfig, _TusharLinuxConfig, _JamesLinuxConfig]
_special_configs = [_ModelsOnlyConfig, _UnittestConfig, _SystemTestConfig]
