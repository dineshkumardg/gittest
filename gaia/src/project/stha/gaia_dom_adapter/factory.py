import gaia.dom.adapter.factory
import project.stha.gaia_dom_adapter.stha

class Factory(gaia.dom.adapter.factory.Factory):
    ''' return a suitable CHO Gaia DOM Adapter _class_ for a file name. 
        STHA has only one type of data.
        Note:  a class factory not an object factory
    '''
    _adapters = {'stha': project.stha.gaia_dom_adapter.stha.Stha, }
    
    @classmethod
    def _adapter_type(cls, fname):
        ' return a project-specific key (eg a document type) to lookup an adapter.'
        return 'stha'
