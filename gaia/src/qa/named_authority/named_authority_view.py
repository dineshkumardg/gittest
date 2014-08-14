import csv
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from gaia.config.config import get_config
from gaia.log.log import Log
from gaia.egest.outbox import Outbox
from gaia.asset.asset import Asset
from gaia.dom.model.named_authority_item import NamedAuthorityItem
from qa.models import Item, Approval
# from qa.models import Item, ItemStatus


#class NamedAuthorityForm(forms.Form):
#    asset_id = forms.CharField(max_length=25)
#    content_type = forms.ChoiceField(choices=content_types)
#    datepicker_from = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker_from'}))  # hooks into jquery datepicker :-)
#    datepicker_to = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker_to'}))


@login_required
@permission_required('qa.can_qa')
def post(request):
    query_dict = request.POST
    Log.get_logger('qa.views').info('post', query_dict)

    #form = NamedAuthorityForm(query_dict)
    #if form.is_valid():
    #    print form.cleaned_data['asset_id']

    args = {}

    config = get_config(settings.CONFIG_NAME)
    outbox = Outbox(config.outbox)

    if 'seach_asset_id' in query_dict:
        args = _article_assetid_or_psmid(config, outbox, query_dict)
    elif 'produce_report' in query_dict:
        args = _date_ingested_from_to(config, outbox, query_dict)

    #args['form'] = form

    return render_to_response('qa/named_authority.html', args, context_instance=RequestContext(request))


def _article_assetid_or_psmid(config, outbox, query_dict):
    args = {}

    psmid_or_asset_id = query_dict['asset_id'].strip()
    args['asset_id'] = psmid_or_asset_id

    if len(psmid_or_asset_id) == 0:
        args['error'] = 'please provide an asset id'
    else:
        # search by psmid first, assetid second

        # use cursor - instead of return [Item.objects.filter(dom_name=psmid, is_live=True)] - due to a FieldError: Join on field 'dom_name' not permitted.
        items = _search_by_psmid_or_asset_id("SELECT dom_name FROM item WHERE is_live = True AND dom_name LIKE %s",
                                 psmid_or_asset_id)

        if items is None:
            # might be a document
            items = _search_by_psmid_or_asset_id("SELECT distinct document.dom_name, document.dom_id FROM public.document, public.document_final_id WHERE document_final_id.document_id = document.id AND document_final_id.final_id LIKE %s",
                                        psmid_or_asset_id)

        if items is None:
            # might be a chunk
            items = _search_by_psmid_or_asset_id("SELECT document.dom_name FROM chunk, chunk_final_id, document WHERE chunk.document_id = document.id AND chunk_final_id.chunk_id = chunk.id AND chunk_final_id.final_id LIKE %s",
                                        psmid_or_asset_id)

        if items is None:
            args['error'] = '0 records found: %s' % psmid_or_asset_id
        else:
            args['msg'] = '%s: %s' % (len(items), psmid_or_asset_id)
            args['results'] = _get_results(items, config, outbox)

    return args


def _search_by_psmid_or_asset_id(sql, psmid_or_asset_id):
    cursor = None
    try:
        cursor = connection.cursor()
        psmid_sql = "%" + psmid_or_asset_id.replace("%", "%%") + "%"
        cursor.execute(sql, (psmid_sql, ))
        rows = cursor.fetchall()

        items_with_asset_id = []
        for row in rows:
            items_with_asset_id.append(row[0])

        if len(items_with_asset_id) > 0:
#             return Item.objects.filter(dom_name__in=items_with_asset_id, is_live=True).exclude(itemstatus__status=ItemStatus.REJECTED).order_by('dom_name')

            return Item.objects.filter(dom_name__in=items_with_asset_id, is_live=True).order_by('dom_name')
        else:
            return None
    finally:
        cursor.close()


def _date_ingested_from_to(config, outbox, query_dict):
    args = {}

    datepicker_from = query_dict['datepicker_from']
    datepicker_to = query_dict['datepicker_to']

    args['datepicker_from'] = datepicker_from
    args['datepicker_to'] = datepicker_to

    if len(datepicker_from) == 0:
        args['error'] = "please select a 'from' date"
    elif len(datepicker_to) == 0:
        args['error'] = "please select a 'to' date"
    else:
        start_date = datepicker_from.split('/')
        end_date = datepicker_to.split('/')

