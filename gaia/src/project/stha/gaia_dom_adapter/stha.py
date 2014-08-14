from gaia.utils.errors_mixin import ErrorsMixin
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from gaia.dom.document_error import DocumentError
from gaia.dom.model.document import Document
from gaia.dom.model.page import Page
from gaia.dom.model.chunk import Chunk
#from gaia.dom.model.clip import Clip
#from gaia.dom.model.link import Link


class Stha(GaiaDomAdapter, ErrorsMixin):
    ' An adapter for STHA '

    def __init__(self, *args, **kwargs):
        GaiaDomAdapter.__init__(self, *args, **kwargs)
        ErrorsMixin.__init__(self)

    def _asset_fnames(self):
        # expect one image per page...

        #	<pageid colorimage="No" pageType="Body" isPartOf="Standard">STHA-1827-0204-0001</pageid>
        fnames = []
        for page in self.pages():
            fnames.append(page.info['_asset_fname'])

        errors = self.errors()  # Note: this can be set by used methods
        if errors:
            raise errors
        else:
            self._log.debug('expected asset fnames:', fnames=fnames)
            return fnames

    def _get_document(self):
        ' return a Document() object '

        issue_paths = [
            '/GALENP/Newspaper/issue/metadatainfo/newspaperID', # == STHA! ignore?
            '/GALENP/Newspaper/issue/id',
            '/GALENP/Newspaper/issue/is',
            '/GALENP/Newspaper/issue/da',
            '/GALENP/Newspaper/issue/pf',
            '/GALENP/Newspaper/issue/dw',
            '/GALENP/Newspaper/issue/ip',
            '/GALENP/Newspaper/issue/copyright',
            '/GALENP/Newspaper/issue/imdim', ]  # ignore?

        dom_id = self._xml_dict['/GALENP/Newspaper/issue/id']   # eg <id>STHA-1827-0204</id>
        #dom_name = self._xml_dict['/GALENP/Newspaper/issue/da'] # eg <da>February 04, 1827</da>    # odd chars cause problems :(
        dom_name = dom_id

        info = {}
        for path in issue_paths:
            self._get(info, path)

        return Document(dom_id, dom_name, info)

    def _get_pages(self): 
        pages = []
        dom_ids = set()

        for page in self._etree.getroot().findall('.//page'):
            page_xpath = self._etree.getpath(page)
            page_id = self._xml_dict[page_xpath + '/pageid']

            if page_id in dom_ids:
                self.add_error(DocumentError('Duplicate pageid!', pageid=page_id))  #Note: "pageid" (no underscore) to match xml page/pageid
            else:
                dom_ids.add(page_id)
                info = {}
                info['_asset_fname'] = page_id + '.jpg'    # save the asset name (there's some duplication here with asset fnames :( )

                source_page_xpath = page_xpath + '/pa'
                self._get(info, source_page_xpath)
                dom_name = info[source_page_xpath]
                pages.append(Page(page_id, dom_name, info)) # Note: use the full page_id (eg"STHA-1827-0204-0001") as a dom_id (cf just a nnumber in CHO)

        # TODO: check that dom_ids is a sequential and correct set of ids

        errors = self.errors()
        if errors:
            raise errors
        else:
            return pages

    def _get_chunks(self):
        chunks = []

        dom_ids = set()
        for article in self._etree.getroot().findall('.//page/article'):
            article_xpath = self._etree.getpath(article)
            article_id = self._xml_dict[article_xpath + '/id']

            if article_id in dom_ids:
                self.add_error(DocumentError('Duplicate article id!', article_id=article_id))
            else:
                dom_ids.add(article_id)
                info = {}

                for subtag in [ '/id', '/sc', '/pc', '/ti', '/ct',]:
                    self._get(info, article_xpath + subtag)

                dom_name = info[article_xpath + '/ti']    # eg <ti>Law and Police Summary</ti>

                page_ids = self._xml_dict[article_xpath + '/pi'] # returns a string or a list depending on how many exist
                #print "TUSH:pi ", str(page_ids)
                if not isinstance(page_ids, list):
                    page_ids = [page_ids,]

                clip_ids = self._xml_dict[article_xpath + '/ci'] # returns a string or a list depending on how many exist
                #print "TUSH: ci", clip_ids
                if isinstance(clip_ids, str):
                    clip_ids = [clip_ids,]

                dom_name = info[article_xpath + '/ti']    # eg <ti>Law and Police Summary</ti>
                chunks.append(Chunk(article_id, dom_name, info, page_ids, clip_ids))

                # il TODO 
                # clips/links...
                #<pi pgref="1">STHA-1827-0204-0001</pi>
                #<ci pgref="1" clip="1">STHA-1827-0204-0001-001-001</ci>
                #<ci pgref="1" clip="2">STHA-1827-0204-0001-001-002</ci>
                #<ci pgref="1" clip="3">STHA-1827-0204-0001-001-003</ci>

        errors = self.errors()
        if errors:
            raise errors
        else:
            return chunks
        
    def _get_clips(self):
        return [] # TODO

    def _get_links(self):
        ' "internal" links are links to anything that is available within one Item (eg a linked mp3 file) '
        return [] # TODO


    # utility methods --------------------------------------------------------
    def _get(self, info, xpath):
        ' get the information from xml(xpath) and put it into the "info" dict '
        val = self._xml_dict[xpath]
        if val is None:
            val = GaiaDomAdapter.MISSING_FIELD_VALUE #? (for UI: replaces mandatory=False)
        info[xpath] = val
