from gaia.error import GaiaError
from gaia.dom.model.item import Item
from project.cho.cho_content_type import ChoContentType
from gaia.xml.xml_dict import XmlDict


class NamedAuthorityItem(Item):
    def __init__(self, dom_id, dom_name, assets, config, chunks=None, document=None, date=None, is_live=None):
        Item.__init__(self, dom_id, dom_name, assets, config)
        etree = self._get_dom_adapter()._etree
        self._xml_dict = XmlDict(etree)  # access xpaths via this as code, from conversion, expects same return interface

        # used for unit test patching
        if chunks is not None:
            self.chunks = chunks
        if document is not None:
            self.document = document
        if date is not None:
            self.date = date
        if is_live is not None:
            self.is_live = is_live

        if chunks is not None:
            chunk_dom_ids = []
            for chunk in self.chunks:
                chunk_dom_ids.append(chunk.dom_id)
            self.ordered_chunk_dom_ids = sorted(chunk_dom_ids)  # order so that matches CHOA-1074

    def named_authority_details(self):
        named_authority_info = []
        article_index = 1

        date = str(self.date)[:19]

        if self.dom_name[:8] in ['cho_meet', 'cho_chbp', 'cho_chrx', 'cho_rpax']:  # single retrievable items
            # meetings are arranged differently!
            article_title = self._xml_dict['/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()]
            authors = self._document_meta_authors()

            document_final_id = self.document.get_final_id()  # use document asset id not chunk for these types
            if authors is not None:
                for author in authors:
                    named_authority_info.append({'item_id': self.dom_id, 'ingest_date': date, 'psmid': self.dom_name, 'article_id': article_index, 'asset_id': document_final_id, 'gift_article_title': article_title, 'gift_author': author})
            else:
                named_authority_info.append({'item_id': self.dom_id, 'ingest_date': date, 'psmid': self.dom_name, 'article_id': article_index, 'asset_id': document_final_id, 'gift_article_title': article_title, 'gift_author': ''})
        else:
            pages = self._xml_dict['/chapter/page']

            for page in range(1, len(pages) + 1):
                articles = self._xml_dict['/chapter/page[%s]/article' % page]

                if articles is not None:
                    for article in  range(1, len(articles) + 1):
                        article_title = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/title' % (page, article)]
                        article_id = self._xml_dict['/chapter/page[%s]/article[%s]/@id' % (page, article)]

                        if article_title is not None:
                            article_final_id = self._article_final_id(article_index)
                            article_authors = self._article_conference_series_meta_authors(page, article)

                            if article_authors is not None:
                                for author in article_authors:
                                    named_authority_info_entry = {'item_id': self.dom_id, 'ingest_date': date, 'psmid': self.dom_name, 'article_id': article_index, 'asset_id': article_final_id, 'gift_article_title': article_title, 'gift_author': author}
                                    named_authority_info.append(named_authority_info_entry)
                            else:
                                    named_authority_info_entry = {'item_id': self.dom_id, 'ingest_date': date, 'ingest_date': date, 'psmid': self.dom_name, 'article_id': article_index, 'asset_id': article_final_id, 'gift_article_title': article_title, 'gift_author': ''}
                                    named_authority_info.append(named_authority_info_entry)
                            article_index += 1

        return named_authority_info

    def _article_conference_series_meta_authors(self, page, article):
        authors = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author' % (page, article)]
        if authors is None:
            return None

        if isinstance(authors, basestring):
            author_count = 1
        else:
            author_count = len(authors)

        _authors = []
        for author_index in range(1, author_count + 1):
            role = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/@role' % (page, article, author_index)]

            if role == u'author':
                prefix = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/prefix' % (page, article, author_index)]
                first = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/first' % (page, article, author_index)]
                middle = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/middle' % (page, article, author_index)]
                last = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/last' % (page, article, author_index)]
                suffix = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/suffix' % (page, article, author_index)]

                aucomposed = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/aucomposed' % (page, article, author_index)]

                if first is None or last is None:
                    name = ''

                    if prefix is not None:
                        name += prefix

                    if first is not None:
                        if name is not '':
                            name += ' '
                        name += first

                    if middle is not None:
                        if name is not '':
                            name += ' '
                        name += middle

                    if last is not None:
                        if name is not '':
                            name += ' '
                        name += last

                    if suffix is not None:
                        if name is not '':
                            name += ' '
                        name += suffix

                    _authors.append(name)
                else:
                    _authors.append(aucomposed)

        if len(_authors) > 0:
            corporate_author = self._xml_dict['/chapter/page[%s]/article[%s]/articleInfo/byline' % (page, article)]
            if corporate_author is not None:
                _authors.append(corporate_author)

            return _authors
        else:
            return None

    def _article_final_id(self, article):
        target_chunk_dom_id = self.ordered_chunk_dom_ids[article - 1]
        for chunk in self.chunks:
            if chunk.dom_id == target_chunk_dom_id:
                return chunk.get_final_id()

    def _document_meta_authors(self):
        authors = []

        author_list = self._xml_dict['/chapter/citation/%s/author' % self.content_type()]

        if author_list is not None:
            author_count = len(author_list)
            for author_index in range(1, author_count + 1):
                role = self._xml_dict['/chapter/citation/%s/author[%s]/@role' % (self.content_type(), author_index)]

                if role == u'author':
                    prefix = self._xml_dict['/chapter/citation/%s/author[%s]/prefix' % (self.content_type(), author_index)]
                    first = self._xml_dict['/chapter/citation/%s/author[%s]/first' % (self.content_type(), author_index)]
                    middle = self._xml_dict['/chapter/citation/%s/author[%s]/middle' % (self.content_type(), author_index)]
                    last = self._xml_dict['/chapter/citation/%s/author[%s]/last' % (self.content_type(), author_index)]
                    suffix = self._xml_dict['/chapter/citation/%s/author[%s]/suffix' % (self.content_type(), author_index)]

                    aucomposed = self._xml_dict['/chapter/citation/%s/author[%s]/aucomposed' % (self.content_type(), author_index)]

                    if first is None or last is None:
                        name = ''

                        if prefix is not None:
                            name += prefix

                        if first is not None:
                            if name is not '':
                                name += ' '
                            name += first

                        if middle is not None:
                            if name is not '':
                                name += ' '
                            name += middle

                        if last is not None:
                            if name is not '':
                                name += ' '
                            name += last

                        if suffix is not None:
                            if name is not '':
                                name += ' '
                            name += suffix

                        authors.append(name)

                    else:
                        authors.append(aucomposed)

        if len(authors) > 0:
            return authors
        else:
            return None

    def content_type(self):
        chapter_citation_book_value = self._xml_dict['/chapter/citation/book']
        return ChoContentType.content_type(chapter_citation_book_value, self.product_content_type())

    def product_content_type(self):
        product_content_type_xpath = '/chapter/metadataInfo/productContentType'
        product_content_type = self._xml_dict[product_content_type_xpath]
        if product_content_type is None:
            raise GaiaError('product_content_type is None')
        else:
            return product_content_type
