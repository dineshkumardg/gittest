from gaia.utils.errors_mixin import ErrorsMixin
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from gaia.dom.document_error import DocumentError
from gaia.dom.model.document import Document
from gaia.dom.model.page import Page
from gaia.dom.model.chunk import Chunk
#from gaia.dom.model.clip import Clip
from gaia.dom.model.link import AssetLink, DocumentLink
from gaia.error import GaiaCodingError
from project.cho.cho_content_type import ChoContentType


class _BadIdError(Exception):  # WARNING: this is for internal use only, DO NOT THROW THIS!! (is NOT a GaiaError).
    pass


class Cho(GaiaDomAdapter, ErrorsMixin):  # TODO change so that we use only valid xpaths + fix EG-469 xptahs being incorrect in gdom
    ' An adapter for ALL CHO types. '

    def __init__(self, *args, **kwargs):
        GaiaDomAdapter.__init__(self, *args, **kwargs)
        ErrorsMixin.__init__(self)
        self._related_links = None

    def _asset_fnames(self):
        # add one image per page...
        # Note: we're using a project-defined image type here 
        # _not_ via the config: this is ok as this is a cho-specific adapter.
        #fnames = [self._page_asset_fname(page.info['@id']) for page in self.pages()]   # TODO: error handling?
        fnames = [page.info['_asset_fname'] for page in self.pages()]   # TODO: error handling?

        # include mp3 / relatedMedia
        for link in self.links():
            #if link.info.has_key('_asset_fname'):           # Note: not all links will be related to assets in this Item.
                #fnames.append(link.info['_asset_fname'])
            if isinstance(link, AssetLink):
                fnames.append(link.asset_fname)

        self._log.debug('expected asset fnames:', fnames=fnames)
        return fnames

    def _page_asset_fname(self, pgref):
        ' WARNING: check self.errors() to see if anything failed after returning.'
        # Note: there's also now a pageImage tag that seems to have the file-name in it! hey ho :( ?
        doc_id = self.document().dom_id
        page_prefix = '_'.join(doc_id.split('_')[:-1]) # strip the last number part and replace it with a page-number

        try:
            fname = '%s_%04d.jpg' % (page_prefix, self._int_pgref(pgref))
        except _BadIdError, e: 
            self.add_error(DocumentError('missing or non-integer pgref in page', page_prefix=page_prefix))
            fname = 'ERROR' #?

        return fname

    def _get(self, info, xpath, create=False):  # WARNING if True and element does not exist then we would need to create those elements: which is a massive dev effort!
        ''' Get the information from xml(xpath) and put it into the "info" dict

            If create=True, the path will always eventually exist, either with
            it's real value, or if not present, the value "_IS_ABSENT_".
        '''
        try:
            val = self._xml_dict[xpath]
        except GaiaCodingError, e:
            if create:
                val = None
            else:
                raise e

        if val is None:
            val = GaiaDomAdapter.MISSING_FIELD_VALUE #? (for UI: replaces mandatory=False) # TODO: factor out to a generic place (constant in dom adapter?)

        # If we have a list, then we'll treast it all as separate fields by
        # fully qualifying the xpath (required for FIX UI).
        # WARNING: conversion MUST use same (qualified) xpaths for access.
        if isinstance(val, list):
            self._fill_dict_with_values_list(info, xpath, val)
        else:
            info[xpath] = val

    def _fill_dict_with_values_list(self, info, xpath, val):
        xparts = xpath.rsplit('/', 1)

        if len(xparts) > 1:
            part0 = xparts[0]
            part1 = '/' + xparts[1]
            is_attr = xparts[1].startswith('@') # is an attribute, not a normal node
        else:
            part0 = xparts[0]   # TODO: test this clause!
            part1 = ''
            is_attr = False

        xpath_qualifier = 1

        for each_value in val:
            if is_attr:
                qualified_xpath = '%s[%d]%s' % (part0, xpath_qualifier, part1)
            else:
                qualified_xpath = '%s%s[%d]' % (part0, part1, xpath_qualifier)

            info[qualified_xpath] = each_value
            xpath_qualifier += 1

    def _get_children(self, info, xpath):
        ' get the data from direct children of xml(xpath) and fill the "info" dict '
        # TODO: might need an exclusion list here?
        nodes = self._etree.xpath(xpath + '/*') #?

        for node in nodes:
            self._get(info, self._etree.getpath(node))
        try:
            del info[xpath] # we don't want the parent node. Make sure that the order of calls calls this LAST
        except KeyError, e:
            pass
        
    def _get_document(self):
        ' return a Document() object (shows up in Doc tab  in QA app)'
        ignore = ['/chapter/metadataInfo/ocr',
                  '/chapter/metadataInfo/mcode',
                  '/chapter/metadataInfo/assetID',
                  '/chapter/metadataInfo/contentDate',
                  '/chapter/metadataInfo/subDocumentType',
                  '/chapter/metadataInfo/relatedMedia', # assumed only ever 1 instance of this element, and that its represented by Links
                  ]

        dom_id = self._xml_dict['/chapter/metadataInfo/PSMID']
        dom_name = dom_id #?

        info = {}
        self._get(info, '/chapter/@contentType')
        self._get_children(info, '/chapter/metadataInfo')
        self._get_children(info, '/chapter/metadataInfo/sourceLibrary')
        self._get_children(info, '/chapter/metadataInfo/contentDate')
        self._get(info, '/chapter/metadataInfo/isbn', True)
        self._get(info, '/chapter/metadataInfo/issn', True)

        chapter_citation_book_value = self._xml_dict['/chapter/citation/book']
        citation_subtag = ChoContentType.content_type(chapter_citation_book_value, info['/chapter/metadataInfo/productContentType']) 
        self._get(info, '/chapter/citation/%s/totalPages' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/pubDate' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/author' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/titleGroup' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/volumeGroup' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/imprint' % citation_subtag)
        self._get_children(info, '/chapter/citation/%s/publicationPlace' % citation_subtag)

        self._get(info, '/chapter/citation/%s/byline' % citation_subtag, True)
        self._get(info, '/chapter/citation/%s/author/@type' % citation_subtag, True)
        self._get(info, '/chapter/citation/%s/author/@role' % citation_subtag, True)
        self._get(info, '/chapter/citation/%s/editionNumber' % citation_subtag, True)
        self._get(info, '/chapter/citation/%s/editionStatement' % citation_subtag, True)

        if citation_subtag == 'book':
            self._get(info, '/chapter/citation/book/seriesGroup/seriesTitle', True)
            self._get(info, '/chapter/citation/book/seriesGroup/seriesNumber', True)

        if citation_subtag == 'conference':
            self._get(info, '/chapter/citation/conference/conferenceGroup/conferenceName', True)
            self._get(info, '/chapter/citation/conference/conferenceGroup/conferenceLocation', True)

        if citation_subtag == 'meeting':
            self._get(info, '/chapter/citation/meeting/meetingGroup/meetingNumber', True)
            self._get(info, '/chapter/citation/meeting/meetingGroup/sponsoringOrganisation', True)
            self._get(info, '/chapter/citation/meeting/meetingGroup/meetingLocation', True)

        # Remove any unwanted info: might need to remove others here too..waiting for a QA Spec!
        for key in ignore:
            try:
                del info[key]
            except KeyError, e:
                pass

        return Document(dom_id, dom_name, info)

    def _get_pages(self):   # Note: This is a GOOD EXAMPLE OF HOW TO HANDLE ERRORS with the ErrorsMixin
        pages = []

        dom_id = 1

        for page in self._etree.findall('page'):
            page_xpath = self._etree.getpath(page)
            info = {}
            page_id = page.get('id')
            info.update({'@id': page_id})  # TO CHANGE?? TUSH: TODO? (use full xpath etc)..
            info.update({'_asset_fname': self._page_asset_fname(page_id)})    # save the asset name (there's some duplication here with asset fnames :( )
            info.update({'_id': dom_id})    # save the id ??? (TODO: push into base Page() etc objects??)

            source_page_xpath = page_xpath + '/sourcePage'
            self._get(info, source_page_xpath)
            self._get(info, page_xpath + '/article/text/textclip/footnote/word')

            dom_name = info[source_page_xpath]
            pages.append(Page(dom_id, dom_name, info))

            dom_id += 1

        errors = self.errors()  # Note: this can be set by _page_asset_fname() above
        if errors:
            raise errors
        else:
            return pages

    def _get_chunks(self):
        chunks = []
        ignore = ['/articleInfo/ocr',
                  '/articleInfo/assetID',]

        # FUTURE: TODO: check that all meeting articles are on the first? page only. (extra validation)
        links = []
        link_dom_id = 1

        dom_id = 1
        article_seq = 1

        for article in self._etree.findall('page/article'):
            article_xpath = self._etree.getpath(article)
            info = {}
            self._get(info, article_xpath + '/@type')
            self._get(info, article_xpath + '/@level')
            self._get(info, article_xpath + '/@id')
            self._get_children(info, article_xpath + '/articleInfo')
            self._get_children(info, article_xpath + '/articleInfo/author')
            #self._get(info, article_xpath + '/articleInfo/author/aucomposed', True)  # EG-469
            self._get_children(info, article_xpath + '/articleInfo/pubDate')
            
            self._get(info, article_xpath + '/articleInfo/issueNumber', True)
            self._get(info, article_xpath + '/articleInfo/issueTitle', True)
            self._get(info, article_xpath + '/articleInfo/byline', True)
            self._get(info, article_xpath + '/articleInfo/language', True)
            self._get(info, article_xpath + '/articleInfo/author/@type', True)
            #self._get(info, article_xpath + '/text/textclip/marginalia', True)  # EG-469
            for key in ignore:
                try:
                    del info[article_xpath + key]
                except KeyError, e:
                    pass

            page_ids = []
            for clip in article.findall('clip'):
                try:
                    page_ids.append(self._int_pgref(clip.get('pgref'))) # TODO: check with Sarah why these aren't always present!! :(
                except _BadIdError, e: 
                    self.add_error(DocumentError('missing or non-integer pgref in article', article_sequence_number=dom_id))

            if not page_ids:
                self.add_error(DocumentError('missing pgref in article tag', article_sequence_number=dom_id))
            else:
                title_xpath = article_xpath + '/articleInfo/title'
                self._get(info, title_xpath, True)

                if info[title_xpath] != GaiaDomAdapter.MISSING_FIELD_VALUE:
                    dom_name = info[title_xpath] # should this be mandatory (Sarah)??
                else:
                    id_xpath = article_xpath + '/@id'
                    dom_name = info[id_xpath]

                chunks.append(Chunk(dom_id, dom_name, info, clip_ids=None, page_ids=page_ids))

                # Note: we do this here because the context defines the source of the link (yuk!)
                # eg /chapter/page[297]/article/text/textclip[13]/relatedDocument[1]
                for related_doc in article.findall('.//relatedDocument'):
                    related_xpath = self._etree.getpath(related_doc)

                    dom_name = self._xml_dict[related_xpath]    # note: this can be empty
                    if not dom_name:
                        dom_name = 'link_%d' % link_dom_id
                    
                    info = {}
                    self._get(info, related_xpath + '/@docref')
                    self._get(info, related_xpath + '/@pgref')
                    self._get(info, related_xpath + '/@type')
                    
                    # <textclip>
                    #   <articlePage pgref="16">cho_sia_1963_02_0016</articlePage>
                    #   <relatedDocument type="footnote" docref="cho_dia_1962_000_000_0000" pgref="16">Documents, 1962, No. 128</relatedDocument>
                    try:
                        source = {'page':     self._mkid(self._xml_dict[related_xpath + '/../articlePage/@pgref']),
                                  'chunk':    dom_id, }     # Note: dom_id is the current *article/chunk* dom_id

                        target = {'document': self._xml_dict[related_xpath + '/@docref'],
                                  'page':     self._mkid(self._xml_dict[related_xpath + '/@pgref']),        #, is_optional=True),   # WARNING: samples need fixing!! TODO
                                  'chunk':    self._mkid(self._xml_dict[related_xpath + '/@articleref']),}   # , is_optional=True), }
                                  #'page':     self._mkid(self._xml_dict[related_xpath + '/@pgref'], is_optional=True),   # WARNING: samples need fixing!! TODO
                                  #'chunk':    self._mkid(self._xml_dict[related_xpath + '/@articleref'], is_optional=True), }

                        links.append(DocumentLink(link_dom_id, dom_name, info, source, target))           
                    except _BadIdError, e:
                        self.add_error(DocumentError('Bad relatedDocument link (problem with refs?)!', related_document_xpath=related_xpath, link_number=link_dom_id))

                    link_dom_id += 1
#
                dom_id += 1
                article_seq += 1

            self._related_links = links # for use later in _get_links()

            # Note: Illustrations are modelled as Binary Chunks.
            # in this schema, they are in the wrong place, ie in the article (for human xml review! :( )
            for illustration in article.findall('illustration'):
                illustration_xpath = self._etree.getpath(illustration)
                info = {}
                self._get(info, illustration_xpath + '/@pgref')
                self._get(info, illustration_xpath + '/@type')
                self._get(info, illustration_xpath + '/@colorimage')
                self._get(info, illustration_xpath + '/caption')

                try:
                    page_ids = [self._int_pgref(illustration.get('pgref')),]
                    # Don't do the following, but carry on round the loop if the above doesn't work.
                    dom_name = info[illustration_xpath + '/caption']
                    if dom_name == GaiaDomAdapter.MISSING_FIELD_VALUE:
                        dom_name = '%s_%s' % (info[illustration_xpath + '/@type'], str(dom_id))

                    chunks.append(Chunk(dom_id, dom_name, info, clip_ids=None, page_ids=page_ids, is_binary=True))
                    dom_id += 1 # Note: intentionally _NOT_ bumping up article_seq here (this is for error reporting: see above)
                except _BadIdError, e: 
                    self.add_error(DocumentError('missing or non-integer pgref in illustration', article_sequence_number=article_seq))

        errors = self.errors()
        if errors:
            raise errors
        else:
            return chunks
        
    def _get_clips(self):
        return [] # TODO

    def _get_links(self):
        ''' Currently there are mp3 files which are part of this item (relatedMedia)
            and links to other documents (relatedDocument).
        '''
        if not self._related_links:
            self.chunks() # make sure that self._get_chunks has been called as this is where we collect relatedDocument links (it's a crap data model!)

        links = self._related_links
        dom_id = len(links) + 1 # start at the next available sequence number

        for related_media in self._etree.findall('metadataInfo/relatedMedia'):
            # eg <relatedMedia id="cho_meet_2010_7771_001_0001.mp3" mediaType="Audio" dataType="mp3" duration="12.34" assetID=""/>
            related_xpath = self._etree.getpath(related_media)
            
            info = {}
            self._get(info, related_xpath + '/@mediaType')
            self._get(info, related_xpath + '/@dataType')
            self._get(info, related_xpath + '/@duration')
            
            asset_fname = self._xml_dict[related_xpath + '/@id']
            dom_name = asset_fname 
            #info['_asset_fname'] = dom_name    # TODO: check okay not to have this!
            links.append(AssetLink(dom_id, dom_name, info, asset_fname))           
            dom_id += 1

        return links

    # utility methods
    def _int_pgref(self, pgref_str):
        ' try to convert a string pgref to an int and raise exception if cannot '
        try:
            pgref = int(pgref_str)
            return pgref

        except TypeError, e:    # get this for int(None)
            raise _BadIdError()
        except ValueError, e:
            raise _BadIdError()
            #self.add_error(DocumentError('non-integer pgref in article', article_sequence_number=dom_id))

    def _mkid(self, id_str, is_optional=False):
        ''' Make a string into an ID string.

            Try to convert an xs:integer field (that can have leading zeroes) into a string version
            that can be used as an id (ie is conistently the same; with no leading zeroes)
            Raise exception if cannot unless it's optional, in whcih case, return None.
        '''
        try:
            normalised_id_string = str(int(id_str))
            return normalised_id_string

        except TypeError, e:    # get this for int(None)
            if is_optional:
                return None
            else:
                raise _BadIdError()
        except ValueError, e:
            raise _BadIdError()
