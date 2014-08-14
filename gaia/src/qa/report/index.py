from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from qa.models import Item, IngestError

@login_required
@permission_required('qa.can_qa')
def index(request):
    args = {}

    args['num_total_items']         = Item.objects.count()
    args['num_in_qa']               = Item.in_qa().count()
    args['num_ready_for_release']   = Item.in_ready_for_release().count() + Item.in_ready_for_release_only_xml().count() 
    args['num_exporting']           = Item.in_exporting().count()
    args['num_released']            = Item.in_released().count()
    args['num_rejected']            = Item.in_rejected().count()
    args['num_item_errors']         = Item.in_error().count()
    args['num_ingest_errors']       = IngestError.objects.all().count()

    return render_to_response('qa/report/reports.html', args, context_instance=RequestContext(request))
