class ChoNamespaces:
    '''
    the aim of this class is to remove all the following namespaces from any xml string.
    '''

    xml_ns = ['xmlns:dir="http://www.gale.com/goldschema/dir"',
        'xmlns:essay="http://www.gale.com/goldschema/essay"',
        'xmlns:etoc="http://www.gale.com/goldschema/etoc"',
        'xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc"',
        'xmlns:gold="http://www.gale.com/gold"',
        'xmlns:index="http://www.gale.com/goldschema/index"',
        'xmlns:list="http://www.gale.com/goldschema/list"',
        'xmlns:math="http://www.w3.org/1998/Math/MathML"',
        'xmlns:media="http://www.gale.com/goldschema/media"',
        'xmlns:meta="http://www.gale.com/goldschema/metadata"',
        'xmlns:mla="http://www.gale.com/goldschema/mla"',
        'xmlns:pres="http://www.gale.com/goldschema/pres"',
        'xmlns:pub-meta="http://www.gale.com/goldschema/pub-meta"',
        'xmlns:shared="http://www.gale.com/goldschema/shared"',
        'xmlns:table="http://www.gale.com/goldschema/table"',
        'xmlns:tt="http://www.w3.org/ns/ttml"',
        'xmlns:vault-link="http://www.gale.com/goldschema/vault-linking"',
        'xmlns:verse="http://www.gale.com/goldschema/verse"',
        'xmlns:xatts="http://www.gale.com/goldschema/xatts"',
        'xmlns:xlink="http://www.w3.org/1999/xlink"',]

    @classmethod
    def remove_ns(cls, xml):
        # lxml puts namespaces at element level - this causes LST to break!

        ns_free_xml = xml
        for xmlns in cls.xml_ns:
            ns_free_xml = ns_free_xml.replace(' ' + xmlns, '')

        return ns_free_xml
