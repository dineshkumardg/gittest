import glob
from lxml import etree

def list_asset_ids(xml_files):
    for xml_file in xml_files:
        _extract_asset_id_from_xml_file(xml_file)

def _extract_asset_id_from_xml_file(xml_fname):
    tree = etree.parse(xml_fname, etree.XMLParser())

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

    asset_ids = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value/text()', namespaces=xml_ns)

    fpath = xml_fname.replace('/home/jsears/Desktop/tmp/sh-pd-assetid-list-feed-files/from-gaia/', '')
    fpath = fpath.replace('/home/jsears/Desktop/tmp/sh-pd-assetid-list-feed-files/from-merge/', '')

    results = []
    for asset_id in asset_ids:
        #results.append('%s|%s' % (fpath, asset_id))
        results.append('%s' % asset_id)

    for sorted_result in sorted(results):
        print sorted_result

# py find_asset_ids_in_feed_files.py | sort  | uniq -c | sort -nr > gaia.count
#list_asset_ids(glob.glob('/home/jsears/Desktop/tmp/sh-pd-assetid-list-feed-files/from-gaia/*.xml'))

# py find_asset_ids_in_feed_files.py | sort  | uniq -c | sort -nr > merge.count
list_asset_ids(glob.glob('/home/jsears/Desktop/tmp/sh-pd-assetid-list-feed-files/from-merge/*.xml'))


