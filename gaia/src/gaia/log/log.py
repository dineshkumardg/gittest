import os
import logging.handlers

#CRITICAL 	50
#ERROR   	40
#WARNING 	30
#INFO   	20
#DEBUG  	10
#NOTSET 	0

class _GaiaFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == Log.ENTER:
            level = 'DEBUG: >>>'
        elif record.levelno == Log.EXIT:
            level = 'DEBUG: <<<'
        elif record.levelno == logging.DEBUG:
            level = 'DEBUG: ...'
        elif record.levelno == logging.INFO:
            level = 'INFO:  ...'
        elif record.levelno == logging.WARNING:
            level = 'WARN:  ooo'
        elif record.levelno == logging.ERROR:
            level = 'ERROR: ***'
        elif record.levelno == logging.CRITICAL:
            level = 'CRIT!: ***'
        else:
            level = record.levelname    #?

        #return '[%s] %s:%s(): %s %s' % (self.formatTime(record), record.name, record.funcName, level, record.getMessage())
        #return '%s %-60s\t[%s %s:%s()]' % (level, record.getMessage(), self.formatTime(record), record.name, record.funcName,)
        return '[%s] %s %s.%s(): %s' % (self.formatTime(record), level, record.name, record.funcName, record.getMessage(),)

class Log(logging.Logger):
    ENTER = 11 # these 2 levels should be visible at DEBUG level 
    EXIT  = 12

    def __init__(self, name):
        logging.Logger.__init__(self, name)

    @classmethod
    def get_logger(cls, for_object):
        ''' WARNING: This logger uses kwargs differently to the standard logger!
        '''
        return logging.getLogger(str(for_object.__class__.__name__))

    @classmethod
    def configure_logging(cls, name, config, multi_process=False, rollover=True):
        ''' Configure logging for the Gaia system.
            and return the name of the log file.

            "multi_process" should be set if separate logs are required per-process.
            "rollove" will make the logs rollover.

            This is for use in the main, top-level, of the process only.
            Configures the root logger's handlers (that sub loggers will inherit),
            and makes this the class for all Logger objects.
        '''
        if multi_process:
            fpath = os.path.join(config.log_dir, '%s_%s.log' % (name, str(os.getpid())))
        else:
            fpath = os.path.join(config.log_dir, '%s.log' % name)

        logging.setLoggerClass(Log)

        if rollover:
            h = logging.handlers.RotatingFileHandler(fpath, backupCount=99)
            h.doRollover() # rollover on re-run only 
        else:
            h = logging.FileHandler(fpath) #?   

        #formatter = logging.Formatter('[%(asctime)s] %(levelname)7s %(name)20s: %(message)s')
        #formatter = logging.Formatter('%(levelname)7s: %(message)s\t\t[%(asctime)s %(name)s]')
        formatter = _GaiaFormatter()
        h.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.addHandler(h)
        logger.setLevel(config.log_level)

        return fpath

    def _args_str(self, *args, **kwargs):
        msg=''

        if args:
            for arg in args:
                try:
                    msg += '%s ' % str(arg)
                except UnicodeEncodeError, e:
                    # if we have unicode data, this will replace non-ascii chars with "?" so that we can print most of it.
                    msg += '%s ' % str(arg.encode('ascii', 'replace'))
            msg = msg[:-1] # trim the trailing extra space

        if kwargs:
            if args:
                msg += ' ('
            else:
                msg += '('

            for k in kwargs:
                try:
                    msg += '%s="%s", ' % (k, str(kwargs[k]))
                except UnicodeEncodeError, e:
                    # if we have unicode data, this will replace non-ascii chars with "?" so that we can print most of it.
                    try:
                        msg += '%s="%s", ' % (k, str(kwargs[k].encode('ascii', 'replace')))
                    except AttributeError, e:
                        # eg oAttributeError: UnicodeThing instance has no attribute 'encode'
                        if 'encode' in str(e):
                            msg += '%s="_cannot_print_unicode_data_for_object_id:%s", ' % (k, id(kwargs[k]))
            msg = msg[:-2] + ')'

        return msg

    def enter(self, *args, **kwargs):
        self.log(self.ENTER, msg=self._args_str(*args, **kwargs))

    def exit(self, *args, **kwargs):
        self.log(self.EXIT, msg=self._args_str(*args, **kwargs))

    def debug(self, *args, **kwargs):
        self.log(logging.DEBUG, msg=self._args_str(*args, **kwargs))

    def info(self, *args, **kwargs):
        self.log(logging.INFO, msg=self._args_str(*args, **kwargs))

    def warning(self, *args, **kwargs):
        self.log(logging.WARNING, msg=self._args_str(*args, **kwargs))

    def error(self, *args, **kwargs):
        self.log(logging.ERROR, msg=self._args_str(*args, **kwargs))

    def critical(self, *args, **kwargs):
        self.log(logging.CRITICAL, msg=self._args_str(*args, **kwargs))


    def findCaller(self):   # modified from logging.__init__.py
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
            f = f.f_back     # CENGAGE: The stack will always have a minimum of 3 frames, ie: log();_log();findCaller();
            f = f.f_back     # CENGAGE: .. so this is safe.
            
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv
    
    def _log(self, level, msg, args, exc_info=None, extra=None): # modified from logging.__init__.py
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller throws an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        if msg is None:         # CENGAGE: added for enter and exit levels.
            msg = func + '()'   # CENGAGE

        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.handle(record)

# The following is copied from logging.__init__.py

# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.
#
import sys
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "gaia%slog%slog%s" % (os.sep, os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back
