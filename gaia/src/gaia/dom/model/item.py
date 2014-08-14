from gaia.log.log import Log
from gaia.schema.schema import Xsd, Dtd
from gaia.dom.model.dom_error import GaiaDomError
from gaia.dom.model.link import AssetLink, DocumentLink


class ItemError(GaiaDomError):
    pass


class NoDocument(ItemError):
    pass


class ItemIncompleteWarning(ItemError):
    pass


class ItemAndDocumentNameMismatch(ItemError):
    pass


class Item:
    ''' A container for everything that makes up one whole document

        ie Assets (files such as the Document file (xml), Page Files (images), Media files: eg mp3, etc)
        and the Gaia DOM Data objects.
    '''

    def __init__(self, dom_id, dom_name, assets, config):
        self.dom_id = dom_id
        self.dom_name = dom_name
        self.assets = assets
        self.config = config
        self._log = Log.get_logger(self)
        self._dom_adapter = None    # created on demand.
        self._xml_asset = None    # created on demand.
        self._binary_assets = None    # created on demand.

    def xml_asset(self):
        if not self._xml_asset:
            for asset in self.assets:
                if asset.ftype == 'xml':
                    self._xml_asset = asset
                    break

        return self._xml_asset

    def image_assets(self):
        ' return all assets which are images '
        return [asset for asset in self.assets if asset.is_image()]

    def audio_video_assets(self):
        ' return all assets which are either audio or video files '
        return [asset for asset in self.assets if asset.is_audio() or asset.is_video()]

    def binary_assets(self):
        ' return all assets other than the xml asset '
        return [asset for asset in self.assets if asset.ftype != 'xml']

    def _get_dom_adapter(self):
        if self._dom_adapter:
            return self._dom_adapter

        xml_asset = self.xml_asset()

        if not xml_asset:
            raise NoDocument()

        cls = self.config.dom_adapter_factory.adapter_class(xml_asset.fname)
        self._dom_adapter = cls(xml_asset)

        return self._dom_adapter

    def document(self):
        return self._get_dom_adapter().document()

    def pages(self):
        return self._get_dom_adapter().pages()

    def chunks(self):
        return self._get_dom_adapter().chunks()

    def clips(self):
        return self._get_dom_adapter().clips()

    def asset_links(self):
        ' This returns links to assets of this item '
        return [link for link in self._get_dom_adapter().links() if isinstance(link, AssetLink)]

    def document_links(self):
        ' This returns links to external (ie other, related) documents '
        return [link for link in self._get_dom_adapter().links() if isinstance(link, DocumentLink)]

    def _check_complete(self):  # throws ItemIncompleteWarning
        asset_fnames = [asset.fname for asset in self.assets]
        reqd_fnames = self._get_dom_adapter().asset_fnames()

        for fname in reqd_fnames:
            if fname not in asset_fnames:
                self._log.warning('incomplete item', xml_document_requires='\n' + str(sorted(reqd_fnames)))  # split into 3 to make easier to read!
                self._log.warning('incomplete item', current_assets='\n' + str(sorted(asset_fnames)))
                raise ItemIncompleteWarning(item_name=self.dom_id, missing_at_least=fname)

    def is_complete(self):
        ''' An Item is "complete" if all the parts that should be present are,
            ie all the assets referred to within the xml file are available.

            Note: this has the side-effect of validating the xml against the schema.
        '''

        # first check that we have a valid xml file, if not, we can't check anything!
        xml_asset = self.xml_asset()
        if xml_asset:
            schema_fpath = self.config.schema_fpath
            if schema_fpath.endswith('.xsd'):
                Xsd.validate(xml_asset.fpath, self.config.schema_fpath)
            else:
                Dtd.validate(xml_asset.fpath, self.config.schema_fpath)

        try:
            # make sure the Item id matches the document id (this should always be true).
            # (but can mis-match when a folder name is wrong)
            if self.dom_id != self.document().dom_id:
                raise ItemAndDocumentNameMismatch('The item name and document name should be the same, but are not!', item_name=self.dom_id, document_name=self.document().dom_id)

            self._check_complete()
            return True
        except NoDocument, e:
            self._log.warning('Item is not yet complete (missing the xml file)', item_name=self.dom_id)
            return False
        except ItemIncompleteWarning, e:
            self._log.warning(str(e))
            return False

    def etoc_info(self, ordered_final_asset_ids):
        """
        # stuff that might have been 'FIX'd 
        web_box = WebBox(config)
        item_changes = web_box.get_changes(item)
        source_xml_dict = CachedXmlDict(tree, *item_changes)

        xpath = '/chapter/page[%s]/article[%s]/articleInfo/title' % (page, article)
        title_display = source_xml_dict[xpath]
        """

        tree = self._get_dom_adapter()._etree
        etoc_info = []
        article_counter = 1

        pages = tree.xpath('/chapter/page')
        for page in range(1, len(pages) + 1):
            articles = tree.xpath('/chapter/page[%s]/article' % page)

            for article in  range(1, len(articles) + 1):
                article_id_xpath = tree.xpath('/chapter/page[%s]/article[%s]/@id' % (page, article))
                article_id = article_id_xpath[0]

                article_title = tree.xpath('/chapter/page[%s]/article[%s]/articleInfo/title' % (page, article))

                if len(article_title) > 0:
                    article_title_text = article_title[0].text
                    asset_id = ordered_final_asset_ids[article_counter - 1]

                    etoc_id = tree.xpath('/chapter/page[%s]/article[%s]/@level' % (page, article))

                    article_type = tree.xpath('/chapter/page[%s]/article[%s]/@type' % (page, article))
                    if article_type is not None:
                        if len(article_type) != 1:
                            article_type_text = article_type
                        else:
                            article_type_text = article_type[0]

                    etoc_indentation = ''
                    for etoc in range(2, int(etoc_id[0]) + 1):
                        etoc_indentation += '++++'

                    etoc_info_entry = {'article_id_real': article_id, 'article_id': article_counter, 'article_title': article_title_text, 'etoc_id': etoc_id[0], 'etoc_indentation': etoc_indentation, 'asset_id': asset_id, 'article_type_text': article_type_text}
                    self._log.debug(etoc_info_entry)

                    etoc_info.append(etoc_info_entry)
                    article_counter += 1

        return etoc_info

    def __str__(self):
        return 'Item (dom_id="%s", dom_name="%s")' % (self.dom_id, self.dom_name)
