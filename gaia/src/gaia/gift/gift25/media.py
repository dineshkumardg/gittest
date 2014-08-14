from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker, attr
from lxml.builder import ElementMaker


class _Media(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self, namespace='http://www.gale.com/goldschema/media', nsmap={'media' : 'http://www.gale.com/goldschema/media', }, **kwargs)

def image(data_type=None, height=None, width=None, image_type=None, layout=None, color_mode=None, folio=None, sequence=None, vault_link=None, _caption=None, _descriptive_indexing=None):
    image_list = []

    if data_type is not None:
        image_list.append(attr('data-type', data_type))

    if width is not None:
        image_list.append(attr('width', width))

    if height is not None:
        image_list.append(attr('height', height))

    if image_type is not None:
        image_list.append(attr('image-type', image_type))

    if layout is not None:
        image_list.append(attr('layout', layout))

    if color_mode is not None:
        image_list.append(attr('color-mode', color_mode))

    if folio is not None:
        image_list.append(attr('folio', folio))

    if sequence is not None:
        image_list.append(attr('sequence', sequence))

    if vault_link is not None:
        image_list.append(vault_link)

    if _caption is not None:
        image_list.append(
            E.caption(_caption)
        )

    if _descriptive_indexing is not None:
        image_list.append(_descriptive_indexing)

    return _image(
        *image_list
        )

def audio(filesize, data_type, audio_type, descriptive_indexing, vault_link, _title):
    return _audio(  attr('filesize', unicode(filesize)),
                    attr('data-type', data_type),
                    attr('audio-type', audio_type),
                    descriptive_indexing,
                    vault_link,
                    title(_title)
                    )

E = _Media()
_image = E.image
_audio = E.audio
title = E.title
