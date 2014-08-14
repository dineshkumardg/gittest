import csv
import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connection
from qa.models import Item, Document, Chunk, Page, AssetLink, DocumentLink, MCodes,\
    Approval
from gaia.log.log import Log
from gaia.web.web_box import WebBox
from gaia.config.config import get_config
from gaia.egest.outbox import Outbox
from gaia.dom.model.item import Item as DomItem
from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from project.cho.hard_coded_mcodes import HardCodedMCodes


@class_view_decorator(permission_required('qa.can_qa'))
class ItemListView(FilteredCommonView):
    template_name = "qa/items.html"

    search_field = ['dom_name', 'mcode']
    sort_fields_list = ['date', 'ingest_count', 'mcode', 'is_fully_linked', 'dom_id', 'with_approval', 'notes', 'who', 'when']
    sort_name_list = ['ingested', 'ingest_count', 'mcode', 'complete', 'psmid', 'approved', 'notes (40 chars. visible; max. 250 chars.)', 'who', 'when']  # ordered to reflect what we see in ui

    def _get_data_using_model(self):
        all_items_in_qa = Item.in_qa()

        items_and_mcodes = []
        for item in all_items_in_qa:

            #item_status = ItemStatus.objects.filter(item=item)[0]
            if item.is_live == True:  # and item_status.status != ItemStatus.REJECTED:
                mcode = MCodes.get_mcodes([item.dom_id])
                if len(mcode) > 0:
                    item.mcode = mcode[0]
                else:
                    item.mcode = ''

                try:
                    approval = Approval.objects.filter(item_id=item.id).order_by('-id')[0]  # most recent one is shown
                    item.approved = approval.approved
                    item.notes = approval.notes
                    item.who = approval.who
                    item.when = approval.when
                except (ObjectDoesNotExist, IndexError):
                    item.approved = False
                    item.notes = ''
                    item.who = ''
                    item.when = ''

            items_and_mcodes.append(item)

        return items_and_mcodes

    def _get_ingest_count_using_sql(self):
        sql = 'SELECT dom_name, count(dom_name) as ingested_count ' \
            'FROM item ' \
            'group by dom_name ' \
            ' having count(dom_name) > 1 ' \
            'order by ingested_count desc'
        cursor = None
        multiple_ingest = {}
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Log.get_logger('qa.views').info(multiple_ingest_count=len(rows))

            for row in rows:
                multiple_ingest[row[0]] = row[1]
        except Exception as e:
            Log.get_logger('qa.views').error(e)
        finally:
            cursor.close()
            return multiple_ingest

    def _get_data_using_sql(self, items_with_multiple_ingest):  # TODO refactor - same code in releave_view!
        sql = 'SELECT item.id, item.date, m_codes.mcode, item.dom_name, ' \
            'approval.approved, approval.notes, ' \
            'approval.when, auth_user.username ' \
            'FROM ' \
                'item_status JOIN m_codes RIGHT OUTER JOIN item ON m_codes.psmid = item.dom_name ON item_status.item_id = item.id ' \
                'LEFT OUTER JOIN approval ON item.id = approval.item_id LEFT OUTER JOIN auth_user ON approval.who_id = auth_user.id ' \
            'WHERE (item_status.status = 300 AND item.is_live = TRUE) AND ' \
                '(approval.id = (SELECT MAX(approval.id) FROM approval WHERE approval.item_id = item.id) OR approval.id IS NULL)' \
            'ORDER BY item.date DESC'

        items_and_mcodes = []

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Log.get_logger('qa.views').info(rows_count=len(rows))

            for row in rows:
                sql_item = Item(id=row[0])
                sql_item.date = row[1]

                hard_coded_mcode = HardCodedMCodes.mcode_from_psmid(row[3][:12])
                if hard_coded_mcode is not None:
                    sql_item.mcode = hard_coded_mcode
                elif row[2] is None:
                    sql_item.mcode = ''
                else:
                    sql_item.mcode = row[2]

                sql_item.dom_id = row[3]
                sql_item.dom_name = row[3]
                sql_item.with_approval = row[4]

                if row[5] is None:
                    sql_item.notes = ''
                else:
                    sql_item.notes = row[5]

                if row[6] is None:
                    sql_item.when = datetime.strptime('Jan 1 1970', '%b %d %Y')  # allow sorting on field
                    sql_item.show_when = False  # problem with getting django template to evaluate when successfully
                else:
                    sql_item.when = row[6]
                    sql_item.show_when = True

                if row[7] is None:
                    sql_item.who = ''
                else:
                    sql_item.who = row[7]

                if sql_item.dom_name in items_with_multiple_ingest.keys():
                    sql_item.ingest_count = items_with_multiple_ingest[sql_item.dom_name]
                else:
                    sql_item.ingest_count = 1

                items_and_mcodes.append(sql_item)

            # Log.get_logger('qa.views').info(items_and_mcodes_count=len(items_and_mcodes))
            return items_and_mcodes
        except Exception as e:
            Log.get_logger('qa.views').error(e)
        finally:
            cursor.close()

    def get_data(self):
        items_with_multiple_ingest = self._get_ingest_count_using_sql()
        return self._get_data_using_sql(items_with_multiple_ingest)
        #return self._get_data_using_model()

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['queryset'] = self.data
        context['filter_types'] = self.get_filter_list(self.data, self.filter_field)

        context['msg'] = self.msg
        context['error'] = self.error

        sort_list = list(zip(self.sort_name_list, self.sort_fields_list))  # have it as a list of tuples, so column headers can be ordered how we want!
        context['sort_fields_list'] = sort_list

        if self.date_filter_field:
            context['date_filter_name_list'] = self.date_filter_name_list
        return context

    def post(self, request, *args, **kwargs):
        request_post = request.POST

        if 'save' in request_post:
            self._save(request_post)

        return super(ItemListView, self).get(RequestContext(request, {}), *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request_get = request.GET

        response = super(ItemListView, self).get(RequestContext(request, {}), *args, **kwargs)

        if 'csv_search_by' in request_get:
            return self._create_csv()
        else:
            return response

    def _create_csv(self, ):
        csv_response = HttpResponse(mimetype='text/csv')

        fname = "qa_items.csv"
        csv_response['Content-Disposition'] = 'attachment; filename=%s' % fname

        # EG-467
        csv_response['Pragma'] = 'public'
        csv_response['Expires'] = '0'
        csv_response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
        csv_response['Cache-Control'] = 'private'
        csv_response['Content-Type'] = 'application/octet-stream'
        csv_response['Content-Transfer-Encoding'] = 'binary'

        writer = csv.writer(csv_response, delimiter="|")
        writer.writerow(['ingested', 'ingest_count', 'mcode', 'complete', 'psmid', 'approved', 'notes', 'who', 'when'])
        for item in self.data:
            if item.when == datetime.strptime('Jan 1 1970', '%b %d %Y'):
                item.when = ''
            if item.with_approval == False:
                item.with_approval = ''
            writer.writerow([item.date, item.ingest_count, item.mcode, item.is_fully_linked(), item.dom_name, item.with_approval, item.notes, item.who, item.when])

        return csv_response

    def _save(self, request_post):
        user = User.objects.get(username__exact=self.request.user)
        approved_checkboxes = request_post.getlist('approved')

        something_was_saved = False
        for item_id in request_post.getlist('id'):
            notes = request_post.get('notes-%s' % item_id)

            if approved_checkboxes is not None and item_id in approved_checkboxes:
                approved = True
            else:
                approved = False

            # only save if values are different or its new & there's something to save
            try:
                current_approval = Approval.objects.filter(item_id=item_id).order_by('-id')[0]
                if current_approval.approved != approved or current_approval.notes != notes:
                    approval = Approval(item_id=item_id, approved=approved, notes=notes, who_id=user.id)
                    approval.save()
                    something_was_saved = True
            except (ObjectDoesNotExist, IndexError):
                if approved == True or len(notes) > 0:
                    approval = Approval(item_id=item_id, approved=approved, notes=notes, who_id=user.id)
                    approval.save()
                    something_was_saved = True

        if something_was_saved == True:
            self.msg = 'saved'
        else:
            self.error = 'please make a change to either &apos;approved&apos; or &apos;notes&apos;'


@login_required
@permission_required('qa.can_qa')
def detail(request, item_id):

    item_index = get_object_or_404(Item, pk=item_id)

    if not request.user.is_superuser:
        item_index.track(request.user.username)

    document = get_object_or_404(Document, item=item_id)

    ordered_final_asset_ids = _ordered_final_asset_id(document)
    etoc_info = _etoc_info(document, ordered_final_asset_ids)

    # order the articles by sequence.
    # Note: We use the *integer* version of the dom_id (string) to ensure numeric (not alpha) ordering.
    # so instead of 1,10,11,12,2 we get 1,2,10,11,12.
    text_chunks_index = sorted(Chunk.objects.filter(document=document.id, is_binary=False), key=lambda chunk: int(chunk.dom_id))

    # we need some sort of index, so etoc can link against it!!!
    new_text_chunks_index = []
    for i in range(1, len(text_chunks_index) + 1):
        chunk = text_chunks_index[i - 1]
        setattr(chunk, 'etoc_article_id', i)
        setattr(chunk, 'final_id', ordered_final_asset_ids[i - 1])
        new_text_chunks_index.append(chunk)

    binary_chunks_index = Chunk.objects.filter(document=document.id, is_binary=True)

    binary_chunk_map = {}
    for chunk in text_chunks_index:
        for bin_chunk in binary_chunks_index:
            bin_page = bin_chunk.pages.all()[0]  # Note: binary chunks only ever exist on one page
            if bin_page in chunk.pages.all():
                if binary_chunk_map.has_key(chunk.id):
                    binary_chunk_map[chunk.id].append((bin_chunk.dom_name, bin_page.id))
                else:
                    binary_chunk_map[chunk.id] = [(bin_chunk.dom_name, bin_page.id), ]

    config = get_config(settings.CONFIG_NAME)
    web_box = WebBox(config)

    page_ids_with_articles = []
    page_img_map = {}

    for chunk in text_chunks_index:
        chunk_pages = chunk.pages.all()
        page_ids_with_articles.extend([page.id for page in chunk_pages])

        for page in chunk_pages:
            page_info = json.loads(web_box.page_info(item_index.dom_name, item_id, page.dom_id))
            page_img_map[str(chunk.id) + str(page.dom_id)] = page_info['_thumb_url']

    pages_without_articles = []
    all_item_pages = Page.objects.filter(document=document.id)
    page_ids_without_articles = set([page.id for page in all_item_pages]) - set(page_ids_with_articles)  # note that we're ignorig binary chunks intentionally here.

    for page_id in page_ids_without_articles:
        page = Page.objects.get(pk=page_id)
        pages_without_articles.append(page)
        page_img_map['noarticle' + str(page.dom_id)] = page_info['_thumb_url']

    # Note: The web box retains one view of links for backwards compatability,
    # but there are really now 2 types of link
    asset_links = AssetLink.objects.filter(document=document)
    document_links = DocumentLink.objects.filter(document=document)
    #links_info = []
    #for link in link_indexes:
        #link_info = web_box.link_info(item_index.dom_name, item_index.id, link.dom_id) # this is a JSON string
        #links_info.append((link.id, link.dom_name, link_info))

    warning = ''
    if not item_index.is_fully_linked():
        warning = 'WARNING! this item has links to other documents/articles/pages that are not yet in Gaia (or may be wrong)! (<a href="#document_links">document links</a>)!'

    args = {'item': item_index,
            'page_img_map': page_img_map,
            'text_chunks': new_text_chunks_index,
            'binary_chunk_map': binary_chunk_map,
            'pages_without_articles': pages_without_articles,
            'asset_links': asset_links,
            'document_links': document_links,
            'warning': warning,
            'etoc_info': etoc_info,
            }
    return render_to_response('qa/item.html', args, context_instance=RequestContext(request))


def _ordered_final_asset_id(document):
    if document.dom_name[:8] in ['cho_meet', 'cho_chbp', 'cho_chrx', 'cho_rpax']:  # single retrievable items
        return [document.get_final_id()]
    else:
        """ order so that matches CHOA-1074 """
        chunks = Chunk.objects.filter(document=document.id)
        chunk_dom_ids = []
        for chunk in chunks:
            chunk_dom_ids.append(chunk.dom_id)
        ordered_chunk_dom_ids = sorted(chunk_dom_ids)

        ordered_final_asset_ids = []
        for ordered_chunk_dom_id in ordered_chunk_dom_ids:
            for chunk in chunks:
                if chunk.dom_id == ordered_chunk_dom_id:
                    ordered_final_asset_ids.append(chunk.get_final_id())
                    break

    return ordered_final_asset_ids


def _etoc_info(document, ordered_final_asset_ids):
    config = get_config(settings.CONFIG_NAME)
    outbox = Outbox(config.outbox)

    item_name = document.item.dom_name
    assets = outbox.assets(item_name)

    item = DomItem(item_name, item_name, assets, config)
    return item.etoc_info(ordered_final_asset_ids)
