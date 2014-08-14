from qa.models import FeedFile, DocumentFinalId, PageFinalId, ChunkFinalId, MCodes
from qa.common_view import CommonView
from qa.view_decorator import class_view_decorator
from django.views.generic import ListView
from django.contrib.auth.decorators import permission_required
from collections import OrderedDict


@class_view_decorator(permission_required('qa.can_qa'))
class FeedFileItemView(CommonView):
    paginate_by = 35
    template_name = 'qa/report/feed_file_items.html'
    feed_ids = {}

    def get_data(self):
        feed = self.request.GET.get("feed_file")
        return FeedFile.objects.filter(fname=feed).order_by('-when')

    def _get_asset_ids(self, query_set):
        if query_set:
            feed_ids = {}
            for each_feed in query_set:# to get the list of all items in the feedfile

                for item in each_feed.items.all():
                    feed_ids[item.dom_id] = {}
                    page_final_ids = []
                    chunk_final_ids = []
                    doc_final_ids = []

                    if self.request.GET.get("show_asset_ids") == 'true':

                        for each_page in item.pages():# page ids for the item
                            page_ids = PageFinalId.objects.filter(page = each_page).order_by('page')
                            for eachpage in page_ids:
                                page_final_ids.append(str(eachpage.final_id))
                        feed_ids[item.dom_id]["page_id"] =  sorted(page_final_ids)

                        for each_chunk in item.chunks(): # chunk ids for the item
                            chunk_ids= ChunkFinalId.objects.filter(chunk = each_chunk).order_by('chunk')
                            for eachpage in chunk_ids:
                                chunk_final_ids.append(str(eachpage.final_id))
                        feed_ids[item.dom_id]["chunks_id"] =  sorted(chunk_final_ids)

                        doc_ids = item.document() # document ids for the item
                        doc_final_ids =  DocumentFinalId.objects.filter(document=doc_ids)
                        doc_ids = []

                        for each_doc in doc_final_ids:
                            doc_ids.append(str(each_doc.final_id))
                        feed_ids[item.dom_id]["document_id"] = doc_ids

            #x = self._show_missing_mcodes(feed_ids)

            return OrderedDict(sorted(feed_ids.items(), key=lambda t: t[0]))

    def _show_missing_mcodes(self, psmids):  # TODO  show if an mcode is missing?!
        return psmids

    def _get_mcode_string(self, mcode):
        # if we've got more then one MCODE then put an OR between them
        mcode_string = ''
        for each_mcode in mcode:
            if mcode_string == '':
                mcode_string = each_mcode
            elif not each_mcode in mcode_string:
                 mcode_string = mcode_string + ' OR ' +  each_mcode
        return mcode_string

    # overrides the base class method
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        ids = self._get_asset_ids(context[self.context_object_name])
        context['ids'] = ids

        mcodes = MCodes.get_mcodes(ids)
        context['content_set_definiton'] = self._get_mcode_string(mcodes)

        return context
