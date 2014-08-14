import os
import json


class _DomFileStore:
    ''' The folder structure (e.g. for v3 of one item) is like this:
        (note that the numbers are examples of IDs which may be any string).
            item/v3/79.xml
            item/v3/79_1.jpg
            item/v3/79_2.jpg
            item/v3/79_2a.mp3
            item/v3/document/79/info.txt
            item/v3/page/79_1/info.txt
            item/v3/page/79_2/info.txt
            item/v3/chunk/1/info.txt
            item/v3/chunk/2/info.txt
            item/v3/clip/1/info.txt
            item/v3/link/1/info.txt

        This is a convenience mixin for DomStore to hold just the
        file-based code (this is generally bad practice! :) )

        Change methods change the info stored for an item. 
        This implements simple "replace-only" functionality (ie not add/delete)
        (to support search/replace features).

        Note: the change dictionary parameters hold the new values
        for changed fields only (ie not a whole info object).
    '''
    def add_item(self, item, item_index_id):
        self._log.enter(item=item, item_index_id=item_index_id)

        item_dir = self._item_dir(item.dom_id, item_index_id)

        self._add_document(item, item_dir)
        self._add_pages(item, item_dir)
        self._add_chunks(item, item_dir)
        self._add_clips(item, item_dir)
        self._add_links(item, item_dir)

        self._log.exit(item=item, item_index_id=item_index_id)

    def doc_info(self, item_dom_name, item_index_id, document_dom_id):
        ' return the doc_info as a JSON string (use json.loads() to de-serialize. '
        info, doc_dir = self._read_doc_info(item_dom_name, item_index_id, document_dom_id)
        return info

    def get_changes(self, dom_item, item_index_id): 
        ''' return all of the *CHANGEABLE* info objects for an Item as *plain dicts* (NOT as JSON objects)

            WARNING: do NOT use this to get ALL of the info (links and clips are NOT returned)!
        '''
        item_dom_name = dom_item.dom_name

        doc_info = self.doc_info(item_dom_name, item_index_id, dom_item.document().dom_id)
        pages_info = self.pages_info(item_dom_name, item_index_id)
        chunks_info = self.chunks_info(item_dom_name, item_index_id)

        json_item_info = [doc_info, ]
        json_item_info.extend(pages_info)
        json_item_info.extend(chunks_info)

        changes = [json.loads(info) for info in json_item_info]
        return sorted(changes, key=lambda k: k['_dom_id'])

    def change_item_info(self, item_dom_name, item_index_id, doc_info_changes={}, page_info_changes={}, chunk_info_changes={}):  # TODO clip_and link info_changes?
        for dom_id in doc_info_changes.keys():
            self._change_doc_info(item_dom_name, item_index_id, dom_id, doc_info_changes[dom_id])

        for dom_id in page_info_changes.keys():
            self._change_info(item_dom_name, item_index_id, dom_id, page_info_changes[dom_id], 'page')

        for dom_id in chunk_info_changes.keys():
            self._change_info(item_dom_name, item_index_id, dom_id, chunk_info_changes[dom_id], 'chunk')

    def _change_info(self, item_dom_name, item_index_id, dom_id, changes, doc_type_fname):
        self._log.enter(item_dom_name=item_dom_name, item_index_id=item_index_id, dom_id=dom_id, changes=changes, doc_type_fname=doc_type_fname)

        info_dir = self._item_dir(item_dom_name, item_index_id, doc_type_fname, dom_id)
        json_info_fpath = open(os.path.join(info_dir, 'info.txt')).read()
        info = json.loads(json_info_fpath)
        info.update(changes)
        self._write_info(info_dir, info)

        self._log.exit()

    def _change_doc_info(self, item_dom_name, item_index_id, dom_id, doc_info_changes):
        ''' change document info.

            doc_changes is a dict of doc_name to changed fields, eg:
                {doc_dom_id: {changed_field_1: new_value1;
                              changed_field_2: new_value2}}
        '''
        self._log.enter(item_dom_name=item_dom_name, item_index_id=item_index_id, doc_info_changes=doc_info_changes)

        json_info, doc_dir = self._read_doc_info(item_dom_name, item_index_id, dom_id)
        info = json.loads(json_info)
        info.update(doc_info_changes)
        self._write_info(doc_dir, info)

        self._log.exit()

    def _add_document(self, item, item_dir):
        # item/document/79/info.txt (for a document with id=79)
        document = item.document()
        doc_dir = self._mkdir(item_dir, 'document', document.dom_id)
        self._log.debug('adding document into doc_dir="%s"' % doc_dir)

        self._write_info(doc_dir, document.info)

    def _read_doc_info(self, item_dom_name, item_index_id, document_dom_id):
        ' return the JSON format of the doc info '
        doc_dir = self._item_dir(item_dom_name, item_index_id, 'document', document_dom_id)

        info = open(os.path.join(doc_dir, 'info.txt')).read()
        return info, doc_dir

    def _write_info(self, doc_dir, info):
        f = open(os.path.join(doc_dir, 'info.txt'), 'w+')
        json.dump(info, f)
        f.close()

    def link_info(self, item_dom_name, item_index_id, link_dom_id):
        ''' return the link info as a JSON string (use json.loads() to de-serialize 
            return None if there aren't any links.

            Note that for historical and backwards-compatibility reasons, we
            are collecting together both Asset and Document Links.

            FUTURE: In a future project (we won't do this in Gaia/Chatham House),
            we might want to split this into asset and document links to match everything else.
        '''
        _dir = self._item_dir(item_dom_name, item_index_id, 'link', link_dom_id)
        fname = os.path.join(_dir, 'info.txt')
        info = None # TODO: review: not sure this is a good idea (maybe return an empty json dict/array string?)
        if os.path.exists(fname):
            info = open(fname).read()

        return info

    def clip_info(self, item_dom_name, item_index_id, clip_dom_id):
        ''' return the clip info as a JSON string (use json.loads() to de-serialize 
            return None if there aren't any clips 
        '''
        _dir = self._item_dir(item_dom_name, item_index_id, 'clip', clip_dom_id)
        fname = os.path.join(_dir, 'info.txt')
        info = None # TODO: review: not sure this is a good idea (maybe return an empty json dict/array string?)
        if os.path.exists(fname):
            info = open(fname).read()

        return info

    def page_info(self, item_dom_name, item_index_id, page_dom_id):
        ''' return the page info as a JSON string (use json.loads() to de-serialize.
            (It is impossible to have an item without pages according to the gaia DOM).
        '''
        _dir = self._item_dir(item_dom_name, item_index_id, 'page', page_dom_id)
        info = open(os.path.join(_dir, 'info.txt')).read()
        return info

    def pages_info(self, item_dom_name, item_index_id):
        ' return an UNORDERED list of page_info for all the pages for this item.'
        item_pages_dir = self._item_dir(item_dom_name, item_index_id, 'page')
        pages = os.listdir(item_pages_dir)

        # WARNING: *** THIS WIL BE ALPHA SORTED: *NOT* in numeric order!
        # not ideal, but ok, as ong as callers don't expect this to be ordered. 
        pages_info = []

        for page_dir in pages:
            fpath = os.path.join(item_pages_dir, page_dir, 'info.txt')
            info = open(fpath).read()
            pages_info.append(info)

        return pages_info

    def chunk_info(self, item_dom_name, item_index_id, chunk_dom_id):
        ''' return the chunk info as a JSON string (use json.loads() to de-serialize. 
            (It is impossible to have an item without chunks according to the gaia DOM).
        '''
        _dir = self._item_dir(item_dom_name, item_index_id, 'chunk', chunk_dom_id)
        info = open(os.path.join(_dir, 'info.txt')).read()
        return info

    def chunks_info(self, item_dom_name, item_index_id):
        ' return a list (*NOT* ordered) of chunk_info for all the chunks for this item.'
        item_chunks_dir = self._item_dir(item_dom_name, item_index_id, 'chunk')
        chunks = os.listdir(item_chunks_dir)

        chunks_info = []

        for chunk_dir in chunks:
            fpath = os.path.join(item_chunks_dir, chunk_dir, 'info.txt')
            info = open(fpath).read()
            chunks_info.append(info)

        return chunks_info

    def _add_pages(self, item, item_dir):
        # item/page/79/info.txt (for a page with id=79)
        pages = item.pages()

        for page in pages:
            page_dir = self._mkdir(item_dir, 'page', page.dom_id)
            self._log.debug('adding page into: "%s"' % page_dir)

            f = open(os.path.join(page_dir, 'info.txt'), 'w+')
            json.dump(page.info, f)
            f.close()

    def _add_chunks(self, item, item_dir):
        # item/chunk/79/info.txt (for a chunk with id=79)
        chunks = item.chunks()

        for chunk in chunks:
            chunk_dir = self._mkdir(item_dir, 'chunk', chunk.dom_id)
            self._log.debug('adding chunk into chunk_dir', chunk=chunk, chunk_dir=chunk_dir)

            f = open(os.path.join(chunk_dir, 'info.txt'), 'w+')
            json.dump(chunk.info, f)
            f.close()

    def _add_clips(self, item, item_dir):
        # item/clip/79/info.txt (for a clip with id=79)
        clips = item.clips()

        for clip in clips:
            clip_dir = self._mkdir(item_dir, 'clip', clip.dom_id)
            self._log.debug('adding clip into: "%s"' % clip_dir)

            f = open(os.path.join(clip_dir, 'info.txt'), 'w+')
            json.dump(clip.info, f)
            f.close()

    def _add_links(self, item, item_dir):
        # item/link/79/info.txt (for a link with id=79)
        links = item.asset_links()
        links.extend(item.document_links()) # TODO check!

        for link in links:
            link_dir = self._mkdir(item_dir, 'link', link.dom_id)
            self._log.debug('adding link into: "%s"' % link_dir)

            f = open(os.path.join(link_dir, 'info.txt'), 'w+')
            json.dump(link.info, f)
            f.close()

    def _mkdir(self, root_dir, sub_dir, dom_id):
        _dir = os.path.join(root_dir, sub_dir, str(dom_id))

        if not os.path.exists(_dir):
            os.makedirs(_dir)   # TODO: should probably catch IOERROR, OSERROR here?

        return _dir
