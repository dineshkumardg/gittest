from qa.models import FeedFile, DocumentFinalId, PageFinalId, ChunkFinalId, Document, Page, Chunk, Item
from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from django.http import Http404


@class_view_decorator(permission_required('qa.can_qa'))
class FeedFileView(FilteredCommonView):
    paginate_by = 35
    template_name = 'qa/report/feed_file_index.html'

    filter_field = 'group'
    search_field = 'fname'
    sort_fields_list = ['when', 'fname', 'group', 'num_docs']
    sort_name_list = ['date', 'feed file name', 'group', 'docs']
    date_filter_field = 'when'

    def get_data(self):
        self.search_feed = self.request.GET.get("search_feed")
        self.search_for = self.request.GET.get("search_for")

        if (self.search_feed is None and self.search_for is None):
            # return unfiltered data 
            return FeedFile.objects.all().order_by('-when')
        else:
            search_feed = self.search_feed.strip()

            # TODO the pagination system is completely broken, if you try and query different data sets

            if self.search_for == "item":  # search for an item in feed file
                query = FeedFile.objects.filter(items__dom_name__contains=search_feed).distinct().order_by('-when')
                self.paginate_by = len(query)
                return query

            elif self.search_for == "feed":  # search for a feed file
                query = FeedFile.objects.filter(fname__contains=search_feed).order_by('-when')
                self.paginate_by = len(query)
                return query

            elif self.search_for == "asset_id":  # search for an asset_id
                feed_file_ids = self._search_for_asset_id(search_feed)
                self.paginate_by = len(feed_file_ids)
                return FeedFile.objects.filter(id__in=feed_file_ids).order_by('-when')

    def _search_for_asset_id(self, search_feed):
        feed_files = self._document_with_asset_id(search_feed)  # TNIHUJ419297655

        if not feed_files:
            feed_files = self._chunks_with_asset_id(search_feed)  # KSSTTF200022521

        if not feed_files:
            feed_files = self._pages_with_asset_id(search_feed)  # AALAXS296488370

        return feed_files

    def _after_filter_sort_search(self, data):
        feeds = list(data)

        feeds_with_type = []

        for each_feed in feeds:
            content_types = []

            for item in each_feed.items.all():
                con_type =  item.dom_id.split('_')[1]
                if not  con_type in content_types:
                    content_types.append(con_type)

            each_feed.type = content_types
            feeds_with_type.append(each_feed)

        return feeds_with_type

    def _document_with_asset_id(self, asset_id):
        # follow the joins across, also see joins in: https://docs.djangoproject.com/en/dev/topics/db/queries/
        feed_file_ids = []

        document_final_ids = DocumentFinalId.objects.filter(final_id=asset_id)

        for document_final_id in document_final_ids:
            documents = Document.objects.filter(id=document_final_id.document_id)

            for document in documents:
                items = Item.objects.filter(id=document.item_id)  # show it whether its live or not

                for item in items:
                    feed_files = FeedFile.objects.filter(items__id=item.id)

                    for feed_file in feed_files:
                        feed_file_ids.append(feed_file.id)

        return feed_file_ids

    def _chunks_with_asset_id(self, asset_id):
        feed_file_ids = []

        chunk_final_ids = ChunkFinalId.objects.filter(final_id=asset_id)
        for chunk_final_id in chunk_final_ids:

            chunks = Chunk.objects.filter(id=chunk_final_id.chunk_id)
            for chunk in chunks:

                documents = Document.objects.filter(id=chunk.document_id)
                for document in documents:

                    items = Item.objects.filter(id=document.item_id)  # show it whether its live or not
                    for item in items:

                        feed_files = FeedFile.objects.filter(items__id=item.id)
                        for feed_file in feed_files:
                            feed_file_ids.append(feed_file.id)

        return feed_file_ids

    def _pages_with_asset_id(self, asset_id):
        feed_file_ids = []

        page_final_ids = PageFinalId.objects.filter(final_id=asset_id)
        for page_final_id in page_final_ids:

            pages = Page.objects.filter(id=page_final_id.page_id)
            for page in pages:

                documents = Document.objects.filter(id=page.document_id)
                for document in documents:

                    items = Item.objects.filter(id=document.item_id)  # show it whether its live or not
                    for item in items:

                        feed_files = FeedFile.objects.filter(items__id=item.id)
                        for feed_file in feed_files:
                            feed_file_ids.append(feed_file.id)

        return feed_file_ids
