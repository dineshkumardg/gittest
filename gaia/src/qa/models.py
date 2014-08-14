''' Models for the Gaia QA Web Application

Note: To see the db schema use:
    src/scripts/dev/python manage.py TUSH_PC sqlall qa      # Note: is empty!
    src/scripts/dev/python manage.py TUSH_PC sqlall index   # shows the tables

This is saved in:
    ../db_scripts/<project>/create_models.sql
(and that script is the authoratative source).
(see also scripts/dev/dump_models.sh)

If you change these models, you *MUST* add a script in
    ../db_scripts/<project>/alter_db_00n.sql
to alter the database appropriately.
'''

import logging
from django.contrib.auth.models import User
import gaia.dom.index.models
from django.db import models
import qa.models
from django.core.exceptions import ObjectDoesNotExist
from gaia.utils.safe_unicode import safe_formatted_unicode
from gaia.error import GaiaError
from django.db.models import Q  # used for an OR query
from django.conf import settings
from gaia.config.config import get_config
from gaia.egest.outbox import Outbox
from gaia.dom.model.item import Item as DomItem
from lxml import etree
from project.cho.hard_coded_mcodes import HardCodedMCodes


class MissingFinalId(GaiaError):
    ''' An error class to represent xxxFinalId.DoesNotExist
        (because we need to detect missing final_ids in error cases).
    '''
    pass


