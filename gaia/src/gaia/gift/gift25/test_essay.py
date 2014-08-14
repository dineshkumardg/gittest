import doctest
suite = doctest.DocFileSuite('test_essay.py')

if __name__ == '__main__':
    doctest.testfile("test_essay.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import essay, meta, shared, media, vault_link
>>> from lxml import etree

>>> # A: TEST OPTIONAL DIV ELEMENTS  =======================================================
>>> divs = essay.div(
...     'document_segment_type0',
...     'term_id0',
...     'term_source0'
...     )
>>> essay_div_container = essay.div_container(
...     'document_segment_type1',
...     'term_id1',
...     'term_source1',
...     divs
...     )

>>> print etree.tostring(essay_div_container, pretty_print=True)
<essay:div xmlns:essay="http://www.gale.com/goldschema/essay" document-segment-type="document_segment_type1" term-id="term_id1" term-source="term_source1"/>
<BLANKLINE>

>>> # B: TEST ALL DIV ELEMENTS  =======================================================
>>> complex_meta=essay.complex_meta(
...      meta.page_id_number('page_id_number')
... )
>>> shared_media=shared.media(
...     media.image(
...         data_type='data_type',
...         height='height',
...         width='width',
...         image_type='image_type',
...         layout='layout',
...         color_mode='color_mode',
...         folio='folio',
...         sequence='sequence', 
...         vault_link=vault_link.vault_link(
...             '_link_type',
...             'term_id',
...             'term_source',
...             '_category',
...             '_action',
...             'where_path',
...             '_target')
...         )
...     )
>>> vault_link0=vault_link.vault_link(
...     '_link_type0',
...     'term_id0',
...     'term_source0',
...     '_category0',
...     '_action0',
...     'where_path0',
...     '_target0')
>>> vault_link1=vault_link.vault_link(
...     '_link_type1',
...     'term_id1',
...     'term_source1',
...     '_category1',
...     '_action1',
...     'where_path1',
...     '_target1')
>>> vault_link2=None
>>> essay_p = essay.p(
...     'document_segment_type0',
...     'term_id0',
...     'term_source0',
...     'full_text')
>>> divs = essay.div(
...     'document_segment_type1',
...     'term_id1',
...     'term_source1', 
...     complex_meta,
...     shared_media,
...     vault_link0,
...     vault_link1,
...     vault_link2,
...     essay_p)
>>> essay_div_container = essay.div_container(document_segment_type='document_segment_type2', term_id='term_id2', term_source='term_source2', elements=divs)

>>> print etree.tostring(essay_div_container, pretty_print=True)
<essay:div xmlns:essay="http://www.gale.com/goldschema/essay" document-segment-type="document_segment_type2" term-id="term_id2" term-source="term_source2">
  <essay:complex-meta>
    <meta:page-id-number xmlns:meta="http://www.gale.com/goldschema/metadata">page_id_number</meta:page-id-number>
  </essay:complex-meta>
  <shared:media xmlns:shared="http://www.gale.com/goldschema/shared">
    <media:image xmlns:media="http://www.gale.com/goldschema/media" data-type="data_type" width="width" height="height" image-type="image_type" layout="layout" color-mode="color_mode" folio="folio" sequence="sequence">
      <vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
        <vault-link:link-type>_link_type</vault-link:link-type>
        <vault-link:link-category term-id="term_source" term-source="_category">_action</vault-link:link-category>
        <vault-link:data-type>term_id</vault-link:data-type>
        <vault-link:action>where_path</vault-link:action>
        <vault-link:where>
          <vault-link:path>_target</vault-link:path>
        </vault-link:where>
      </vault-link:vault-link>
    </media:image>
  </shared:media>
  <vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
    <vault-link:link-type>_link_type0</vault-link:link-type>
    <vault-link:link-category term-id="term_source0" term-source="_category0">_action0</vault-link:link-category>
    <vault-link:data-type>term_id0</vault-link:data-type>
    <vault-link:action>where_path0</vault-link:action>
    <vault-link:where>
      <vault-link:path>_target0</vault-link:path>
    </vault-link:where>
  </vault-link:vault-link>
  <vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
    <vault-link:link-type>_link_type1</vault-link:link-type>
    <vault-link:link-category term-id="term_source1" term-source="_category1">_action1</vault-link:link-category>
    <vault-link:data-type>term_id1</vault-link:data-type>
    <vault-link:action>where_path1</vault-link:action>
    <vault-link:where>
      <vault-link:path>_target1</vault-link:path>
    </vault-link:where>
  </vault-link:vault-link>
  <essay:p>document_segment_type0term_id0term_source0full_text</essay:p>
</essay:div>
<BLANKLINE>

'''