#         items = Item.objects.filter(date__range=('%s-%s-%s 00:00:00.00000' % (start_date[2], start_date[1], start_date[0]),
#                                      '%s-%s-%s 23:59:59.99999' % (end_date[2], end_date[1], end_date[0])),
#                                     is_live=True).exclude(itemstatus__status=ItemStatus.REJECTED).order_by('dom_name', 'id')

        items_within_date = Item.objects.filter(date__range=('%s-%s-%s 00:00:00.00000' % (start_date[2], start_date[1], start_date[0]),
                                                 '%s-%s-%s 23:59:59.99999' % (end_date[2], end_date[1], end_date[0])), is_live=True).order_by('dom_name', 'id')

        # for each item only shows those that have have been approved - EG-475
        items = []
        for item_with_date in items_within_date:
            approval = Approval.objects.filter(item_id=item_with_date.id).order_by('-when')
            if len(approval) >= 1:
                if approval[0].approved == True:
                    items.append(item_with_date)

        if len(items) == 0:
            args['error'] = '0 records found: %s..%s (inclusive)' % (datepicker_from, datepicker_to)
        else:
            args['msg'] = '%s: %s..%s (inclusive)' % (len(items), datepicker_from, datepicker_to)
            args['results'] = _get_results(items, config, outbox)

    return args


def _get_results(items, config, outbox):
    results = []
    for item in items:
        if item.dom_name[:8] in ['cho_meet', 'cho_chbp', 'cho_chrx', 'cho_rpax']:  # single retrievable items
            # we actually use the document asset id, not that of the article
            document = item.document()
            chunks = None
        else:
            document = None
            chunks = item.chunks()

        assets = [Asset('%s/%s/%s.xml' % (outbox._root_dir, item.dom_name, item.dom_name), 'r')]  # only care about the xml assert

        named_authority_item = NamedAuthorityItem(item.id, item.dom_name, assets, config, chunks=chunks, document=document, date=item.date, is_live=item.is_live)
        results.append(named_authority_item.named_authority_details())

    return results


def create_csv(request):
    config = get_config(settings.CONFIG_NAME)
    outbox = Outbox(config.outbox)

    asset_id = request.GET['asset_id']
    datepicker_from = request.GET['datepicker_from']

    datepicker_to = request.GET['datepicker_to']

    response = HttpResponse(mimetype='text/csv')

    if len(asset_id) > 0:
        args = _article_assetid_or_psmid(config, outbox, request.GET)
        fname = "named_authority-%s.csv" % asset_id
        response['Content-Disposition'] = 'attachment; filename=%s' % fname

        # EG-467
        response['Pragma'] = 'public'
        response['Expires'] = '0'
        response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
        response['Cache-Control'] = 'private'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Transfer-Encoding'] = 'binary'

    else:
        datepicker_from_split = datepicker_from.split('/')
        from_year = datepicker_from_split[2]
        from_month = datepicker_from_split[1]
        from_day = datepicker_from_split[0]

        datepicker_to_split = datepicker_to.split('/')
        to_year = datepicker_to_split[2]
        to_month = datepicker_to_split[1]
        to_day = datepicker_to_split[0]

        date_from = '%s%s%s' % (from_year, from_month, from_day)
        date_to = '%s%s%s' % (to_year, to_month, to_day)
        args = _date_ingested_from_to(config, outbox, request.GET)
        fname = "named_authority-%s_%s.csv" % (date_from, date_to)
        response['Content-Disposition'] = 'attachment; filename=%s' % fname

        # EG-467
        response['Pragma'] = 'public'
        response['Expires'] = '0'
        response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
        response['Cache-Control'] = 'private'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Transfer-Encoding'] = 'binary'

    writer = csv.writer(response, delimiter="|")
    writer.writerow(['psmid', 'article_id', 'gift_article_title', 'gift_author', 'asset_id', 'ingest_date', 'atlas_uid', 'pna_notes'])
    for result in args['results']:
        for row in result:
            writer.writerow([row['psmid'], row['article_id'], row['gift_article_title'].encode('utf-8'), row['gift_author'].encode('utf-8'), row['asset_id'], row['ingest_date'], ' ', ' '])

    return response