# Proxies for the basic Gaia DOM objects -----------
class Item(gaia.dom.index.models.Item):
    ''' WARNING: do *NOT* use any other tables directly!

        This is NOT a relational model, it's an object model, therefore you
        *must* use the Item.* access methods to maintain relationships correctly!
    '''
    class Meta:
        proxy = True

    # These 3 methods are _copied_ from dom.index.models so that they return objects of the right _type_
    # and hence acces thej derived class's methods!
    # This is a very annoying thing to have to do, but I can't see any other solition with Django inheritance :(
    # Ultimately I think this means that django models should be pure data-only things (no behaviour).
    # ref: test_web_box.py
    def chunks(self):
        ' a convenience method to get all related chunks '
        document = qa.models.Document.objects.get(item=self)
        chunks = qa.models.Chunk.objects.filter(document=document)
        return chunks

    def chunk(self, chunk_dom_id):
        ' a convenience method to get a chunk by _id_ for this item '
        document = Document.objects.get(item=self)
        chunk = qa.models.Chunk.objects.get(dom_id=chunk_dom_id, document=document)
        return chunk

    def pages(self):
        ''' a convenience method to get all related pages.
            They are returned in *NO PARTICULAR ORDER*
        '''
        document = qa.models.Document.objects.get(item=self)
        pages = qa.models.Page.objects.filter(document=document)  # NOTE: NO ORDERING!
        return pages

    def document(self):
        return qa.models.Document.objects.get(item=self)

    def document_links(self):
        ' a convenience method to get all related document_links '
        document = qa.models.Document.objects.get(item=self)
        links = qa.models.DocumentLink.objects.filter(document=document)
        return links

    def document_link(self, link_dom_id):
        ' a convenience method to get one related document_link '
        document = qa.models.Document.objects.get(item=self)
        link = qa.models.DocumentLink.objects.get(document=document, dom_id=link_dom_id)
        return link

    def is_fully_linked(self):
        ''' An item can be "complete", but any related/linked Items may not yet be available.

            Hence, this checks for "outside" completeness versus is_complete() checking for "internal"-completeness.
            Note that this only checks immediate links (and does NOT walk the graph of consequent links)
        '''
        document = qa.models.Document.objects.get(item=self)
        links = qa.models.DocumentLink.objects.filter(document=document)

        _is_fully_linked = True

        # for each link, check that unresolved targets can get resolved (ie the target is there).
        for link in links:
            if link.unresolved_target_item and link.target_item is None:
                _is_fully_linked = False
                break

            if link.unresolved_target_chunk and link.target_chunk is None:
                _is_fully_linked = False
                break

            if link.unresolved_target_page and link.target_page is None:
                _is_fully_linked = False
                break

        return _is_fully_linked

    # Action/set methods ----------------------------------------------------------------------
    def track(self, username):
        ' A convenience method to record activity for an item '
        logging.info('Recording QA view of item with id "%s"' % self.id)
        activity = ItemActivity(item_id=self.id, username=username)
        activity.save()

    def reject(self, reason, err_type='QA'):
        ' Reject this item due to a QA problem. '
        logging.info('REJECTING Item FROM QA (reason="%s", err_type="%s", item="%s")' % (reason, err_type, str(self)))
        self._set_status(ItemStatus.REJECTED)
        self._add_error(err_type, reason)

    def error(self, err_type, err_msg):
        ' Flag this item as ERRoneous '
        logging.info('ERRORing Item (err_type="%s", err_msg="%s", item="%s")' % (err_type, err_msg, str(self)))
        self._set_status(ItemStatus.ERROR)
        self._add_error(err_type, err_msg)

    def ready_for_release(self):
        logging.info('Marking Item as READY_FOR_RELEASE (item="%s")' % (str(self)))
        self._set_status(ItemStatus.READY_FOR_RELEASE)

    def ready_for_release_only_xml(self):
        logging.info('Marking Item as READY_FOR_RELEASE and RELEASING ONLY XML FILES (item="%s")' % (str(self)))
        self._set_status(ItemStatus.READY_FOR_RELEASE_ONLY_XML)

    def ready_for_release_only_callisto(self):  # TODO ADD code
        logging.info('Marking Item as READY_FOR_RELEASE and RELEASING ONLY CALLISTO FILES (item="%s")' % (str(self)))
        self._set_status(ItemStatus.READY_FOR_RELEASE_ONLY_CALLISTO)

    def released(self):
        logging.info('Marking Item as RELEASED (item="%s")' % (str(self)))
        self._set_status(ItemStatus.RELEASED)

    def ready_for_qa(self):
        logging.info('Marking Item as IN_QA (item="%s")' % (str(self)))
        self._set_status(ItemStatus.IN_QA)

    def with_approval(self):
        try:
            approval = Approval.objects.filter(item_id=self.id).order_by('-id')[0]
            if approval.approved == True:
                return True
        except (ObjectDoesNotExist, IndexError) as e:
            pass

        return False

    @classmethod
    def set_released(cls, item_id):
        logging.debug('Marking Item as RELEASED (item_id="%s")..retrieving item.' % (str(item_id)))
        item = Item.objects.get(pk=item_id)
        item.released()

    @classmethod
    def set_qa(cls, item_id):
        logging.debug('Marking Item as RELEASED (item_id="%s")..retrieving item.' % (str(item_id)))
        item = Item.objects.get(pk=item_id)
        item.ready_for_qa()

    @classmethod
    def set_error(cls, item_id, err_type, err_msg):
        logging.debug('ERRORing Item (err_type="%s", err_msg="%s", item_id="%s")..retrieving item' % (err_type, err_msg, str(item_id)))
        item = Item.objects.get(pk=item_id)
        item.error(err_type, err_msg)

    @classmethod
    def release_next(cls, limit=None):
        ''' A convenience method to take items off the "ready for release and read for release only xml" queue.

            Returns the list of item_ids and changes their state.
            Supply a limit number if you you want to restrain the list, eg to 10 items.
            item will be in QA status if only CALLISTO is RELEASES
            item will be in RELEASED states if either XML or both are released

            New feature:
            release type by type, so it can create feed file for each content type

            | meet | feed_file | conference | feed_file | journal | feed_file | book | feed_file...
        '''
        # get all items
        all_released_item = ItemStatus.objects.filter(Q(status=ItemStatus.READY_FOR_RELEASE_ONLY_XML, item__is_live=True) | Q(status=ItemStatus.READY_FOR_RELEASE, item__is_live=True)| Q(status=ItemStatus.READY_FOR_RELEASE_ONLY_CALLISTO, item__is_live=True)) 

        # put them into corresponding content type list.
        meeting = []            # meet
        conference_series = []  # bcrc, iprx
        report = []             # rpax, chrx, chbp
        survey = []             # sbca, siax, dsca, diax, byil,             rsxx,
        journal = []            # iaxx, wtxx, binx,              rfpx, rfpc,
        book = []               # book
        others = []             # other extra types, just in case

        for item_status in all_released_item:
            con_type =  item_status.item.dom_name.split('_')[1]
            if con_type == "meet":  # meeting
                meeting.append(item_status)
            elif con_type == "bcrc" or con_type == "iprx":  # conference series
                conference_series.append(item_status)
            elif con_type == "rpax" or con_type == "chrx" or con_type == "chbp":    # report
                report.append(item_status)
            elif con_type == "sbca" or con_type == "siax" or con_type == "dsca" or con_type == "diax" or con_type == "byil" or con_type == "rsxx":    # survey
                survey.append(item_status)
            elif con_type == "iaxx" or con_type == "wtxx" or con_type == "binx" or con_type == "rfpx" or con_type == "rfpc":    # journal
                journal.append(item_status)
            elif con_type == "book":    # book
                book.append(item_status)
            else:
                others.append(item_status)

        group = []
        group.append(meeting)
        group.append(conference_series)
        group.append(report)
        group.append(survey)
        group.append(journal)
        group.append(book)
        group.append(others)

        create_feed = False

        # return released jobs to egest mgr type by type
        for type_list in group:
            if len(type_list) != 0:
                if limit:
                    if limit <= len(type_list):
                        item_statuses = type_list[:limit]
                    elif limit > len(type_list):
                        item_statuses = type_list[:limit]
                        create_feed = True
                else:
                    item_statuses = type_list
                    create_feed = True

                ids = []
                names = []
                release_type = []
                for item_status in item_statuses:
                    ids.append(item_status.item.id)
                    names.append(item_status.item.dom_name)

                    if item_status.status == ItemStatus.READY_FOR_RELEASE_ONLY_XML:
                        release_type.append('xml')

                    elif item_status.status == ItemStatus.READY_FOR_RELEASE_ONLY_CALLISTO:
                        release_type.append('callisto')

                    elif item_status.status == ItemStatus.READY_FOR_RELEASE:
                        release_type.append('both')
                    item_status.status = ItemStatus.EXPORTING
                    item_status.save()

                return ids, names, release_type, create_feed

        # work here means group is empty
        return [], [], [], create_feed

    # Query/get methods ----------------------------------------------------------------------
    @classmethod
    def in_importing(cls):
        return cls._in_status(ItemStatus.IMPORTING)

    @classmethod
    def in_qa(cls):
        return cls._in_status(ItemStatus.IN_QA)

    @classmethod
    def in_ready_for_release(cls):
        return cls._in_status(ItemStatus.READY_FOR_RELEASE)

    @classmethod
    def in_ready_for_release_only_xml(cls):
        return cls._in_status(ItemStatus.READY_FOR_RELEASE_ONLY_XML)

    @classmethod
    def in_exporting(cls):
        return cls._in_status(ItemStatus.EXPORTING)

    @classmethod
    def in_released(cls):
        return cls._in_status(ItemStatus.RELEASED)

    @classmethod
    def in_archived(cls):
        return cls._in_status(ItemStatus.ARCHIVED)

    @classmethod
    def in_rejected(cls):
        return cls._in_status(ItemStatus.REJECTED)

    @classmethod
    def in_error(cls):
        return cls._in_status(ItemStatus.ERROR)

    @classmethod
    def _in_status(cls, status):
        ' return the set of *live* items in a given state. '
        logging.debug('getting list of items that are in status %s' % status)
        item_ids = [item_status.item_id for item_status in ItemStatus.objects.filter(status=status)]
        items = Item.objects.filter(pk__in=item_ids, is_live=True).order_by('-id')
        return items

    @classmethod
    def rejections(cls):
        logging.debug('getting list of items that been rejected (newest first)')
        item_ids = [item_status.item_id for item_status in ItemStatus.objects.filter(status=ItemStatus.REJECTED)]
        items = Item.objects.filter(pk__in=item_ids).order_by('-date')
        return items

    # private methods ----------------------------------------------------------------------
    def _set_status(self, new_status):
        ' A convenience method to set or change the status of an item '
        logging.info('Changing the state of Item "%s" to "%s"' % (self.id, new_status))
        item_status, created = ItemStatus.objects.get_or_create(item_id=self.id, defaults={'status': new_status})
        item_status.status = new_status  # not really sure why we need this: defaults above should do it??
        item_status.save()

    def _add_error(self, err_type, err_msg):
        logging.info('Adding an error for Item (err_type="%s", err_msg="%s", item="%s")' % (err_type, err_msg, str(self)))
        item_error = ItemError(item=self, err_type=err_type, err_msg=err_msg)
        item_error.save()


