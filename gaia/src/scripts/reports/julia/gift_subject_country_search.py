from lxml import etree
import os

xml_ns = {'dir': 'http://www.gale.com/goldschema/dir',
    'essay': 'http://www.gale.com/goldschema/essay',
    'etoc': 'http://www.gale.com/goldschema/etoc',
    'gift-doc': 'http://www.gale.com/goldschema/gift-doc',
    'gold': 'http://www.gale.com/gold',
    'index': 'http://www.gale.com/goldschema/index',
    'list': 'http://www.gale.com/goldschema/list',
    'math': 'http://www.w3.org/1998/Math/MathML',
    'media': 'http://www.gale.com/goldschema/media',
    'meta': 'http://www.gale.com/goldschema/metadata',
    'mla': 'http://www.gale.com/goldschema/mla',
    'pres': 'http://www.gale.com/goldschema/pres',
    'pub-meta': 'http://www.gale.com/goldschema/pub-meta',
    'shared': 'http://www.gale.com/goldschema/shared',
    'table': 'http://www.gale.com/goldschema/table',
    'tt': 'http://www.w3.org/ns/ttml',
    'vault-link': 'http://www.gale.com/goldschema/vault-linking',
    'verse': 'http://www.gale.com/goldschema/verse',
    'xatts': 'http://www.gale.com/goldschema/xatts',
    'xlink': 'http://www.w3.org/1999/xlink'}


def show(gift_fname, document_instance_index, article_asset_id, subject_text, geo_scope_text, event_text, person_text):
    print '%s|%s|%s|%s|%s|%s|%s' % (gift_fname, document_instance_index, article_asset_id, subject_text, geo_scope_text, event_text, person_text)

try:
    print 'gift filename|document instance|article asset id|subject|geo scope|event|person'

    gift_fname = os.path.join(os.path.dirname(__file__), 'PSM-CHOA_20130923_00480.xml')

    tree = etree.parse(gift_fname)
    document_instances_count = tree.xpath('count(/gold:feed/gold:document-instance)', namespaces=xml_ns)

    article_asset_id = subject_text = geo_scope_text = event_text = person_text = ''

    for document_instance_index in range(1, int(document_instances_count) + 1):
        meta_indexing_term_count = tree.xpath('count(/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term)' % document_instance_index, namespaces=xml_ns)

        article_asset_id  = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance_index, namespaces=xml_ns)
        article_asset_id_text = article_asset_id[0].text

        for meta_indexing_term_index in range(1, int(meta_indexing_term_count) + 1):
            meta_indexing_term = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term[%s]/meta:term/meta:term-type' % (document_instance_index, meta_indexing_term_index), namespaces=xml_ns)
            meta_indexing_term_text = meta_indexing_term[0].text

            #print meta_indexing_term_text

            meta_indexing_term_value = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term[%s]/meta:term/meta:term-value' % (document_instance_index, meta_indexing_term_index), namespaces=xml_ns)

            if meta_indexing_term_text == 'SUBJECT':
                subject_text = meta_indexing_term_value[0].text
                show(gift_fname, document_instance_index, article_asset_id_text, subject_text, geo_scope_text, event_text, person_text)

            if meta_indexing_term_text == 'GEO_SCOPE':
                geo_scope_text = meta_indexing_term_value[0].text
                show(gift_fname, document_instance_index, article_asset_id_text, subject_text, geo_scope_text, event_text, person_text)

            if meta_indexing_term_text == 'EVENT':
                event_text = meta_indexing_term_value[0].text
                show(gift_fname, document_instance_index, article_asset_id_text, subject_text, geo_scope_text, event_text, person_text)

            if meta_indexing_term_text == 'PERSON':
                person_text = meta_indexing_term_value[0].text
                show(gift_fname, document_instance_index, article_asset_id_text, subject_text, geo_scope_text, event_text, person_text)

except Exception as e:
    print e
