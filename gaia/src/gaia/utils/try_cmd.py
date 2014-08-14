import subprocess
import logging
from gaia.error import GaiaError

class CommandError(GaiaError):
    pass

class CommandFailed(CommandError):

    def __init__(self, cmd, retcode, stdout, stderr):
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr
        msg = 'cmd="%s" (retcode="%s", stdout="%s", stderr="%s")' % (str(cmd), retcode, stdout, stderr)
        GaiaError.__init__(self, msg)

class CommandStartError(CommandError):
    
    def __init__(self, cmd, err):
        msg = 'Could not run command (cmd="%s", cause="%s")' % (str(cmd), str(err))
        CommandError.__init__(self, msg)

def try_cmd(*cmd):
    'try to run a command, if it fails a CommandError (or subclass) error is raised. '
    logging.debug('... About to try_cmd: %s' % str(cmd))
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        retcode = process.returncode
    
    except OSError, e:
        raise CommandStartError(cmd, e)
    
    except ValueError, e:
        raise CommandStartError(cmd, e)

    if retcode != 0:
        raise CommandFailed(cmd, retcode, stdout, stderr)

    logging.debug('... try_cmd returned stdout: "%s"' % stdout)
    return stdout
