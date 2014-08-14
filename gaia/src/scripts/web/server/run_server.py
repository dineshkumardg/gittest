#!/usr/bin/python2.7
# A standalone WSGI Server to run a Gaia App
import sys
import django.core.handlers.wsgi
#from django.core.servers.basehttp import AdminMediaHandler # Not supported in Django 1.4!!
from django.conf import settings
from server.cherrypy import wsgiserver     # This is a copy of cherrypy.wsgiserver
from server.translogger import TransLogger # This is a copy of Ian Bicking's Paste Translogger
from gaia.config.config import get_config
from gaia.log.log import Log

def run(config_name):
    config = get_config(config_name)
    settings.configure(**config.get_django_settings())
    print '=== using config:\n', str(config)

    log_name = 'qa_web_server'
    Log.configure_logging(log_name, config)
    logger = Log.get_logger(log_name)

    # app = AdminMediaHandler(django.core.handlers.wsgi.WSGIHandler()) # NOT Django 1.4 compatible
    app = django.core.handlers.wsgi.WSGIHandler()
    app = TransLogger(app, logger=logger)   # define the logger to avoid replacing gaia settings

    ip_address, port = config.qa_server.split(':')
    port = int(port)
    print "=== ..using ip_address, port", ip_address, port
    server = wsgiserver.CherryPyWSGIServer( (ip_address, port), app)
    server.start()


try:
    config_name = sys.argv[1]    # eg DEMO or STHA
    run(config_name)
except IndexError, e:
    print "Usage: run_server.py PROJECT_CODE"
    sys.exit(-1)
