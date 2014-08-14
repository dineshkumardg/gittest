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

fnames = ['Meetings/PSM-CHOA_20130923_00480.xml',
          'Meetings/PSM-CHOA_20130531_059.xml',
#     'Conferences/PSM-CHOA_20130823_00362.xml',
#     'Conferences/PSM-CHOA_20130823_00359.xml',
#     'Conferences/PSM-CHOA_20130823_00356.xml',
#     'Books/PSM-CHOA_20130913_00443.xml',
#     'Books/PSM-CHOA_20130913_00440.xml',
#     'Books/PSM-CHOA_20130913_00437.xml',
#     'Books/PSM-CHOA_20130913_00434.xml',
#     'WRFP/PSM-CHOA_20130913_00449.xml',
#     'WRFP/PSM-CHOA_20130913_00446.xml',
#     'Journals/PSM-CHOA_20130910_00395.xml',
#     'Journals/PSM-CHOA_20130910_00392.xml',
#     'Journals/PSM-CHOA_20130910_00389.xml',
#     'Journals/PSM-CHOA_20130910_00386.xml',
#     'Refugee Survey/PSM-CHOA_20130823_00365.xml',
#     'Pamphlets/PSM-CHOA_20130903_00376.xml',
#     'Survey and Documents/PSM-CHOA_20130814_227.xml',
#     'Survey and Documents/PSM-CHOA_20130814_224.xml',
#     'Survey and Documents/PSM-CHOA_20130820_00308.xml'
    ]

try:
    print 'KEY: feed file, document-instance # in feedfile, uid, count of uid, asset id'

    for fname in fnames:
        meetings_list = []
        list_21817803 = []
        list_21817804 = []
        list_17528382 = []
        list_14242630 = []

        gift_fname = os.path.join(os.path.dirname(__file__), fname)

        tree = etree.parse(gift_fname)
        document_instances_count = tree.xpath('count(/gold:feed/gold:document-instance)', namespaces=xml_ns)

        count_21817803 = 0
        count_21817804 = 0
        count_17528382 = 0
        count_14242630 = 0
        for document_instance in range(1, int(document_instances_count) + 1):
            asset_id = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
            asset_id_text = asset_id[0].text
            uids = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term/meta:term/meta:term-id' % document_instance, namespaces=xml_ns)
            found = False

            for uid in uids:
                if uid.text == '21817803':
                    count_21817803 += 1
                    list_21817803.append([fname, document_instance, uid.text, count_21817803, asset_id_text])
                    found = True

                if uid.text == '21817804':
                    count_21817804 += 1
                    list_21817804.append([fname, document_instance, uid.text, count_21817804, asset_id_text])
                    found = True

                if uid.text == '17528382':
                    count_17528382 += 1
                    list_17528382.append([fname, document_instance, uid.text, count_17528382, asset_id_text])
                    found = True

            if found == False:
                asset_id = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
                asset_id_text = asset_id[0].text
                count_14242630 += 1
                list_14242630.append([fname, document_instance, '14242630', count_14242630, asset_id_text])

            meetings_list.append(asset_id[0].text)

        for entry in list_14242630:
            print entry

        for entry in list_21817803:
            print entry

        for entry in list_21817804:
            print entry

        for entry in list_17528382:
            print entry

        print sorted(meetings_list)

        print 'cumulative=%s; 14242630=%s; 21817803=%s; 21817804=%s; 17528382=%s\n\n' %(len(list_14242630) + len(list_21817803) + len(list_21817804) +len(list_17528382), 
            len(list_14242630), len(list_21817803), len(list_21817804), len(list_17528382))

except Exception as e:
    print e
