import copy
from gaia.log.log import Log
from gaia.utils.safe_unicode import safe_formatted_unicode


class _DomObject:
    ''' A Gaia Document Object Model object has an dom_id, a dom_name and Info.
        The dom_id and dom_name are copied into the info dict to allow a
        reversible transformation from the info to the object.
    '''
    def __init__(self, dom_id, dom_name, info):
        self._log = Log.get_logger(self)

        self.dom_id = dom_id
        self.dom_name = dom_name

        self.info = copy.copy(info)
        self.info['_dom_id'] = dom_id
        self.info['_dom_name'] = dom_name

    def __str__(self, **kwargs):
        ' does not reveal private attributes and safely handles unicode characters '
        if 'info' in kwargs:
            info = kwargs['info']
            del kwargs['info']
        else:
            info = copy.copy(self.info)

        del info ['_dom_id']
        del info ['_dom_name']

        extra = ''
        for key in sorted(kwargs):
            extra += '%s="%s", ' % (key, kwargs[key])

        return safe_formatted_unicode('%s(dom_id="%s", dom_name="%s", %sinfo="%s")', self.__class__.__name__, self.dom_id, self.dom_name, extra, info)