class Document(gaia.dom.index.models.Document):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for Document (final_id="%s", document="%s")' % (final_id, str(self)))
        fid, created = DocumentFinalId.objects.get_or_create(document_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)

    def get_final_id(self):
        ' Get a "final_id" for this object '
        try:
            final_id_obj = DocumentFinalId.objects.get(document=self)   # should only ever be one match.
            fid = final_id_obj.final_id
            logging.debug('Getting Final ID for Document (final_id="%s", document="%s")' % (fid, str(self)))
            return fid
        except DocumentFinalId.DoesNotExist, e:
            raise MissingFinalId(for_object=self)


class Page(gaia.dom.index.models.Page):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for Page (final_id="%s", page="%s")' % (final_id, str(self)))
        fid, created = PageFinalId.objects.get_or_create(page_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)

    def get_final_id(self):
        ' Get a "final_id" for this object '
        try:
            final_id_obj = PageFinalId.objects.get(page=self)   # should only ever be one match.
            fid = final_id_obj.final_id
            logging.debug('Getting Final ID for Page (final_id="%s", page="%s")' % (fid, str(self)))
            return fid
        except PageFinalId.DoesNotExist, e:
            raise MissingFinalId(for_object=self)

    def track(self, username):
        ' A convenience method to record activity for a page '
        logging.debug('Recording QA activity for page with id %s' % self.id)
        activity = PageActivity(page_id=self.id, username=username)
        activity.save()


