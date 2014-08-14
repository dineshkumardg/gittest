import django.core.urlresolvers
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext
from django.conf import settings
from gaia.utils.sliding_window import SlidingWindow
from gaia.config.config import get_config
from gaia.web.web_box import WebBox
from qa.models import Page, AssetLink, DocumentLink, RejectReason
from qa.reject.reject_form import RejectForm
from qa.fix.fix_form import FixForm
from qa.fix.fix_view import fix


@login_required
@permission_required('qa.can_qa')
def detail(request, page_id):
    fix_form = FixForm()
    page = get_object_or_404(Page, pk=page_id)
    pages = Page.objects.filter(document=page.document)
    pages = sorted(pages, cmp=lambda x, y: cmp(int(x.dom_id), int(y.dom_id)))  # Note: dom_id is a string, but we want to make sure we sort in numerical order.

    window = SlidingWindow(pages)  # Note: we use this instead of the django "Paginator" (which is a pain to use!)
    prev_page, next_page, page_window, pager_start_i = window.view(page)
    pages = page_window

    if not request.user.is_superuser:
        page.track(request.user.username)

    config = get_config(settings.CONFIG_NAME)
    item_index = page.document.item

    web_box = WebBox(config)
    page_info = web_box.page_info(item_index.dom_name, item_index.id, page.dom_id)  # this is a JSON string
    doc_info = web_box.doc_info(item_index.dom_name, item_index.id, page.document.dom_id)  # this is a JSON string
    fix_form.add_page_info(page_info)

    chunks_info = []
    chunks = page.chunk_set.all()
    for chunk in chunks:
        chunk_info = web_box.chunk_info(item_index.dom_name, item_index.id, chunk.dom_id)  # this is a JSON string
        chunks_info.append((chunk.id, chunk.dom_name, chunk_info))
        fix_form.add_chunk_info(chunk_info)

    fix_form.add_doc_info(doc_info)  # Note: the order of adding info *is* important, hence this is last.

    # Note: The web box retains one view of links for backwards compatability,
    # but there are really now 2 types of link
    link_indexes = AssetLink.objects.filter(document=page.document)

    asset_links_info = []
    for link in link_indexes:
        link_info = web_box.link_info(item_index.dom_name, item_index.id, link.dom_id)  # this is a JSON string
        asset_links_info.append((link.id, link.dom_name, link_info))

    link_indexes = DocumentLink.objects.filter(document=page.document)

    document_links_info = []
    for link in link_indexes:
        link_info = web_box.link_info(item_index.dom_name, item_index.id, link.dom_id)  # this is a JSON string
        document_links_info.append((link.id, link.dom_name, link_info))

    # WARNING: The reject from is a normal django form, the fix form is NOT!
    reject_form = RejectForm()

    url = django.core.urlresolvers.reverse(fix, kwargs={'item_id': item_index.id, 'page_id': page_id})
    fix_form_html = fix_form.form(url) # use the whole prepared html for the form

    try:
        reject_reason = RejectReason.objects.filter(item_id__exact=item_index.id).order_by('-when')  # only show most recent
        reject_reason_value = ''
        if len(reject_reason) > 0:
            reject_reason_value = reject_reason[0].reason
    except RejectReason.DoesNotExist:
        pass
    reject_form = RejectForm({'reason': reject_reason_value})  # WARNING: The reject form is a normal django form, the fix form is NOT!

    args = {'page': page,
            'pages': pages,
            'prev_page': prev_page,
            'next_page': next_page,
            'pager_start_i': pager_start_i,
            'page_info': page_info,
            'item_index': item_index,
            'reject_form': reject_form,
            'fix_form_html': fix_form_html,
            'reject_form': reject_form,
            'STATIC_URL': settings.STATIC_URL}  # note: this is always required for gaia.css: should probably push into django middleware TODO

    return render_to_response('qa/page.html', args, context_instance=RequestContext(request))
