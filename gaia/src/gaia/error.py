class GaiaError(Exception):
    ''' A base class for all application errors.
        
        Note that you can supply parameters as keyword arguments, and
        these will appear in a bracketed list in the error message.
        You can use this for general info and to pass on error detail, eg:
        
            raise GaiaError(missing_tag=xpath, error=e)
        
        *** Please make sure that the keyword names you use are HUMAN-FRIENDLY! ***
    '''
    
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        self.kwargs = kwargs

        #Hmm.. something is doing this..somewhere!..leave out/OK for now.
        #if not msg and not kwargs:
            #raise GaiaCodingError('Tried to create a GaiaError without any msg or kwargs!')
        
    def __str__(self):
        err_prefix = self.__class__.__name__
        if self.msg:
            msg = '%s: %s' % (err_prefix, self.msg)
        else:
            msg = '%s: ' % err_prefix

        if self.kwargs:
            if self.msg:    # if there's no message, then the message is given by the kwargs, so no brackets required.
                msg += ' ('

            for error_indicator in self.kwargs:
                try:
                    msg += '%s="%s", ' % (error_indicator, str(self.kwargs[error_indicator]))
                except UnicodeEncodeError, e:
                    # if we have unicode data, this will replace non-ascii chars with "?" so that we can print most of it.
                    msg += '%s="%s", ' % (error_indicator, str(self.kwargs[error_indicator].encode('ascii','replace')))

            msg = msg[:-2]# strip the superfluous ", "

            if self.msg:
                msg += ')'

        return msg
    
class GaiaSystemError(GaiaError):
    pass
    
class GaiaCodingError(GaiaSystemError):
    pass
    
class GaiaErrors(GaiaError):
    'This collects together a set of GaiaError objects'

    def __init__(self, *errors):
        self.errors = list(errors)

    def __str__(self):
        return '\n'.join([str(e) for e in self.errors])

    def append(self, err):
        self.errors.append(err)

class MCodeError(GaiaError):
    pass
