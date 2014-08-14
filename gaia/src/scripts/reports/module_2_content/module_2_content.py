from cStringIO import StringIO
import os
from lxml import etree

# noinspection PyShadowingNames
def get_psmid_prefix(psmid):
    return psmid[:8]

def get_xpath_values_from_fixed_psmid(psmid, use_test_data=False):
    fixed_xml = get_fixed_xml_as_string_from_file(psmid, use_test_data)
    if fixed_xml is not None:
        psmid_prefix = get_psmid_prefix(psmid)

        if psmid_prefix in ['cho_book']:
            return get_details_from_book_or_report_pamphlet_and_briefing_paper_or_meeting(psmid, fixed_xml, 'book')
        elif psmid_prefix in ['cho_chbp', 'cho_chrx', 'cho_rpax']:
            return get_details_from_book_or_report_pamphlet_and_briefing_paper_or_meeting(psmid, fixed_xml, 'book')
        elif psmid_prefix in ['cho_meet']:
            return get_details_from_book_or_report_pamphlet_and_briefing_paper_or_meeting(psmid, fixed_xml, 'meeting')
        elif psmid_prefix in ['cho_bcrc', 'cho_iprx', 'cho_conf']:
            return get_details_from_conference_series(psmid, fixed_xml)
        elif psmid_prefix in ['cho_binx', 'cho_iaxx', 'cho_wtxx']:
            return get_details_from_journal(psmid, fixed_xml)

    return None

def get_fixed_xml_as_string_from_file(psmid, use_test_data=False):
    if use_test_data:
        psmid_fpath = os.path.join(os.path.dirname(__file__), 'test_data/%s.xml' % psmid)
    else:
        psmid_fpath = os.path.join('/run/media/jsears/1TB/all_xml/%s.xml' % psmid)

    try:
        return open(psmid_fpath).read()
    except IOError:
        return None

def get_xml_tree(fixed_xml):
    return etree.parse(StringIO(fixed_xml))

def get_details_from_book_or_report_pamphlet_and_briefing_paper_or_meeting(psmid, fixed_xml, type):
    xml_tree = get_xml_tree(fixed_xml)
    authors = xml_tree.xpath('/chapter/citation/%s/author[@role="author"]/aucomposed' % type)
    title = xml_tree.xpath('/chapter/citation/%s/titleGroup/fullTitle' % type)
    date = xml_tree.xpath('/chapter/citation/%s/pubDate/composed' % type)

    details = ""
    if len(authors) > 0:
        for author in authors:
            details += '%s|||%s|||%s|||%s\n' % (psmid, author.text,  title[0].text, date[0].text)
    else:
        details = '%s||||||%s|||%s\n' % (psmid, title[0].text, date[0].text)

    return details

def get_details_from_conference_series(psmid, fixed_xml):
    xml_tree = get_xml_tree(fixed_xml)
    conferance_names = xml_tree.xpath('/chapter/citation/conference/conferenceGroup/conferenceName')
    date = xml_tree.xpath('/chapter/citation/conference/pubDate/composed')

    details = ""
    for conferance_name in conferance_names:
        details += '%s|||%s|||%s\n' % (psmid, conferance_name.text, date[0].text)

    return details

def get_details_from_journal(psmid, fixed_xml):
    xml_tree = get_xml_tree(fixed_xml)
    volume_number = xml_tree.xpath('/chapter/citation/journal/volumeGroup/volumeNumber')

    return '%s|||%s\n' % (psmid, volume_number[0].text)

def main(csv_with_psmids=os.path.join(os.path.dirname(__file__), 'module_2_psmids.csv')):
    with open(csv_with_psmids) as f:
        for psmid in f:
            print get_xpath_values_from_fixed_psmid(psmid.replace('\n', '')).rstrip()

if __name__ == "__main__":
    main()