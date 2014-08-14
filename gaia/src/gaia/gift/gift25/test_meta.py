import doctest
suite = doctest.DocFileSuite('test_meta.py')

if __name__ == '__main__':
    doctest.testfile("test_meta.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import meta
>>> import gaia.gift.gift25 
>>> from lxml import etree

>>> # TEST OPTIONAL DOCUMENT_IDS =======================================================
>>> document_ids = meta.document_ids()
>>> print etree.tostring(document_ids, pretty_print=True)
<meta:document-ids xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST ALL DOCUMENT_IDS =======================================================
>>> document_ids = meta.document_ids(_type0='_type0', _value0='_value0', _type1='_type1', _value1='_value1')
>>> print etree.tostring(document_ids, pretty_print=True)
<meta:document-ids xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:id type="_type0">
    <meta:value>_value0</meta:value>
  </meta:id>
  <meta:id type="_type1">
    <meta:value>_value1</meta:value>
  </meta:id>
</meta:document-ids>
<BLANKLINE>

>>> # TEST OPTIONAL DESCRIPTIVE_INDEXING =======================================================
>>> descriptive_indexing = meta.descriptive_indexing()
>>> print etree.tostring(descriptive_indexing, pretty_print=True)
<meta:descriptive-indexing xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST OPTIONAL SOURCE_CITIATION_GROUP =======================================================
>>> source_citation_group = meta.source_citation_group()
>>> print etree.tostring(source_citation_group, pretty_print=True)
<meta:source-citation-group xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST OPTIONAL DOCUMENT_TITLES =======================================================
>>> document_titles = meta.document_titles()
>>> print etree.tostring(document_titles, pretty_print=True)
<meta:document-titles xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST ALL DOCUMENT_TITLES =======================================================
>>> document_titles = meta.document_titles('_title_display', '_title_sort', '_title_open_url')
>>> print etree.tostring(document_titles, pretty_print=True)
<meta:document-titles xmlns:meta="http://www.gale.com/goldschema/metadata">_title_display_title_sort_title_open_url</meta:document-titles>
<BLANKLINE>

>>> # TEST OPTIONAL SOURCE_PAGINATION_GROUP =======================================================
>>> source_pagination_group = meta.source_pagination_group()
>>> print source_pagination_group
None

>>> # TEST ALL SOURCE_PAGINATION_GROUP =======================================================
>>> source_pagination_group = meta.source_pagination_group('_composed')
>>> print etree.tostring(source_pagination_group, pretty_print=True)
<meta:source-pagination-group xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:source-pagination>
    <meta:pagination-group>
      <meta:pagination>
        <meta:composed>_composed</meta:composed>
      </meta:pagination>
    </meta:pagination-group>
  </meta:source-pagination>
</meta:source-pagination-group>
<BLANKLINE>

>>> # TEST OPTIONAL STRUCTURED_NAME =======================================================
>>> structured_name = meta.structured_name()
>>> print etree.tostring(structured_name, pretty_print=True)
<meta:structured-name xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST ALL STRUCTURED_NAME =======================================================
>>> structured_name = meta.structured_name('_prefix', '_first_name', '_middle_name', '_last_name', '_suffix')
>>> print etree.tostring(structured_name, pretty_print=True)
<meta:structured-name xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:prefix>_prefix</meta:prefix>
  <meta:first-name>_first_name</meta:first-name>
  <meta:middle-name>_middle_name</meta:middle-name>
  <meta:last-name>_last_name</meta:last-name>
  <meta:suffix>_suffix</meta:suffix>
</meta:structured-name>
<BLANKLINE>

>>> # TEST OPTIONAL BIBLIOGRAPHIC_IDS =======================================================
>>> bibliographic_ids = meta.bibliographic_ids()
>>> print etree.tostring(bibliographic_ids, pretty_print=True)
<meta:bibliographic-ids xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST ALL BIBLIOGRAPHIC_IDS =======================================================
>>> bibliographic_ids = meta.bibliographic_ids('_type', '_value')
>>> print etree.tostring(bibliographic_ids, pretty_print=True)
<meta:bibliographic-ids xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:id type="_type">
    <meta:value>_value</meta:value>
  </meta:id>
</meta:bibliographic-ids>
<BLANKLINE>

>>> # TEST OPTIONAL TERM =======================================================
>>> term = meta.term()
>>> print etree.tostring(term, pretty_print=True)
<meta:term xmlns:meta="http://www.gale.com/goldschema/metadata"/>
<BLANKLINE>

>>> # TEST ALL TERM =======================================================
>>> term = meta.term('_type', 'source', '_id', 'value')
>>> print etree.tostring(term, pretty_print=True)
<meta:term xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:term-type>_type</meta:term-type>
  <meta:term-source>source</meta:term-source>
  <meta:term-id>_id</meta:term-id>
  <meta:term-value>value</meta:term-value>
</meta:term>
<BLANKLINE>

>>> # TEST RECORD_ADMIN_INFO =======================================================
>>> record_admin_info = meta.record_admin_info('_standard_date_type', '_standard_data_value')
>>> print etree.tostring(record_admin_info, pretty_print=True)
<meta:record-admin-info xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:standard-date type="_standard_date_type">_standard_data_value</meta:standard-date>
</meta:record-admin-info>
<BLANKLINE>

>>> # TEST PUBLICATION_DATE =======================================================
>>> publication_date = meta.publication_date(_year='1', _month='2', _day='3', _day_of_week='4', _irregular_value='5', _start_date='6', _end_date='7')
>>> print etree.tostring(publication_date, pretty_print=True)
<meta:publication-date xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:structured-date>
    <meta:year>1</meta:year>
    <meta:month>2</meta:month>
    <meta:day>3</meta:day>
    <meta:day-of-week>4</meta:day-of-week>
    <meta:irregular>5</meta:irregular>
  </meta:structured-date>
  <meta:standard-date type="Start date">6</meta:standard-date>
  <meta:standard-date type="End date">7</meta:standard-date>
</meta:publication-date>
<BLANKLINE>

>>> # TEST SOURCE_INSTITUTION =======================================================
>>> source_institution = meta.source_institution('_institution_name', '_institution_location', '_copyright_statement')
>>> print etree.tostring(source_institution, pretty_print=True)
<meta:source-institution xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:institution-name>_institution_name</meta:institution-name>
  <meta:institution-location>_institution_location</meta:institution-location>
  <meta:copyright-statement>_copyright_statement</meta:copyright-statement>
</meta:source-institution>
<BLANKLINE>

>>> # TEST CONTENT_DATE =======================================================
>>> content_date = meta.content_date(_year='1', _month='2', _day='3', _day_of_week='4', _irregular_value='5', _start_date='6', _end_date='7')
>>> print etree.tostring(content_date, pretty_print=True)
<meta:content-date xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:structured-date>
    <meta:year>1</meta:year>
    <meta:month>2</meta:month>
    <meta:day>3</meta:day>
    <meta:day-of-week>4</meta:day-of-week>
    <meta:irregular>5</meta:irregular>
  </meta:structured-date>
  <meta:standard-date type="Start date">6</meta:standard-date>
  <meta:standard-date type="End date">7</meta:standard-date>
</meta:content-date>
<BLANKLINE>

>>> # TEST OPTIONAL CORPORATE_AUTHOR =======================================================
>>> corporate_author = meta.corporate_author()
>>> print etree.tostring(corporate_author, pretty_print=True)
<meta:corporate-author xmlns:meta="http://www.gale.com/goldschema/metadata"></meta:corporate-author>
<BLANKLINE>

>>> # TEST ALL CORPORATE_AUTHOR =======================================================
>>> corporate_author = meta.corporate_author('corporate_author')
>>> print etree.tostring(corporate_author, pretty_print=True)
<meta:corporate-author xmlns:meta="http://www.gale.com/goldschema/metadata">corporate_author</meta:corporate-author>
<BLANKLINE>

>>> # TEST META =======================================================
>>> _meta = meta.meta('meta')
>>> print etree.tostring(_meta, pretty_print=True)
<meta:Meta xmlns:meta="http://www.gale.com/goldschema/metadata">meta</meta:Meta>
<BLANKLINE>

>>> # TEST AUTHORS =======================================================
>>> authors = meta.authors('authors')
>>> print etree.tostring(authors, pretty_print=True)
<meta:authors xmlns:meta="http://www.gale.com/goldschema/metadata">authors</meta:authors>
<BLANKLINE>

>>> # TEST VOLUME_NUMBER =======================================================
>>> volume_number = meta.volume_number('volume_number')
>>> print etree.tostring(volume_number, pretty_print=True)
<meta:volume-number xmlns:meta="http://www.gale.com/goldschema/metadata">volume_number</meta:volume-number>
<BLANKLINE>

>>> # TEST MCODE =======================================================
>>> mcode = meta.mcode('mcode')
>>> print etree.tostring(mcode, pretty_print=True)
<meta:mcode xmlns:meta="http://www.gale.com/goldschema/metadata">mcode</meta:mcode>
<BLANKLINE>

>>> # TEST PUBLICATION_TITLE =======================================================
>>> publication_title = meta.publication_title('publication_title')
>>> print etree.tostring(publication_title, pretty_print=True)
<meta:publication-title xmlns:meta="http://www.gale.com/goldschema/metadata">publication_title</meta:publication-title>
<BLANKLINE>
    
>>> # TEST ID =======================================================
>>> id = meta.id('id')
>>> print etree.tostring(id, pretty_print=True)
<meta:id xmlns:meta="http://www.gale.com/goldschema/metadata">id</meta:id>
<BLANKLINE>

>>> # TEST VALUE =======================================================
>>> value = meta.value('value')
>>> print etree.tostring(value, pretty_print=True)
<meta:value xmlns:meta="http://www.gale.com/goldschema/metadata">value</meta:value>
<BLANKLINE>

>>> # TEST STANDARD_DATE =======================================================
>>> standard_date = meta.standard_date('standard_date')
>>> print etree.tostring(standard_date, pretty_print=True)
<meta:standard-date xmlns:meta="http://www.gale.com/goldschema/metadata">standard_date</meta:standard-date>
<BLANKLINE>

>>> # TEST INDEXING_TERM =======================================================
>>> indexing_term = meta.indexing_term('indexing_term')
>>> print etree.tostring(indexing_term, pretty_print=True)
<meta:indexing-term xmlns:meta="http://www.gale.com/goldschema/metadata">indexing_term</meta:indexing-term>
<BLANKLINE>

>>> # TEST TERM_TYPE =======================================================
>>> term_type = meta.term_type('term_type')
>>> print etree.tostring(term_type, pretty_print=True)
<meta:term-type xmlns:meta="http://www.gale.com/goldschema/metadata">term_type</meta:term-type>
<BLANKLINE>

>>> # TEST TERM_SOURCE =======================================================
>>> term_source = meta.term_source('term_source')
>>> print etree.tostring(term_source, pretty_print=True)
<meta:term-source xmlns:meta="http://www.gale.com/goldschema/metadata">term_source</meta:term-source>
<BLANKLINE>

>>> # TEST TERM_ID =======================================================
>>> term_id = meta.term_id('term_id')
>>> print etree.tostring(term_id, pretty_print=True)
<meta:term-id xmlns:meta="http://www.gale.com/goldschema/metadata">term_id</meta:term-id>
<BLANKLINE>

>>> # TEST TERM_VALUE =======================================================
>>> term_value = meta.term_value('term_value')
>>> print etree.tostring(term_value, pretty_print=True)
<meta:term-value xmlns:meta="http://www.gale.com/goldschema/metadata">term_value</meta:term-value>
<BLANKLINE>

>>> # TEST STRUCTURED_DATE =======================================================
>>> structured_date = meta.structured_date('structured_date')
>>> print etree.tostring(structured_date, pretty_print=True)
<meta:structured-date xmlns:meta="http://www.gale.com/goldschema/metadata">structured_date</meta:structured-date>
<BLANKLINE>

>>> # TEST IRREGULAR =======================================================
>>> irregular = meta.irregular('irregular')
>>> print etree.tostring(irregular, pretty_print=True)
<meta:irregular xmlns:meta="http://www.gale.com/goldschema/metadata">irregular</meta:irregular>
<BLANKLINE>

>>> # TEST TITLE_DISPLAY =======================================================
>>> title_display = meta.title_display('title_display')
>>> print etree.tostring(title_display, pretty_print=True)
<meta:title-display xmlns:meta="http://www.gale.com/goldschema/metadata">title_display</meta:title-display>
<BLANKLINE>

>>> # TEST TITLE_SORT =======================================================
>>> title_sort = meta.title_sort('title_sort')
>>> print etree.tostring(title_sort, pretty_print=True)
<meta:title-sort xmlns:meta="http://www.gale.com/goldschema/metadata">title_sort</meta:title-sort>
<BLANKLINE>

>>> # TEST TITLE_OPEN_URL =======================================================
>>> title_open_url = meta.title_open_url('title_open_url')
>>> print etree.tostring(title_open_url, pretty_print=True)
<meta:title-open-url xmlns:meta="http://www.gale.com/goldschema/metadata">title_open_url</meta:title-open-url>
<BLANKLINE>

>>> # TEST INSTITUTION_NAME =======================================================
>>> institution_name = meta.institution_name('institution_name')
>>> print etree.tostring(institution_name, pretty_print=True)
<meta:institution-name xmlns:meta="http://www.gale.com/goldschema/metadata">institution_name</meta:institution-name>
<BLANKLINE>

>>> # TEST INSTITUTION_LOCATION =======================================================
>>> institution_location = meta.institution_location('institution_location')
>>> print etree.tostring(institution_location, pretty_print=True)
<meta:institution-location xmlns:meta="http://www.gale.com/goldschema/metadata">institution_location</meta:institution-location>
<BLANKLINE>

>>> # TEST COPYRIGHT_STATEMENT =======================================================
>>> copyright_statement = meta.copyright_statement('copyright_statement')
>>> print etree.tostring(copyright_statement, pretty_print=True)
<meta:copyright-statement xmlns:meta="http://www.gale.com/goldschema/metadata">copyright_statement</meta:copyright-statement>
<BLANKLINE>

>>> # TEST AUTHOR =======================================================
>>> author = meta.author('author')
>>> print etree.tostring(author, pretty_print=True)
<meta:author xmlns:meta="http://www.gale.com/goldschema/metadata">author</meta:author>
<BLANKLINE>

>>> # TEST PAGE_ID_NUMBER =======================================================
>>> page_id_number = meta.page_id_number('page_id_number')
>>> print etree.tostring(page_id_number, pretty_print=True)
<meta:page-id-number xmlns:meta="http://www.gale.com/goldschema/metadata">page_id_number</meta:page-id-number>
<BLANKLINE>

>>> # TEST PREFIX =======================================================
>>> prefix = meta.prefix('prefix')
>>> print etree.tostring(prefix, pretty_print=True)
<meta:prefix xmlns:meta="http://www.gale.com/goldschema/metadata">prefix</meta:prefix>
<BLANKLINE>

>>> # TEST FIRST_NAME =======================================================
>>> first_name = meta.first_name('first_name')
>>> print etree.tostring(first_name, pretty_print=True)
<meta:first-name xmlns:meta="http://www.gale.com/goldschema/metadata">first_name</meta:first-name>
<BLANKLINE>

>>> # TEST MIDDLE_NAME =======================================================
>>> middle_name = meta.middle_name('middle_name')
>>> print etree.tostring(middle_name, pretty_print=True)
<meta:middle-name xmlns:meta="http://www.gale.com/goldschema/metadata">middle_name</meta:middle-name>
<BLANKLINE>

>>> # TEST LAST_NAME =======================================================
>>> last_name = meta.last_name('last_name')
>>> print etree.tostring(last_name, pretty_print=True)
<meta:last-name xmlns:meta="http://www.gale.com/goldschema/metadata">last_name</meta:last-name>
<BLANKLINE>

>>> # TEST SUFFIX =======================================================
>>> suffix = meta.suffix('suffix')
>>> print etree.tostring(suffix, pretty_print=True)
<meta:suffix xmlns:meta="http://www.gale.com/goldschema/metadata">suffix</meta:suffix>
<BLANKLINE>

>>> # TEST TITLE =======================================================
>>> title = meta.title('title')
>>> print etree.tostring(title, pretty_print=True)
<meta:title xmlns:meta="http://www.gale.com/goldschema/metadata">title</meta:title>
<BLANKLINE>

>>> # TEST NAME =======================================================
>>> name = meta.name('name')
>>> print etree.tostring(name, pretty_print=True)
<meta:name xmlns:meta="http://www.gale.com/goldschema/metadata">name</meta:name>
<BLANKLINE>

>>> # TEST COMPOSED_NAME =======================================================
>>> composed_name = meta.composed_name('composed_name')
>>> print etree.tostring(composed_name, pretty_print=True)
<meta:composed-name xmlns:meta="http://www.gale.com/goldschema/metadata">composed_name</meta:composed-name>
<BLANKLINE>

>>> # TEST SOURCE_PAGINATION =======================================================
>>> source_pagination = meta.source_pagination('source_pagination')
>>> print etree.tostring(source_pagination, pretty_print=True)
<meta:source-pagination xmlns:meta="http://www.gale.com/goldschema/metadata">source_pagination</meta:source-pagination>
<BLANKLINE>

>>> # TEST PAGINATION_GROUP =======================================================
>>> pagination_group = meta.pagination_group('pagination_group')
>>> print etree.tostring(pagination_group, pretty_print=True)
<meta:pagination-group xmlns:meta="http://www.gale.com/goldschema/metadata">pagination_group</meta:pagination-group>
<BLANKLINE>

>>> # TEST PAGINATION =======================================================
>>> pagination = meta.pagination('pagination')
>>> print etree.tostring(pagination, pretty_print=True)
<meta:pagination xmlns:meta="http://www.gale.com/goldschema/metadata">pagination</meta:pagination>
<BLANKLINE>

>>> # TEST COMPOSED =======================================================
>>> composed = meta.composed('composed')
>>> print etree.tostring(composed, pretty_print=True)
<meta:composed xmlns:meta="http://www.gale.com/goldschema/metadata">composed</meta:composed>
<BLANKLINE>

>>> # TEST CONTENT_TYPE =======================================================
>>> content_type = meta.content_type('content_type')
>>> print etree.tostring(content_type, pretty_print=True)
<meta:content-type xmlns:meta="http://www.gale.com/goldschema/metadata">content_type</meta:content-type>
<BLANKLINE>

>>> # TEST SOURCE_CITATION =======================================================
>>> source_citation = meta.source_citation('source_citation')
>>> print etree.tostring(source_citation, pretty_print=True)
<meta:source-citation xmlns:meta="http://www.gale.com/goldschema/metadata">source_citation</meta:source-citation>
<BLANKLINE>

>>> # TEST MONTH =======================================================
>>> month = meta.month('month')
>>> print etree.tostring(month, pretty_print=True)
<meta:month xmlns:meta="http://www.gale.com/goldschema/metadata">month</meta:month>
<BLANKLINE>

>>> # TEST DAY =======================================================
>>> day = meta.day('day')
>>> print etree.tostring(day, pretty_print=True)
<meta:day xmlns:meta="http://www.gale.com/goldschema/metadata">day</meta:day>
<BLANKLINE>

>>> # TEST YEAR =======================================================
>>> year = meta.year('year')
>>> print etree.tostring(year, pretty_print=True)
<meta:year xmlns:meta="http://www.gale.com/goldschema/metadata">year</meta:year>
<BLANKLINE>

>>> # TEST OCR_CONFIDENCE  =======================================================
>>> ocr_confidence = meta.ocr_confidence('ocr_confidence')
>>> print etree.tostring(ocr_confidence, pretty_print=True)
<meta:ocr-confidence xmlns:meta="http://www.gale.com/goldschema/metadata">ocr_confidence</meta:ocr-confidence>
<BLANKLINE>

>>> # TEST TOTAL_PAGES =======================================================
>>> total_pages = meta.total_pages('total_pages')
>>> print etree.tostring(total_pages, pretty_print=True)
<meta:total-pages xmlns:meta="http://www.gale.com/goldschema/metadata">total_pages</meta:total-pages>
<BLANKLINE>

>>> # TEST LANGUAGES =======================================================
>>> languages = meta.languages('languages')
>>> print etree.tostring(languages, pretty_print=True)
<meta:languages xmlns:meta="http://www.gale.com/goldschema/metadata">languages</meta:languages>
<BLANKLINE>

>>> # TEST LANGUAGE =======================================================
>>> language = meta.language('language')
>>> print etree.tostring(language, pretty_print=True)
<meta:language xmlns:meta="http://www.gale.com/goldschema/metadata">language</meta:language>
<BLANKLINE>

'''
