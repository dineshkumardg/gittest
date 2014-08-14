#!/usr/bin/env python
import sys
from django.conf import settings
from gaia.config.config import get_config
from django.core.management import execute_from_command_line
from gaia.config.config_errors import GaiaConfigurationError

def usage():
    print 'Usage: manage.py PROJECT_CODE command command-args'
    print 'eg:    manage.py TUSH_PC syncdb'
    print 'eg:    manage.py TUSH_PC sqlall qa'
    print 'eg:    manage.py TUSH_PC sqlall index # for gaia.dom.index App' 
    print 'eg:    manage.py DG sqlall for using DG config'

if len(sys.argv) == 1:
    usage()
    execute_from_command_line(sys.argv)
    sys.exit()

if len(sys.argv) > 1:
#    if sys.argv[1] == 'help':
#        execute_from_command_line(sys.argv)
#        sys.exit()
    
    project_code = sys.argv[1]
    try:
        config = get_config(project_code)
        settings.configure(**config.get_django_settings())
        del sys.argv[1]
        execute_from_command_line(sys.argv)
    except GaiaConfigurationError, e:
        print 'Error: %s' % str(e)
        usage()
