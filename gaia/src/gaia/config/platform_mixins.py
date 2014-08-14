'''
    Mixins used to set parameters for specific environments/platforms
'''
import logging


class _LinuxPlatform:
    perl_fpath = '/usr/bin/perl'
    xmllint_fpath = '/usr/bin/xmllint'
    #imagemagick_fpath = '/usr/bin/identify'
    identify_fpath = '/usr/bin/identify'
    convert_fpath = '/usr/bin/convert'
    zip_fpath = '/usr/bin/7z'

    _schema_dir = '/etc/gaia/dtds' #?  # not for direct use.
    _working_dir = '/var/gaia' #? # use subdirs per project within this..

class _WindowsPlatform:
    perl_fpath     = r'c:\Program Files\Git\bin\perl.exe'
    xmllint_fpath  = r'c:\xmllint\bin\xmllint.exe'
    identify_fpath = r'c:\Program Files\ImageMagick\identify.exe'
    convert_fpath  = r'c:\Program Files\ImageMagick\convert.exe'
    zip_fpath      = r'c:\Program Files\7-Zip\7z.exe'

    _schema_dir    = r'c:\GAIA\dtds'
    _working_dir   = r'c:\GAIA\WORK'

class _ZmqLocal:    # ref: http://api.zeromq.org/2-1:zmq-tcp
    # ZeroMq endpoints: there are 2 endpoints for each message queue.
    # we're calling these 2 ends "send" and "receive".
    # TODO: simplify to one address (they are now both identical).
    # Note; bind requires numeric ipv4 address (connect can use dns name).
    ingest_job_sockets = {
        'request': {'send': 'tcp://127.0.0.1:5551', 'recv': 'tcp://127.0.0.1:5551',},   # push/pull
        'reply':   {'send': 'tcp://127.0.0.1:5552', 'recv': 'tcp://127.0.0.1:5552',},   # push/pull
    }

    egest_job_sockets = {
        'request':  {'send': 'tcp://127.0.0.1:6551', 'recv': 'tcp://127.0.0.1:6551',},  # push/pull
        'reply':    {'send': 'tcp://127.0.0.1:6552', 'recv': 'tcp://127.0.0.1:6552',},  # push/pull
    }

    management_sockets = {
        'command':  {'send': 'tcp://127.0.0.1:7551', 'recv': 'tcp://127.0.0.1:7551',},  # pub/sub
        'status':   {'send': 'tcp://127.0.0.1:7552', 'recv': 'tcp://127.0.0.1:7552',},  # pub/sub
    }


class Ukandgaia07Platform(_LinuxPlatform, _ZmqLocal):
    ' settings for our LIVE, PRODUCTION system on ukandgaia07'
    log_level = logging.INFO # TEMP FOR UAT ONLY TODO: change this to WARNING for live runs?
    _schema_dir = '/home/gaia/GIT_REPOS/gaia/src/gaia/config/dtds'
    _working_dir = '/GAIA' # I think this is wrong, but we'll have to review this later :( sorry.


class UkandgaiaPlatform(_LinuxPlatform, _ZmqLocal):
    ' settings for a live, Production system on ukandgaia'
    log_level = logging.INFO


class TusharPcPlatform(_WindowsPlatform, _ZmqLocal):
    log_level = logging.DEBUG
    _schema_dir = r'c:\GIT_REPOS\gaia\src\gaia\config\dtds'
    #qa_server_port = 8887# TMP TODO?


class TusharLinuxPlatform(_LinuxPlatform, _ZmqLocal):
    log_level = logging.DEBUG
    _schema_dir = '/home/tushar/GIT_REPOS/gaia/src/gaia/config/dtds'
    _working_dir = '/home/tushar/GAIA_WORKING_DATA'


class JamesLinuxPlatform(_LinuxPlatform, _ZmqLocal):
    log_level = logging.DEBUG
    _schema_dir = '/home/jsears/GIT_REPOS/gaia/src/gaia/config/dtds'
    _working_dir = '/home/jsears/GAIA_WORKING_DATA'