class Chunk(gaia.dom.index.models.Chunk):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for Chunk (final_id="%s", chunk="%s")' % (final_id, str(self)))
        fid, created = ChunkFinalId.objects.get_or_create(chunk_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)

    def get_final_id(self):
        ' Get a "final_id" for this object '
        try:
            final_id_obj = ChunkFinalId.objects.get(chunk=self)   # should only ever be one match.
            fid = final_id_obj.final_id
            logging.debug('Getting Final ID for Chunk (final_id="%s", chunk="%s")' % (fid, str(self)))
            return fid
        except ChunkFinalId.DoesNotExist, e:
            raise MissingFinalId(for_object=self)

    def track(self, username):
        ' A convenience method to record activity for a chunk '
        logging.debug('Recording QA activity for chunk with id %s' % self.id)
        activity = ChunkActivity(chunk_id=self.id, username=username)
        activity.save()


class Clip(gaia.dom.index.models.Clip):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for Clip (final_id="%s", clip="%s")' % (final_id, str(self)))
        fid, created = ClipFinalId.objects.get_or_create(clip_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)


class AssetLink(gaia.dom.index.models.AssetLink):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for AssetLink (final_id="%s", link="%s")' % (final_id, str(self)))
        fid, created = AssetLinkFinalId.objects.get_or_create(link_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)


class DocumentLink(gaia.dom.index.models.DocumentLink):
    class Meta:
        proxy = True

    def set_final_id(self, final_id):
        ' Set a "final_id" for this object '
        logging.debug('Setting Final ID for DocumentLink (final_id="%s", link="%s")' % (final_id, str(self)))
        fid, created = DocumentLinkFinalId.objects.get_or_create(link_id=self.id)
        fid.final_id = final_id
        fid.save()
        # TODO: would be nice to handle this in save() so that it's completely transparent (and would not require a separate save)

    @property
    def target_chunk(self):
        ' get the latest version of the target chunk for this link (or return None) '
        try:
            target_item = qa.models.Item.objects.get(dom_id=self.unresolved_target_item, is_live=True)
            target_chunk = target_item.chunk(self.unresolved_target_chunk)
            return target_chunk
        except ObjectDoesNotExist, e:  # catch Item or Chunk DoesNotExist
            return None


