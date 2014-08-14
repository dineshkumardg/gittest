from lxml import etree
import os
import psycopg2

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


fnames = [
     # log3 - also picked up PSM-CHOA_20131028_00604.xml
     # same order as log2 verison
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20130924_00487.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131017_00543.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20130926_00498.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131028_00600.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20130926_00501.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131028_00607.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131007_00507.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131028_00610.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131007_00510.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131028_00613.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131007_00513.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131029_00625.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131007_00516.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131029_00628.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131009_00519.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131029_00631.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131009_00522.xml',
    '/home/jsears/Desktop/module_1_feed_files/PSM-CHOA_20131028_00604.xml',
    ]
'''
NOTE - Venus has processed these files!

Here is the list of latest feedfiles directories in:

V:\Production\Feedfiles\CHOA Feedfiles\GAIA EGEST Feedfiles

Whatever you do please can you copy these and create a new directory and version for any editing work. I just want to keep these intact for reference if we need to back track.

Watch out for Conf. Series and S&D folders where there will be unzipped files that Sarah amended in the last couple of days. These are the correct files, but there will also be the original zipped files in the folder as well.

Books_Feedfiles_20131121
Conference_Series_Feedfiles_20131121
Journals_Feedfiles_20131112
Meetings_Feedfiles_20131112
Refugee_Survey_Feedfiles_20131121
Reports_Feedfiles_20131112
Review_of_FP_Feedfiles_20131119
Survey_Documents_Feedfiles_20131122
'''


def get_article_sequence_id(psm_id, document_asset_id):  # for non meetings
    connection = None
    try:
        host = '10.179.176.181'
        port = '5432'
        db = 'cho'
        uid = 'gaia'
        pwd = 'g818'
        connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (host, port, db, uid, pwd))
        cursor = connection.cursor()

        sql = 'SELECT chunk.dom_id as article_sequence, chunk_final_id.final_id as assetid '
        sql += 'FROM public.chunk_final_id, public.chunk, public.document, public.item '
        sql += 'WHERE '
        sql += 'chunk_final_id.chunk_id = chunk.id AND '
        sql += 'chunk.document_id = document.id AND '
        sql += 'document.item_id = item.id AND '
        sql += 'item.is_live = TRUE AND '
        sql += "document.dom_id = '%s' " % psm_id
        sql += 'ORDER BY document.dom_id ASC, chunk.dom_id ASC;'

        cursor.execute(sql)

        articleid = 1
        articleid_assetid_list = {}
        for article_sequence, assetid in cursor:
            #print psm_id, article_sequence, assetid, articleid
            articleid_assetid_list[assetid] = articleid
            articleid += 1

        return articleid_assetid_list[document_asset_id]
    except Exception:
        return -1  # show user there is a problem, that asset id has been 'levelled' away
        ''' SELECT chunk.dom_id as article_sequence, chunk_final_id.final_id as assetid
            FROM public.chunk_final_id, public.chunk, public.document, public.item
            WHERE
            chunk_final_id.chunk_id = chunk.id AND
            chunk.document_id = document.id AND
            document.item_id = item.id AND
            item.is_live = TRUE AND
            document.dom_id ='cho_rpax_1959_carrington_000_0000'
            ORDER BY document.dom_id ASC, chunk.dom_id ASC;
        '''

        '''
        SELECT psmid, articleid, count(articleid) as instance
        FROM tbl_log2
        GROUP BY psmid, articleid
        order by instance desc
        '''

    finally:
        if connection is not None:
            connection.close()


try:
    print 'KEY: feed file|document-instance # in feedfile|psmid|articleid|assetid|title|author(s) wth / seperator'

    for fname in fnames:
        root_fpath = ''
        gift_fname = os.path.join(root_fpath, fname)

        tree = etree.parse(gift_fname)
        document_instances_count = tree.xpath('count(/gold:feed/gold:document-instance)', namespaces=xml_ns)

        for document_instance in range(1, int(document_instances_count) + 1):
            authors = ''

            psm_id = tree.xpath("/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:bibliographic-ids/meta:id[@type='PSM']/meta:value" % document_instance, namespaces=xml_ns)
            psm_id_text = psm_id[0].text

            asset_id = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value' % document_instance, namespaces=xml_ns)
            asset_id_text = asset_id[0].text

            title = tree.xpath('/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/gift-doc:document-titles/meta:title-display' % document_instance, namespaces=xml_ns)
            title_text = title[0].text

            # meeting's use document - so assume what's in the feed file is good
            if psm_id_text[:8] in ['cho_meet', 'cho_chrx', 'cho_chbp', 'cho_rpax']:
                article_id = 1
                authors = tree.xpath("/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:authors/meta:author/meta:composed-name" % document_instance, namespaces=xml_ns)

                authors_id = ''
                if len(authors) == 1:
                    authors_id = authors[0].text

                if len(authors) > 1:
                    for author in authors:
                        print '%s|%s|%s|%s|%s|%s|%s' % (fname, document_instance, psm_id_text, article_id, asset_id_text, title_text.encode('utf-8'), author.text.encode('utf-8'))
                else:
                    print '%s|%s|%s|%s|%s|%s|%s' % (fname, document_instance, psm_id_text, article_id, asset_id_text, title_text.encode('utf-8'), authors_id.encode('utf-8'))
            else:
                article_id = get_article_sequence_id(psm_id_text, asset_id_text)

                author_count = int(tree.xpath('count(/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:authors/meta:author)' % document_instance, namespaces=xml_ns))

                authors_id = ''
                if author_count > 0:
                    for author in range(1, author_count + 1):
                        author_xpath = tree.xpath("/gold:feed/gold:document-instance[%s]/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:authors/meta:author[%s]/meta:composed-name" % (document_instance, author), namespaces=xml_ns)
                        if len(author_xpath) > 0:
                            print '%s|%s|%s|%s|%s|%s|%s' % (fname, document_instance, psm_id_text, article_id, asset_id_text, title_text.encode('utf-8'), author_xpath[0].text.encode('utf-8'))
                else:
                    print '%s|%s|%s|%s|%s|%s|%s' % (fname, document_instance, psm_id_text, article_id, asset_id_text, title_text.encode('utf-8'), authors_id.encode('utf-8'))


except Exception as e:
    print e
