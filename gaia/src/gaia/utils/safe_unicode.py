
def safe_unicode(unicode_string):
    ''' a utility function to safely transform a (possibly) unicode string to an ascii/printable string

        Note that you do NOT have to use this if you are using the gaia.Log class.
    '''
    try:
        return str(unicode_string)
    except UnicodeEncodeError, e:
        # if we have unicode data, this will replace non-ascii chars with "?" so that we can print most of it.
        return str(unicode_string.encode('ascii', 'replace'))

def safe_formatted_unicode(format_string, *unicode_args):
    ''' a handy function when you want to create a formatted string
        with a number of possibly unicode string parameters

        (see the test for an example)
        Note that you do NOT have to use this if you are using the gaia.Log class with keyword args (as you should be!)
    '''
    return format_string % tuple([safe_unicode(unicode_string) for unicode_string in unicode_args])