class ItemStatus(models.Model):
    IMPORTING = 100  # being ingested
    IN_QA = 300  # ready for QA
    READY_FOR_RELEASE = 600  # ready for egest, release both xml and callisto
    READY_FOR_RELEASE_ONLY_XML = 609  # ready for egest and release only xml
    READY_FOR_RELEASE_ONLY_CALLISTO = 610  # ready for egest and release only callisto
    EXPORTING = 611  # being egested
    RELEASED = 700  # egest finished successfully
    ARCHIVED = 777  # has been copied to the long-term Archive storage.
    REJECTED = 799  # rejected during QA
    ERROR = 999  # some random error (eg conversion failure) has stopped progress for this item

    # TODO: add more ERROR types? - e.g.
    # ERROR_CONVERSION - cho into gift failure
    # ERROR_TRANSFER_AGENT - transport / ftp failure

    CHOICES = (
            (IMPORTING, 'Importing'),
            (IN_QA, 'In QA'),
            (READY_FOR_RELEASE, 'Ready For Release'),
            (READY_FOR_RELEASE_ONLY_XML, 'Ready For Release Only Xml'),
            (READY_FOR_RELEASE_ONLY_CALLISTO, 'Ready For Release Only Callisto'),
            (EXPORTING, 'Exporting'),
            (RELEASED, 'Released'),
            (REJECTED, 'Rejected'),
            (ARCHIVED, 'Archived'),
            (ERROR, 'ERROR'),
    )

    # safer to do this in an init, but just be careful please (changes above MUST be copied below)!
    CHOICES_DICT = {
            IMPORTING: 'Importing',
            IN_QA: 'In QA',
            READY_FOR_RELEASE: 'Ready For Release',
            READY_FOR_RELEASE_ONLY_XML: 'Ready For Release Only Xml',
            READY_FOR_RELEASE_ONLY_CALLISTO: 'Ready For Release Only callisto',
            EXPORTING: 'Exporting',
            RELEASED: 'Released',
            REJECTED: 'Rejected',
            ARCHIVED: 'Archived',
            ERROR: 'ERROR',
    }

    item = models.ForeignKey(Item)
    status = models.IntegerField(choices=CHOICES, blank=False)
    when = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'ItemStatus(status="%s", when="%s", item="%s")' % (self.CHOICES_DICT[self.status], self.when, str(self.item))

    def __str__(self):
        return safe_formatted_unicode('ItemStatus(status="%s", when="%s", item="%s")', self.CHOICES_DICT[self.status], self.when, str(self.item))

    #@classmethod
    #def in_qa(cls):
        #status_in_qa = ItemStatus.objects.filter(status=ItemStatus.IN_QA).select_related('item')
        #return [item_status.item for item_status in status_in_qa]

    class Meta:
        db_table = 'item_status'
        verbose_name_plural = 'Item Status'


class QaActivity(models.Model):
    username = models.CharField(max_length=30, blank=False)  # Django auth username - max_length=30
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'QaActivity(username="%s", date="%s")' % (self.username, str(self.date))

    def __str__(self):
        return safe_formatted_unicode('QaActivity(username="%s", date="%s")', self.username, str(self.date))

    class Meta:
        abstract = True


class ItemActivity(QaActivity):
    item = models.ForeignKey(Item)

    class Meta:
        db_table = 'item_qa_activity'
        verbose_name = "Item QA Activity"


class PageActivity(QaActivity):
    page = models.ForeignKey(Page)

    class Meta:
        db_table = 'page_qa_activity'
        verbose_name = "Page QA Activity"


class ChunkActivity(QaActivity):
    chunk = models.ForeignKey(Chunk)

    class Meta:
        db_table = 'chunk_qa_activity'
        verbose_name = "Chunk QA Activity"


class ItemError(models.Model):
    item = models.ForeignKey(Item)
    when = models.DateTimeField(auto_now_add=True)
    err_type = models.CharField(max_length=32)  # NOTE SHORT LENGTH
    err_msg = models.CharField(max_length=2048)  # NOTE: max size for error messages (eg from UI)

    def __unicode__(self):
        return 'ItemError(err_type="%s", err_msg="%s", item="%s", when="%s")' % (self.err_type, self.err_msg, str(self.item), self.when)

    def __str__(self):
        return safe_formatted_unicode('ItemError(err_type="%s", err_msg="%s", item="%s", when="%s")', self.err_type, self.err_msg, str(self.item), self.when)

    class Meta:
        db_table = 'item_errors'
        verbose_name_plural = 'Item Errors'


