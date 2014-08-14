from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext
from gaia.config.config import get_config
from gaia.web.web_box import WebBox
from qa.models import Item
from qa.fix.fix_form import FixForm

@permission_required('qa.can_qa')
def fix(request, item_id, page_id):
    msg = None
    changes = None
    form_data = None

    config = get_config(settings.CONFIG_NAME)
    item_index = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST': # If the form has been submitted...
        form_data = request.POST 
        web_box = WebBox(config)

        doc_info_changes, page_info_changes, chunk_info_changes = FixForm.parse(form_data.dict())
        web_box.change_item_info(item_index, doc_info_changes, page_info_changes, chunk_info_changes)

        changes = doc_info_changes
        changes.update(page_info_changes)
        changes.update(chunk_info_changes)

        # TODO sort the changes xpaths so look nice on the screen

    else:
        msg = 'UNEXPECTEDLY called this fix web page without form data!'

    args = {'changes': changes,
            'item': item_index,
            'msg': msg,
            'page_id': page_id} 
    return render_to_response('qa/fix.html', args, context_instance=RequestContext(request))
