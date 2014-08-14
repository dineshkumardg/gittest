'''
Django Models for the Gaia Document Object Model *Index*

Note that the dom "id" fields are stored here as "dom_id".
(and separate database ids are generated).

WARNING! uniqueness of "dom_ids"s is intentionally NOT required.
Duplicates are added to the Index and the older versions
have their is_live flag set to False. This is a simple
way to do versioning.
'''
import logging
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from gaia.utils.safe_unicode import safe_formatted_unicode


class Item(models.Model):
    dom_id = models.CharField(max_length=1022, blank=False)
    dom_name = models.CharField(max_length=1022, blank=False)
    is_live = models.BooleanField(default=True)         # is_live means "has *not* been superceded by a new version of this Item"
    has_changed = models.BooleanField(default=False)    # has_changed means that the data has been "Fixed" (this is un-related to versions of items).
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'ItemIndex(id="#%s", dom_id="%s", dom_name="%s", created on "%s", is_live="%s", has_changed="%s")' % (self.id, self.dom_id, self.dom_name, self.date, self.is_live, self.has_changed)

    def __str__(self):
        return safe_formatted_unicode('ItemIndex(id="#%s", dom_id="%s", dom_name="%s", created on "%s", is_live="%s", has_changed="%s")', self.id, self.dom_id, self.dom_name, self.date, self.is_live, self.has_changed)

    class Meta:
        db_table = 'item'
    
    def save(self, *args, **kwargs):
        if '_avoid_recursion' in kwargs:
            del kwargs['_avoid_recursion']
        else:
            dom_id = self.__dict__['dom_id']    # Hmm.. can this ever not exist??
            older_versions = Item.objects.filter(dom_id=dom_id)
            if older_versions:
                for item in older_versions:
                    if item.is_live:
                        item.is_live = False
                        item.save(_avoid_recursion=True)
                        logging.warning('NEW VERSION of "%s" has been received (item.id="%s" is being superceded)' % (dom_id, item.id))

        super(Item, self).save(*args, **kwargs) # Save the new (live) item

    def chunk(self, chunk_dom_id):
        ' a convenience method to get a chunk by _id_ for this item '
        document = Document.objects.get(item=self)
        chunk = Chunk.objects.get(dom_id=chunk_dom_id, document=document)
        return chunk

    def chunks(self):
        ' a convenience method to get all related chunks '
        document = Document.objects.get(item=self)
        chunks = Chunk.objects.filter(document=document)
        return chunks

    def page(self, page_dom_id):
        ' a convenience method to get a page by _id_ for this item '
        document = Document.objects.get(item=self)
        page = Page.objects.get(dom_id=page_dom_id, document=document)
        return page

    def pages(self):
        ''' a convenience method to get all related pages.
            They are returned in *NO PARTICULAR ORDER*
        '''
        document = Document.objects.get(item=self)
        #pages = Page.objects.filter(document=document).order_by('dom_id')  # Can't use as srting-collation is no good :(
        pages = Page.objects.filter(document=document)  # NOTE: NO ORDERING!
        return pages

class Document(models.Model):
    dom_id = models.CharField(max_length=1022, blank=False)
    dom_name = models.CharField(max_length=1022, blank=False)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return 'DocumentIndex(id="#%s", dom_id="%s" dom_name="%s")' % (self.id, self.dom_id, self.dom_name)

    def __str__(self):
        return safe_formatted_unicode('DocumentIndex(id="#%s", dom_id="%s" dom_name="%s")', self.id, self.dom_id, self.dom_name)

    class Meta:
        db_table = 'document'

class Page(models.Model):
    dom_id = models.CharField(max_length=1022, blank=False)  # NOTE: do NOT have to be unique.
    dom_name = models.CharField(max_length=1022, blank=False)
    document = models.ForeignKey(Document)

    def __unicode__(self):
        return 'PageIndex(id="#%s", dom_id="%s" dom_name="%s")' % (self.id, self.dom_id, self.dom_name)

    def __str__(self):
        return safe_formatted_unicode('PageIndex(id="#%s", dom_id="%s" dom_name="%s")', self.id, self.dom_id, self.dom_name)

    class Meta:
        db_table = 'page'

