from abc import ABCMeta, abstractmethod
from lxml import etree
from gaia.error import GaiaError, GaiaSystemError
from gaia.xml.xml_dict import XmlDict
from gaia.log.log import Log
from gaia.dom.document_error import DocumentError

class ProjectDocumentAdapterError(GaiaSystemError):
    pass

#class GaiaDomAdapter(metaclass=ABCMeta):   # py3.2 syntax
class GaiaDomAdapter:                       # py2.7 syntax
    ''' Adapt a project-specific xml document to the 
        Gaia standard document object model.

        The idea is to extract Pages, Chunk, Clips and Links
        from an xml file and allow them to be changed and
        eventually written back to the xml file.

        These "GaiaDocumentAdapters" will encapsulate the xml
        of a particular project and provide standard ways
        of accessing the Gaia-relevant information.

        Subclasses can expect and use:
            self._etree

        and must provide:
            _get_document(self, data)
            _get_pages(self, data)
            _get_chunks(self, data)
            _get_clips(self, data)
            _get_links(self, data)
    '''
    __metaclass__ = ABCMeta # required for py 2.x (not 3.x)

    # TODO - eventually refactor '_IS_ABSENT_ occurances in the code to use GaiaDomAdapter.MISSING_FIELD_VALUE
    MISSING_FIELD_VALUE = '_IS_ABSENT_' # This value should be used if a tag has no value


    def __init__(self, xml_asset):
        self.xml_asset = xml_asset
        self._data = {} # this caches data to avoid re-parsing xml.
        # Hmm.. this doesn;t work :( ..?
        #parser = etree.XMLParser(remove_blank_text=True) # ignore whitespace _between_ tags
        #self._etree = etree.parse(xml_asset.fpath, parser=parser) # throws...TODO.
        self._etree = etree.parse(xml_asset.fpath) # throws...TODO.
        self._xml_dict = XmlDict(self._etree)
        self._log = Log.get_logger(self)

    def document(self):
        ' return the Document object for this Item. '
        
        if not self._data.has_key('document'):
            try:
                self._data['document'] = self._get_document()
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError('Failed to extract document info from document', xml_file=self.xml_asset.fname, errors=e)

            # this is a generic system requirement:
            if self.xml_asset.fbase != self._data['document'].dom_id:
                raise DocumentError('Document file name and id within xml file DO NOT MATCH!', xml_file_name=self.xml_asset.fname, internal_document_id=self._data['document'].dom_id)

        return self._data['document']

    def pages(self):
        ' return the Pages in this Document. '
        if not self._data.has_key('pages'):
            try:
                self._data['pages'] = self._get_pages() 
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError(xml_file=self.xml_asset.fname, errors=e)

        return self._data['pages']


    def chunks(self):
        ' return the Chunks in this Document. '
        if not self._data.has_key('chunks'):
            try:
                self._data['chunks'] = self._get_chunks() 
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError('Failed to extract chunks/articles from document!', xml_file=self.xml_asset.fname, errors=e)

        return self._data['chunks']

    def clips(self):
        ' return the Clips in this Document. '
        if not self._data.has_key('clips'):
            try:
                self._data['clips'] = self._get_clips() 
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError('Failed to extract Clips from document!', xml_file=self.xml_asset.fname, errors=e)

        return self._data['clips']

    def links(self, internal=True):
        ''' return the internal links in this Document.
        
            Note: "internal" links are links to anything that is available within one Item (eg a linked mp3 file),
            non-internal links are references to external things, eg other documents.

        '''
        #external: TODO??
        if not self._data.has_key('links'):
            try:
                self._data['links'] = self._get_links() 
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError('Failed to extract Links from document!', xml_file=self.xml_asset.fname, errors=e)

        return self._data['links']


    def asset_fnames(self):
        ' return the fnames for all assets that are referenced by this Document. '
        if not self._data.has_key('asset_fnames'):
            try:
                self._data['asset_fnames'] = self._asset_fnames() 
            except GaiaError, e:
                raise DocumentError(xml_file=self.xml_asset.fname, errors=e)
            except Exception, e:
                raise ProjectDocumentAdapterError('Failed to extract asset filenames from document', xml_file=self.xml_asset.fname, errors=e)

        return self._data['asset_fnames']

    def write(self, fpath=None):
        if not fpath:
            fpath = self.xml_asset.fpath

        self._etree.write(fpath, encoding="utf-8", xml_declaration=True)


    # --------------------------------------------------------------
    # The following abstract methods must be provided by sub-classes.
    # --------------------------------------------------------------
    @abstractmethod
    def _get_document(self): pass

    @abstractmethod
    def _get_pages(self): pass

    @abstractmethod
    def _get_chunks(self): pass

    @abstractmethod
    def _get_clips(self): pass

    @abstractmethod
    def _get_links(self): pass

    @abstractmethod
    def _asset_fnames(self): pass