class IngestError(models.Model):
    provider_name = models.CharField(max_length=24)
    when = models.DateTimeField(auto_now_add=True)
    report = models.CharField(max_length=307200)

    def __unicode__(self):
        return 'IngestError(provider_name="%s", when="%s", report="%s")' % (self.provider_name, self.when, self.report)

    def __str__(self):
        return safe_formatted_unicode('IngestError(provider_name="%s", when="%s", report="%s")', self.provider_name, self.when, self.report)

    class Meta:
        db_table = 'ingest_error'
        verbose_name_plural = 'Ingest Errors'

    @classmethod
    def add_error(cls, provider_name, report):
        ' Add a new Gaia Error for a provider` '
        logging.info('Recording an IngestError (provider_name="%s", report="%s")' % (provider_name, report))

        err = IngestError(provider_name=provider_name, report=report)
        err.save()

    @classmethod
    def provider_errors(cls, provider_name):
        ' return all of the errors for a provider '
        errs = IngestError.objects.filter(provider_name=provider_name)
        return errs


# ------------------------------------------------------------------------------
# Note: unfortunately if a class is a PROXY, it cannot use multiple inheritance.
class _FinalId(models.Model):
    # This is the target-platform's "final" unique object id
    # eg for LST, an "asset id" for each gift document, or
    # for GOLD it would be a ZZ number (in string form)
    final_id = models.CharField(max_length=128)

    class Meta:
        abstract = True  # this pushes the field into each sub-class table


class DocumentFinalId(_FinalId):
    document = models.ForeignKey(Document)

    class Meta:
        db_table = 'document_final_id'


class PageFinalId(_FinalId):
    page = models.ForeignKey(Page)

    class Meta:
        db_table = 'page_final_id'


class ChunkFinalId(_FinalId):
    chunk = models.ForeignKey(Chunk)

    class Meta:
        db_table = 'chunk_final_id'


class ClipFinalId(_FinalId):
    clip = models.ForeignKey(Clip)

    class Meta:
        db_table = 'clip_final_id'


class AssetLinkFinalId(_FinalId):
    link = models.ForeignKey(AssetLink)

    class Meta:
        db_table = 'asset_link_final_id'


class DocumentLinkFinalId(_FinalId):
    link = models.ForeignKey(DocumentLink)

    class Meta:
        db_table = 'document_link_final_id'


class FeedFile(models.Model):
    # id # used as an id within the file name
    fname = models.CharField(max_length=64)
    when = models.DateTimeField(auto_now_add=True)
    group = models.CharField(max_length=64)  # aka "functional type"
    num_docs = models.CharField(max_length=64)  # number of document_instances inside the feed
    items = models.ManyToManyField(Item)  # a feed file contains (objects from) a number of Items

    def __unicode__(self):
        return 'FeedFile(id="%s", fname="%s", when="%s", group="%s", num_docs="%s")' % (self.id, self.fname, self.when, self.group, self.num_docs)

    def __str__(self):
        return safe_formatted_unicode('FeedFile(id="%s", fname="%s", when="%s", group="%s", num_docs="%s")', self.id, self.fname, self.when, self.group, self.num_docs)

    class Meta:
        db_table = 'feed_file'

    @classmethod
    def create(cls, fname, group, num_docs, items):
        ' a convenience wrapper to create a new FeedFie with items '
        ff = FeedFile(fname=fname, group=group, num_docs=num_docs)
        ff.save()
        ff.items.add(*items)  # Note: no need to save again
        return ff


class MCodes(models.Model):
    mcode = models.CharField(max_length=4)
    psmid = models.CharField(max_length=50)
    publication_title = models.CharField(max_length=250)

    def __unicode__(self):
        return 'MCodes(id="%s", mcode="%s", psmid="%s", publication_title="%s")' % (self.id, self.mcode, self.psmid, self.publication_title)

    def __str__(self):
        return safe_formatted_unicode('MCodes(id="%s", mcode="%s", psmid="%s", publication_title="%s")', self.id, self.mcode, self.psmid, self.publication_title)

    class Meta:
        db_table = 'm_codes'

    '''
    SELECT m_codes.psmid, count(*)
    FROM
      public.m_codes
    GROUP BY m_codes.psmid
    ORDER BY COUNT(*) DESC;
    '''
    @classmethod
    def psmid_present(cls, psmids):
        for psmid in psmids:
            mcode = MCodes.objects.filter(psmid=psmid)
            if len(mcode) > 0:
                return True
        return False

    @classmethod
    def get_mcodes(cls, psmids):  # TODO allow a single psmid and not always a list?
        # get list psmid's and return a list of matching mcode's - ignores any psmid's that do not have mcode's
        mcodes = []

        for psmid in psmids:
            hard_coded_mcode = HardCodedMCodes.mcode_from_psmid(psmid[:12])
            if hard_coded_mcode is not None:
                mcodes.append(hard_coded_mcode)
            else:
                # do a straight lookup against the psmid
                mcode = cls.objects.filter(psmid=psmid)
                if len(mcode) == 1 and mcode[0].mcode is not u'':
                    mcodes.append(mcode[0].mcode)

        # sort the mcodes
        return sorted(mcodes)


