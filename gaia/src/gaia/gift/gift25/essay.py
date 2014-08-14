from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker, attr
from lxml.builder import ElementMaker


class _Essay(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self,
                              namespace='http://www.gale.com/goldschema/essay',
                              nsmap={'essay' : 'http://www.gale.com/goldschema/essay', },
                              **kwargs)

def div_container(document_segment_type, term_id, term_source, elements):
    return E.div(
        attr('document-segment-type', document_segment_type),
        attr('term-id', term_id),
        attr('term-source', term_source),
        *elements
        )

def div_related_doc(document_segment_type, term_id, term_source, _complex_meta=None, essay_p=None, shared_media=None, vault_link=None, vault_link_related_doc=None):
    args = []

    #import pdb; pdb.set_trace();
    if _complex_meta is not None:
        args.append(complex_meta(
            *_complex_meta
            )
        )

    if essay_p is not None:
        args.append(essay_p)

    if shared_media is not None:
        args.append(shared_media)

    if vault_link is not None:
        args.append(vault_link)

    if vault_link_related_doc is not None:
        for vault_link in vault_link_related_doc:
            args.append(vault_link)

    return E.div(
        attr('document-segment-type', document_segment_type),
        attr('term-id', term_id),
        attr('term-source', term_source),
        *args
        )

def div(document_segment_type, term_id, term_source, complex_meta=None, shared_media=None, vault_link0=None, vault_link1=None, essay_p=None, _div=None, _ocr=None, elements=None, vault_link2=None):
    args = []

    if complex_meta is not None:
        args.append(complex_meta)

    if essay_p is not None:
        args.append(essay_p)

    if shared_media is not None:
        args.append(shared_media)

    if vault_link0 is not None:  # TODO rename to something that reflects caller
        args.append(vault_link0)

    if vault_link1 is not None:  # TODO rename to something that reflects caller
        args.append(vault_link1)

    if vault_link2 is not None:  # TODO rename to something that reflects caller - i.e. relatedDocument
        for vault_link in vault_link2:
            args.append(vault_link)

    if _div is not None:
        args.append(_div)

    if _ocr is not None:
        args.append(_ocr)

    if elements is not None:  # arbitrary list
        for element in elements:
            if element is not None:
                args.append(element)

    return E.div(
        attr('document-segment-type', document_segment_type),
        attr('term-id', term_id),
        attr('term-source', term_source),
        *args
        )

def ocr_text(position, word):
    return E.ocr_text(
        attr('position', position),
        word
    )

E = _Essay()
p = E.p
complex_meta = E.complex_meta
