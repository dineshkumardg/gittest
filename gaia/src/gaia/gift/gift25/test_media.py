import doctest
suite = doctest.DocFileSuite('test_media.py')

if __name__ == '__main__':
    doctest.testfile("test_media.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import media, vault_link
>>> from lxml import etree

>>> # A: TEST IMAGE  =======================================================
>>> vault_link = vault_link.vault_link(
...     _link_type='link_type',
...     term_id='term_id',
...     term_source='term_source',
...     _category='category',
...     _action='action',
...     where_path='where_path',
...     _target='target'
... )

>>> image = media.image(
...     data_type='data_type',
...     height='height',
...     width='width',
...     image_type='image_type',
...     layout='layout',
...     color_mode='color_mode',
...     folio='folio',
...     sequence='sequence',
...     vault_link=vault_link
...     )

>>> print etree.tostring(image, pretty_print=True)
<media:image xmlns:media="http://www.gale.com/goldschema/media" data-type="data_type" width="width" height="height" image-type="image_type" layout="layout" color-mode="color_mode" folio="folio" sequence="sequence">
  <vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
    <vault-link:link-type>link_type</vault-link:link-type>
    <vault-link:link-category term-id="term_id" term-source="term_source">category</vault-link:link-category>
    <vault-link:action>action</vault-link:action>
    <vault-link:where>
      <vault-link:path>where_path</vault-link:path>
    </vault-link:where>
    <vault-link:select>
      <vault-link:document-nodes>
        <vault-link:target>target</vault-link:target>
      </vault-link:document-nodes>
    </vault-link:select>
  </vault-link:vault-link>
</media:image>
<BLANKLINE>

'''
