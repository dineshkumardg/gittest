from gaia.error import GaiaCodingError

def import_class(class_name):
    ''' import a class by name (name is a fully-qualified string) and return it

        eg thing_class = import_class('gaia.thing.Thing')
    '''
    parts = class_name.split('.')
    module = ".".join(parts[:-1])

    try:
        m = __import__(module)
    except ImportError, e:
        raise GaiaCodingError('cannot import class for name (badly configured or bug in class code?)', class_name=class_name)

    for comp in parts[1:]:
        m = getattr(m, comp)

    return m
