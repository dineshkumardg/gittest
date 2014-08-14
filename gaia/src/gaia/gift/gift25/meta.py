from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker, attr
from lxml.builder import ElementMaker


class _Meta(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self, namespace='http://www.gale.com/goldschema/metadata', nsmap={'meta' : 'http://www.gale.com/goldschema/metadata', }, **kwargs)


def document_ids(_type0=None, _value0=None, _type1=None, _value1=None):
    document_ids = []

    if _type0 is not None and _value0 is not None:
        document_ids.append(id(attr('type', _type0), value(_value0)))

    if _type1 is not None and _value1 is not None:
        document_ids.append(id(attr('type', _type1), value(_value1)))

    return _document_ids(*document_ids)


def bibliographic_ids(type0=None, _value0=None, type1=None, _value1=None, type2=None, _value2=None, type3=None, _value3=None):
    bibliographic_ids = []

    if type0 is not None and _value0 is not None:
        bibliographic_ids.append(id(attr('type', type0), value(_value0)))

    if type1 is not None and _value1 is not None:
        bibliographic_ids.append(id(attr('type', type1), value(_value1)))

    if type2 is not None and _value2 is not None:
        bibliographic_ids.append(id(attr('type', type2), value(_value2)))

    if type3 is not None and _value3 is not None:
        bibliographic_ids.append(id(attr('type', type3), value(_value3)))

    return _bibliographic_ids(*bibliographic_ids)


def record_admin_info(_standard_date_type, _standard_data_value):
    return _record_admin_info(standard_date(attr('type', _standard_date_type), _standard_data_value))


def _date(_date_type=None, _year=None, _month=None, _day=None, _day_of_week=None, _irregular=None, _start_date=None, _end_date=None):
    structured_date_elements = []

    if _year is not None:
        structured_date_elements.append(year(_year))

    if _month is not None:
        structured_date_elements.append(month(_month))

    if _day is not None:
        structured_date_elements.append(day(_day))

    if _day_of_week is not None:
        structured_date_elements.append(day_of_week(_day_of_week))

    if _irregular is not None:
        structured_date_elements.append(irregular(_irregular))

    standard_date_elements = []
    if _start_date is not None:
        standard_date_elements.append(standard_date(attr('type', 'Start date'), _start_date))

    if _end_date is not None:
        standard_date_elements.append(standard_date(attr('type', 'End date'), _end_date))

    return _date_type(
        structured_date(
            *structured_date_elements
            ),
        *standard_date_elements
    )


def content_date(_year=None, _month=None, _day=None, _day_of_week=None, _irregular_value=None, _start_date=None, _end_date=None):
    return _date(_content_date, _year, _month, _day, _day_of_week, _irregular_value, _start_date, _end_date)


def publication_date(_year=None, _month=None, _day=None, _day_of_week=None, _irregular_value=None, _start_date=None, _end_date=None):
    return _date(_publication_date, _year, _month, _day, _day_of_week, _irregular_value, _start_date, _end_date)


def source_institution(_institution_name, _institution_location, _copyright_statement):
    return _source_institution( institution_name(_institution_name),
                                institution_location(_institution_location),
                                copyright_statement(_copyright_statement))


def source_pagination_group(_composed=None):
    if _composed is not None:
        if isinstance(_composed, basestring):
            return _source_pagination_group(
                source_pagination(
                    pagination_group(
                        pagination(
                            composed(_composed)
                        )
                    )
                )
            )
    return None


def structured_name(_prefix=None, _first_name=None, _middle_name=None, _last_name=None, _suffix=None):
    structured_name_elements = []

    if _prefix is not None:
        structured_name_elements.append(prefix(_prefix))

    if _first_name is not None:
        structured_name_elements.append(first_name(_first_name))

    if _middle_name is not None:
        structured_name_elements.append(middle_name(_middle_name))

    if _last_name is not None:
        structured_name_elements.append(last_name(_last_name))

    if _suffix is not None:
        structured_name_elements.append(suffix(_suffix))

    return _structured_name(*structured_name_elements)


def term(_type=None, source=None, _id=None, value=None):
    term_elements = []

    if _type is not None:
        term_elements.append(term_type(_type))

    if source is not None:
        term_elements.append(term_source(source))

    if _id is not None:
        term_elements.append(term_id(_id))

    if value is not None:
        term_elements.append(term_value(value))

    return _term(*term_elements)


def corporate_author(_corporate_author_name=None):
    if _corporate_author_name is not None:
        return _corporate_author(_corporate_author_name)
    else:
        return _corporate_author('')  # Returning an empty element is allegedly fine in GIFT


def composed(_composed_value):
    return _composed(_composed_value)

E = _Meta()
_document_ids = E.document_ids
_record_admin_info = E.record_admin_info
_publication_date = E.publication_date
_source_institution = E.source_institution
_source_pagination_group = E.source_pagination_group
_content_date = E.content_date
_structured_name = E.structured_name
_corporate_author = E.corporate_author
_term = E.term
_bibliographic_ids = E.bibliographic_ids
document_titles = E.document_titles
source_citation_group = E.source_citation_group
descriptive_indexing = E.descriptive_indexing
meta = E.Meta
authors = E.authors
volume_number = E.volume_number
mcode = E.mcode
publication_title = E.publication_title
id = E.id
standard_ids = E.standard_ids
value = E.value
standard_date = E.standard_date
indexing_term = E.indexing_term
term_type = E.term_type
term_source = E.term_source
term_id = E.term_id
term_value = E.term_value
structured_date = E.structured_date
irregular = E.irregular
title_display = E.title_display
title_sort = E.title_sort
title_open_url = E.title_open_url
subtitle = E.subtitle
institution_name = E.institution_name
institution_location = E.institution_location
copyright_statement = E.copyright_statement
author = E.author
editor = E.editor
editors = E.editors
page_id_number = E.page_id_number
prefix = E.prefix
first_name = E.first_name
middle_name = E.middle_name
last_name = E.last_name
suffix = E.suffix
title = E.title
name = E.name
composed_name = E.composed_name
source_pagination = E.source_pagination
pagination_group = E.pagination_group
pagination = E.pagination
_composed = E.composed
content_type = E.content_type
source_citation = E.source_citation
month = E.month
day = E.day
year = E.year
day_of_week = E.day_of_week
ocr_confidence = E.ocr_confidence
total_pages = E.total_pages
languages = E.languages
language = E.language
sobriquet = E.sobriquet
publication_subtitle = E.publication_subtitle
holding_institution = E.holding_institution
reference_number = E.reference_number
reference_number_display = E.reference_number_display
geo_location = E.geo_location
organization = E.organization
product_content_type = E.product_content_type
content_filter = E.content_filter
folio = E.folio
start_number = E.start_number
range = E.range
ranges = E.ranges
begin_page = E.begin_page
end_page = E.end_page
publisher = E.publisher
place_of_publication = E.place_of_publication
imprint = E.imprint
imprint_composed = E.imprint_composed
edition = E.edition
edition_statement = E.edition_statement
number = E.number
series_info = E.series_info
issue_number = E.issue_number
