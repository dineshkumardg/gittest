from collections import OrderedDict
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext
from gaia.log.log import Log
from gaia.config.config import get_config
from gaia.search.query import Query
from qa.qa_link import QaLink
from qa.analyse.analyse_expert_form import AnalyseExpertForm
from qa.global_changes.global_changes_form import GlobalChangesForm
import collections
from django.http import HttpResponse
import csv


@login_required
@permission_required('qa.can_manage')   # For Qa Managers only
def expert(request):
    ' A full-featured, less user-friendly front end to Analysis queries. '

    config = get_config(settings.CONFIG_NAME)
    #Log.configure_logging('qa_web_server', config)  #?
    log = Log.get_logger('qa.views')    #?
    log.enter(request=request)

    args = {}

    if request.method == 'GET':
        expert_query = request.GET.get('expert_query')
        if expert_query is not None:
            expert_query = expert_query.rstrip()
        expert_query_form = AnalyseExpertForm({'expert_query': expert_query})

        args.update({'expert_query': expert_query,
                     'num_found': 0, })

        if expert_query_form.is_valid() and expert_query is not None:
            if expert_query:
                gaia_query = expert_query
                if expert_query and 'fl' in expert_query:
                    # note it's okay to have multiple fl clauses
                    # The id is currently used as the name for the link (TODO: review)
                    # The QaLink.field_name is used by QaLink.link_info()
                    gaia_query += '&fl=id,' + QaLink.field_name

                matches, num_found = Query(config.search_server, search_collection=config.project_code).find(gaia_query)
            else:
                matches, num_found = [], 0

            # TODO also see why Items care not displayed but the search results are.
            show_matches = []
            for match in matches:
                url, item_index_id, chunk_index_id, page_index_id = QaLink.link_info(match)
                match['GAIA_URL'] = url

                #This shoudl no longer be required...
                #item = Item.objects.get(id=item_index_id)
                #`if not item.is_live:  # TODO: review and clean up (maybe remove things from the search index when superceded)?
                  #  continue # ignore this non-live match

                for key in match.keys():
                    if key.startswith('_') or key.startswith('doc__'):
                        del match[key]   # remove internal fields from display
    
                match = OrderedDict(sorted(match.items(), key=lambda t: t[0]))  # order the entries by key for display
                show_matches.append(match)
    
            args.update({'num_found': num_found,
                         'matches': show_matches, })
    
            if num_found is not 0:
                global_changes_form = GlobalChangesForm()
                args.update({'global_changes_form': global_changes_form})
        else:
            args.update({'num_found': 0,})

        args.update({'expert_query_form': expert_query_form,})

    log.exit()
    return render_to_response('qa/analyse_expert.html', args, context_instance=RequestContext(request))

def _get_matches(request):
    config = get_config(settings.CONFIG_NAME)
    expert_query = request.GET.get('csv_expert_query')
    if '&fl' in expert_query and '&fl=doc_PSMID' not in expert_query:
        expert_query += '&fl=doc_PSMID'
    matches, num_found = Query(config.search_server, search_collection=config.project_code).find(expert_query)
    return matches

def create_csv(request):
    matches = _get_matches(request)
    header_columns = _get_csv_header_columns(matches)

    response = HttpResponse(mimetype='text/csv')
    response['Pragma'] = 'public'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Cache-Control'] = 'private'
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Transfer-Encoding'] = 'binary'
    response['Content-Disposition'] = 'attachment; filename=expert_analysis.csv'

    writer = csv.writer(response, delimiter="\t")
    writer.writerow(header_columns)

    for match in matches:
        line = []
        for column in header_columns:
            try:
                try:
                    line.append('%s' % (match[column].encode('utf-8')))
                except AttributeError:
                    line.append('%s' % (match[column]))
            except KeyError:
                line.append('')
        writer.writerow(line)

    return response

def _get_csv_header_columns(matches):
    header_columns = []
    for match in matches:
        ordered_dict = collections.OrderedDict(sorted(match.items()))

        for key, val in ordered_dict.iteritems():
            if key not in header_columns and key not in ['GAIA_URL', 'id']:
                header_columns.append(key)

    return header_columns
