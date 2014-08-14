from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext
from django.conf import settings
from qa.models import Item, RejectReason
from qa.reject.reject_form import RejectForm
from qa.reject.reject_report import RejectReport
from qa.ws.views import WSItem
from gaia.log.log import Log
from gaia.config.config import get_config
from lxml import etree
from gaia.utils.now import now
from gaia.utils.ftp import Ftp, FtpError
from gaia.utils.safe_unicode import safe_unicode


log = Log.get_logger('qa.views')


@permission_required('qa.can_qa')
def reject(request, item_id, page_id):
    error = ''
    args = {'page_id': page_id}

    if request.method == 'POST':
        form = RejectForm(request.POST)

        item = get_object_or_404(Item, pk=item_id)

        args.update({'item': item})

        if form.is_valid():
            reason = form.cleaned_data['reason']
            args.update({'reason': reason})

            log.info(item_id=item.id, reason=reason, who_id=request.user.id)

            reject_reason = RejectReason(item_id=item.id, reason=reason, who_id=request.user.id)
            reject_reason.save()

            if 'save' in request.POST:
                origin_button = 'save'
            else:
                origin_button = 'ftp'

                reject_reason = RejectReason.objects.filter(item_id__exact=item.id).order_by('-when')
                most_recent_reject_reason = safe_unicode(reject_reason[0].reason)

                reject_report_txt_filename = '%s_%s.txt' % (item.dom_name, now())
                reject_xml_filename = '%s_%s.xml' % (item.dom_name, now())

                reject_report = RejectReport(most_recent_reject_reason, item.id, item.dom_id, item.dom_name, request.user, page_id, reject_report_txt_filename, reject_xml_filename)
                reject_report_str = str(reject_report)

                ftp_success, ftp_msg = _ftp_report_to_content_provider(reject_report_txt_filename, reject_report_str, reject_xml_filename, _fixed_xml(item))

                if ftp_success == True:
                    log.info('successfully sent: %s .txt and .xml to content provider' % item.dom_name)

                    item.reject(reject_report)  # record it in the database

                    args.update({'reject_report_txt_filename': reject_report_txt_filename,
                                 'reject_report_contents': str(reject_report),
                                 'reject_xml_filename': reject_xml_filename})
                else:
                    # we haven't been abe tp ftp
                    ftp_failure = ftp_msg
                    log.warn(ftp_failure)
                    args.update({'ftp_failure': ftp_failure})

            args.update({'origin_page': form.cleaned_data['current_page'],
                        'origin_button': origin_button})
        else:
            error = form.invalid_reason
    else:
        error = 'UNEXPECTEDLY called this web page without form data!'

    args.update({'error': error})
    log.exit()

    return render_to_response('qa/reject.html', args, context_instance=RequestContext(request))


def _ftp_report_to_content_provider(reject_report_txt_filename, reject_report, reject_xml_filename, fixed_xml):
    config = get_config(settings.CONFIG_NAME)

    try:
        log.info(ftp_details=config.content_providers['htc'])

        ftp_client = Ftp(**config.content_providers['htc'])  # hard coded as gaia has no idea where an item originates from!!!
        ftp_client.open()

        fpath = '/%s/reports/reject' % config.project_code
        log.info(fpath=fpath)
        ftp_client.cd(fpath)

        ftp_client.write(reject_report_txt_filename, str(reject_report))
        ftp_client.write(reject_xml_filename, fixed_xml)

        return True, None
    except FtpError as e:
        log.warn(str(e))
        return False, str(e)
    except Exception as e:
        log.error(str(e))
        return False, str(e)
    finally:
        ftp_client.close()


def _fixed_xml(item):
    try:
        ws_item = WSItem()
        original_xml_tree, possible_fixes_json_dicts = ws_item.ingested_xml_and_fixes(item.id)
        return etree.tostring(ws_item.patch(original_xml_tree, possible_fixes_json_dicts))
    except Exception as e:
        log.error(str(e))
        raise e
