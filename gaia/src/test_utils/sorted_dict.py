
from collections import OrderedDict

def sorted_dict(d):
    ''' return a dictionary sorted by key
        This is VERY useful in tests (so that dict comparisons are not
        order-sensitive).
    
        (ref http://docs.python.org/2/library/collections.html#collections.OrderedDict)
    '''
    return OrderedDict(sorted(d.items(), key=lambda t: t[0]))
