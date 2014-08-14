from lxml import etree
import os
import csv

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

fnames = ['Conferences/PSM-CHOA_20130823_00362.xml',
    'Conferences/PSM-CHOA_20130823_00359.xml',
    'Conferences/PSM-CHOA_20130823_00356.xml',
    'Books/PSM-CHOA_20130913_00443.xml',
    'Books/PSM-CHOA_20130913_00440.xml',
    'Books/PSM-CHOA_20130913_00437.xml',
    'Books/PSM-CHOA_20130913_00434.xml',
    'WRFP/PSM-CHOA_20130913_00449.xml',
    'WRFP/PSM-CHOA_20130913_00446.xml',
    'Journals/PSM-CHOA_20130910_00395.xml',
    'Journals/PSM-CHOA_20130910_00392.xml',
    'Journals/PSM-CHOA_20130910_00389.xml',
    'Journals/PSM-CHOA_20130910_00386.xml',
    'Refugee Survey/PSM-CHOA_20130823_00365.xml',
    'Pamphlets/PSM-CHOA_20130903_00376.xml',
    'Survey and Documents/PSM-CHOA_20130814_227.xml',
    'Survey and Documents/PSM-CHOA_20130814_224.xml',
    'Survey and Documents/PSM-CHOA_20130820_00308.xml']

try:
    print 'KEY: feed file, psmid, language, title, asset id'
    lang_asset_ids = []
 
    for fname in fnames:
        gift_fname = os.path.join(os.path.dirname(__file__), fname)
 
        tree = etree.parse(gift_fname)
        document_instances_count = tree.xpath('count(/gold:feed/gold:document-instance)', namespaces=xml_ns)
 
        for document_instance in range(1, int(document_instances_count) + 1):
            asset_id = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
            psmid = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:bibliographic-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
            lang = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:languages/meta:language' % document_instance, namespaces=xml_ns)
            title = tree.xpath(' /gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/gift-doc:document-titles/meta:title-display' % document_instance, namespaces=xml_ns)
            uids = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term/meta:term/meta:term-id' % document_instance, namespaces=xml_ns)
 
 
 
            if lang[0].text != 'English':
                # exclusion 21817803    21817804    17528382
 
                found = False
                for uid in uids:
                    if uid.text == '21817803':
                        found = True
 
                    if uid.text == '21817804':
                        found = True
 
                    if uid.text == '17528382':
                        found = True
 
                if found == False:
#                     present = [i for i in lang_asset_ids if i in asset_id[0].text]  # its possible same article is in two feed files
#                     if len(present) == 0: 
                    lang_asset_ids.append(asset_id[0].text)
                    print  [fname, psmid[0].text, lang[0].text, title[0].text, asset_id[0].text]

    #################################################

    fname = 'Meetings/PSM-CHOA_20130923_00480.xml'
    gift_fname = os.path.join(os.path.dirname(__file__), fname)

    tree = etree.parse(gift_fname)
    document_instances_count = tree.xpath('count(/gold:feed/gold:document-instance)', namespaces=xml_ns)

    for document_instance in range(1, int(document_instances_count) + 1):
        asset_id = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
        psmid = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:bibliographic-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
        lang = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:languages/meta:language' % document_instance, namespaces=xml_ns)
        title = tree.xpath(' /gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/gift-doc:document-titles/meta:title-display' % document_instance, namespaces=xml_ns)
        uids = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term/meta:term/meta:term-id' % document_instance, namespaces=xml_ns)

        if lang[0].text != 'English':
            # exclusion 21817803    21817804    17528382
            found = False
            for uid in uids:
                if uid.text == '21817803':
                    found = True

                if uid.text == '21817804':
                    found = True

                if uid.text == '17528382':
                    found = True

            if found == False:
#                     present = [i for i in lang_asset_ids if i in asset_id[0].text]  # its possible same article is in two feed files
#                     if len(present) == 0: 
                lang_asset_ids.append(asset_id[0].text)
                print  [fname, psmid[0].text, lang[0].text, title[0].text, asset_id[0].text]


except Exception as e:
    print e