class Chunk(models.Model):
    # Note: currently (for CHO) a Chunk directly relates to a Page.
    # In a sane project, it should relate via a Clip to a page. TODO later.
    dom_id = models.CharField(max_length=1022, blank=False)
    dom_name = models.CharField(max_length=1022, blank=False)
    document = models.ForeignKey(Document)
    pages = models.ManyToManyField(Page)
    is_binary = models.BooleanField(default=False)

    def __unicode__(self):
        return 'ChunkIndex(id="#%s", dom_id="%s" dom_name="%s" is_binary="%s")' % (self.id, self.dom_id, self.dom_name, self.is_binary)

    def __str__(self):
        return safe_formatted_unicode('ChunkIndex(id="#%s", dom_id="%s" dom_name="%s" is_binary="%s")', self.id, self.dom_id, self.dom_name, self.is_binary)

    class Meta:
        db_table = 'chunk'

class Clip(models.Model):
    dom_id = models.CharField(max_length=1022, blank=False)
    dom_name = models.CharField(max_length=1022, blank=False)
    page = models.ForeignKey(Page)

    def __unicode__(self):
        return 'ClipIndex(id="#%s", dom_id="%s" dom_name="%s")' % (self.id, self.dom_id, self.dom_name)

    def __str__(self):
        return safe_formatted_unicode('ClipIndex(id="#%s", dom_id="%s" dom_name="%s")', self.id, self.dom_id, self.dom_name)

    class Meta:
        db_table = 'clip'

class _Link(models.Model):   # do NOT use this table directly please!
    dom_id = models.CharField(max_length=1022, blank=False)
    dom_name = models.CharField(max_length=1022, blank=False)

    # source fields
    document = models.ForeignKey(Document)                  # as a minimum, a link is mentioned in a Document, and..
    chunk = models.ForeignKey(Chunk, blank=True, null=True) # ..may _optionally_ be associated with a Chunk
    page  = models.ForeignKey(Page,  blank=True, null=True)

    # TODO:? add source and target into str methods (or not)?
    def __unicode__(self):
        return 'LinkIndex(id="#%s", dom_id="%s" dom_name="%s")' % (self.id, self.dom_id, self.dom_name)

    def __str__(self):
        return safe_formatted_unicode('LinkIndex(id="#%s", dom_id="%s" dom_name="%s")', self.id, self.dom_id, self.dom_name)

    class Meta:
        db_table = 'link'

class AssetLink(_Link):
    asset_fname = models.CharField(max_length=512, blank=False)

    class Meta:
        db_table = 'asset_link'

class DocumentLink(_Link):
    # WARNING: The target fields are *strings* that refer to a dom_id (not name) , and
    # are NOT direct links within the index, They are resolved at runtime to the latest
    # matching index object with the target_xxx() methods
    unresolved_target_item = models.CharField(max_length=1022)  # Note: item, not document
    unresolved_target_chunk = models.CharField(max_length=1022)
    unresolved_target_page = models.CharField(max_length=1022)

    @property
    def target_item(self):
        ' get the latest version of the target item for this link (or return None) '
        try:
            target_item = Item.objects.get(dom_id=self.unresolved_target_item, is_live=True)
            return target_item
        except Item.DoesNotExist, e:
            return None
        
    @property
    def target_chunk(self):
        ' get the latest version of the target chunk for this link (or return None) '
        try:
            target_item = Item.objects.get(dom_id=self.unresolved_target_item, is_live=True)
            target_chunk = target_item.chunk(self.unresolved_target_chunk)
            return target_chunk
        except ObjectDoesNotExist, e:   # catch Item or Chunk DoesNotExist
            return None
        
    @property
    def target_page(self):
        ' get the latest version of the target page for this link (or return None) '
        #TODO
        try:
            target_item = Item.objects.get(dom_id=self.unresolved_target_item, is_live=True)
            target_page = target_item.page(self.unresolved_target_page)
            return target_page
        except ObjectDoesNotExist, e:   # catch Item or Page DoesNotExist
            return None
        
    class Meta:
        db_table = 'document_link'
