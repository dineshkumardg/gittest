from lxml.builder import ElementMaker


def attr(name, *args):
    ''' creates attributes on an element '''
    return { name:' '.join(args) }

class HyphenElementMaker(ElementMaker):
    def __getattr__(self, tag):
        ''' allows e factory to produce hyphens '''
        tag = tag.replace('_', '-')
        return ElementMaker.__getattr__(self, tag)
