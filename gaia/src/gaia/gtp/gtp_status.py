
# er..this is a bit over the top, but it's _one_ way to create a fully featured
# Enumeration type ...  not sure I like it, but it'll do for now. :(
class _StatusEnumerationMeta(type):
    _status_list = list(enumerate(['READY', 'PROCESSING', 'NOT_READY']))
    _status = {name: number for number, name in _status_list}

    def __new__(meta, class_name, bases, class_dict):
        ' Return a class which includes the status values as *class* attributes '

        for number, status_name in enumerate(['READY', 'PROCESSING', 'NOT_READY']):
            class_dict[status_name] = number

        #class_dict['_status'] = meta._status
        class_dict['_status_list'] = meta._status_list
        return super(_StatusEnumerationMeta, meta).__new__(meta, class_name, bases, class_dict)

    def __init__(cls, name, bases, dct):
        super(_StatusEnumerationMeta, cls).__init__(name, bases, dct)


class GtpStatus(object):
    ' Handles "Gaia Transfer Protocol" (ref wiki) status features '
    __metaclass__ = _StatusEnumerationMeta

    READY_FNAME = '_status_READY.txt'
    PROCESSING_FNAME = '_status_PROCESSING.txt'

    def __init__(self, status_number):
        self._status_number = status_number

    def __str__(self):
        ' return a string form of a status '
        return self._status_list[self._status_number][1]

    @classmethod
    def status(cls, fnames):
        ' given a set of file names in a folder, return the status '

        if cls.PROCESSING_FNAME in fnames:
            return cls.PROCESSING
        elif cls.READY_FNAME in fnames:
            return cls.READY
        else:
            return cls.NOT_READY

    @classmethod
    def is_ready(cls, fnames):
        return cls.status(fnames) == cls.READY

    @classmethod
    def is_processing(cls, fnames):
        return cls.status(fnames) == cls.PROCESSING
