import urllib
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext
from gaia.log.log import Log
from gaia.config.config import get_config
from qa.qa_query import QaQuery
from qa.global_changes.global_changes_form import GlobalChangesForm
from qa.reject.reject_report import BulkRejectReport
from qa.analyse.analyse_expert_form import AnalyseExpertForm


@login_required
@permission_required('qa.can_qa')
def summary(request):
    log = Log.get_logger('qa.views')  # ?
    log.enter(request=request)

    args = {}
    error = ''  # no error, ie ok
    config = get_config(settings.CONFIG_NAME)

    if request.method == 'POST':
        reason_form = GlobalChangesForm(request.POST)
        expert_analysis_query = request.POST['expert_analysis_query']

        if reason_form.is_valid():
            reason = reason_form.cleaned_data['reason']

            search_expression, search_parameters = AnalyseExpertForm.split_query(expert_analysis_query)
            query = QaQuery(config.search_server, config.project_code)
            items = query.find_items(search_expression, search_parameters)

            log.info('BULK REJECTING: ' + str(items))

            for item in items:
                reject_report = BulkRejectReport(reason, item.id, item.dom_id, item.dom_name, request.user)
                item.reject(reject_report, err_type='GLOBAL_CHANGE')

            args = {'expert_analysis_query': expert_analysis_query,
                    'items': items,
                    'reason': reason}

        else: # form no good
            args.update({'expert_analysis_query': expert_analysis_query,
                         'encoded_expert_analysis_query': '?expert_query=%s' % urllib.quote_plus(expert_analysis_query)})
            error = reason_form.invalid_reason
    else: # GET, not POST
        error = 'UNEXPECTEDLY called this web page without form data!'

    args.update({'error': error})
    log.exit()
    return render_to_response('qa/global_changes.html', args, context_instance=RequestContext(request))
