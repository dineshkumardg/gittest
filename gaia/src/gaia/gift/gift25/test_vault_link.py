import doctest
suite = doctest.DocFileSuite('test_vault_link.py')

if __name__ == '__main__':
    doctest.testfile("test_vault_link.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import vault_link
>>> from lxml import etree

>>> # A: TEST OPTIONAL VAULT_LINK ELEMENTS  =======================================================
>>> vault_link_element = vault_link.vault_link()
>>> print etree.tostring(vault_link_element, pretty_print=True)
<vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking"/>
<BLANKLINE>

>>> # B: TEST ALL VAULT_LINK ELEMENTS  =======================================================
>>> vault_link_element = vault_link.vault_link(   '_link_type',
...                                               'term_id',
...                                               'term_source',
...                                               '_category',
...                                               '_action',
...                                               'where_path',
...                                               '_target')
>>> print etree.tostring(vault_link_element, pretty_print=True)
<vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
  <vault-link:link-type>_link_type</vault-link:link-type>
  <vault-link:link-category term-id="term_source" term-source="_category">_action</vault-link:link-category>
  <vault-link:data-type>term_id</vault-link:data-type>
  <vault-link:action>where_path</vault-link:action>
  <vault-link:where>
    <vault-link:path>_target</vault-link:path>
  </vault-link:where>
</vault-link:vault-link>
<BLANKLINE>

>>> # C: TEST LINK_TYPE  =======================================================
>>> link_type = vault_link.link_type('link_type')
>>> print etree.tostring(link_type, pretty_print=True)
<vault-link:link-type xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">link_type</vault-link:link-type>
<BLANKLINE>

>>> # D: TEST ACTION  =======================================================
>>> action = vault_link.action('action')
>>> print etree.tostring(action, pretty_print=True)
<vault-link:action xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">action</vault-link:action>
<BLANKLINE>

>>> # E: TEST WHERE  =======================================================
>>> where = vault_link.where('where')
>>> print etree.tostring(where, pretty_print=True)
<vault-link:where xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">where</vault-link:where>
<BLANKLINE>

>>> # F: TEST PATH  =======================================================
>>> path = vault_link.path('path')
>>> print etree.tostring(path, pretty_print=True)
<vault-link:path xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">path</vault-link:path>
<BLANKLINE>

>>> # G: TEST LINK_CATEGORY  =======================================================
>>> link_category = vault_link.link_category('link_category')
>>> print etree.tostring(link_category, pretty_print=True)
<vault-link:link-category xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">link_category</vault-link:link-category>
<BLANKLINE>

>>> # H: TEST SELECT  =======================================================
>>> select = vault_link.select('select')
>>> print etree.tostring(select, pretty_print=True)
<vault-link:select xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">select</vault-link:select>
<BLANKLINE>

>>> # I: TEST DOCUMENT_NODES  =======================================================
>>> document_nodes = vault_link.document_nodes('document_nodes')
>>> print etree.tostring(document_nodes, pretty_print=True)
<vault-link:document-nodes xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">document_nodes</vault-link:document-nodes>
<BLANKLINE>

>>> # J: TEST TARGET  =======================================================
>>> target = vault_link.target('target')
>>> print etree.tostring(target, pretty_print=True)
<vault-link:target xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">target</vault-link:target>
<BLANKLINE>

'''
