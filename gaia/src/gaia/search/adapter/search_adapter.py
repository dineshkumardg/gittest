from abc import ABCMeta, abstractmethod

#class GaiaDomAdapter(metaclass=ABCMeta):   # py3.2 syntax
class SearchAdapter:
    __metaclass__ = ABCMeta                 # py2.7 syntax
    ''' A SearchAdapter is used to adapt a project's data
        into searchable SearchObjects.
    '''

    @abstractmethod
    def get_search_objects(self):
        pass  # return a list of SearchObjects