class Approval(models.Model):
    item = models.ForeignKey(Item)
    approved = models.BooleanField(default=False)
    notes = models.CharField(max_length=250)
    who = models.ForeignKey(User)
    when = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Approval(id="%s", item="%s", approved="%s", notes="%s", who="%s", when="%s")' \
               % (self.id,
                  self.item,
                  self.approved,
                  self.notes,
                  self.who,
                  self.when)

    def __str__(self):
        return safe_formatted_unicode('Approval(id="%s", item="%s", approved="%s", notes="%s", who="%s", when="%s")',
                                      self.id,
                                      self.item,
                                      self.approved,
                                      self.notes,
                                      self.who,
                                      self.when)

    class Meta:
        db_table = 'approval'


class Language(models.Model):
    psmid = models.CharField(max_length=50)
    article_id = models.IntegerField()
    lang = models.CharField(max_length=50)

    PSMID_NOT_FOUND_IN_GAIA = 'N/A: psmid not in gaia'
    ARTICLE_NOT_FOUND_IN_GAIA = 'N/A: articleInfo/title xpath not found'

    def article_title(self):
        try:
            # we have to get the title from the xml!
            config = get_config(settings.CONFIG_NAME)
            outbox = self._get_outbox(config)

            item_name = self.psmid
            assets = outbox.assets(item_name)

            item = DomItem(item_name, item_name, assets, config)  # inside the outbox outbox

            if item.xml_asset() is None:
                return Language.PSMID_NOT_FOUND_IN_GAIA

            xml_tree = etree.parse(item.xml_asset().fpath)
            if self.psmid[:8] in ['cho_meet', 'cho_chbp', 'cho_chrx', 'cho_rpax']:  # single retrievable items
                article_titles = xml_tree.xpath('/chapter/citation/*/titleGroup/fullTitle')
            else:
                article_titles = xml_tree.xpath('/chapter/page/article/articleInfo/title')

            return article_titles[self.article_id - 1].text
        except (TypeError, IndexError):
            # logging.error("exception=%s" % str(e))
            return Language.ARTICLE_NOT_FOUND_IN_GAIA

    @classmethod
    def langs(cls, psmid):
        return [language.lang for language in Language.objects.filter(psmid=psmid)]

    def _get_outbox(self, config):
        return Outbox(config.outbox)

    def __unicode__(self):
        return 'Language(id="%s", psmid="%s", article_id="%s", lang="%s")' \
               % (self.id,
                  self.psmid,
                  self.article_id,
                  self.lang)

    def __str__(self):
        return safe_formatted_unicode('Language(id="%s", psmid="%s", article_id="%s", lang="%s")',
                                      self.id,
                                      self.psmid,
                                      self.article_id,
                                      self.lang)

    class Meta:
        db_table = 'language'


class RejectReason(models.Model):
    item = models.ForeignKey(Item)
    reason = models.CharField(max_length=2000)  # less than ItemError.err_msg
    who = models.ForeignKey(User)
    when = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'RejectReason(id="%s", item="%s", reason="%s", who="%s", when="%s")' \
               % (self.id,
                  self.item,
                  self.reason,
                  self.who,
                  self.when)

    def __str__(self):
        return safe_formatted_unicode('RejectReason(id="%s", item="%s", reason="%s", who="%s", when="%s")',
                                      self.id,
                                      self.item,
                                      self.reason,
                                      self.who,
                                      self.when)

    class Meta:
        db_table = 'reject_reason'
