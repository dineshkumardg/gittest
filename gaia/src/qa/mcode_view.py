import re
import copy
from collections import OrderedDict
from gaia.log.log import Log
from qa.models import MCodes
from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext


@class_view_decorator(permission_required('qa.can_manage'))
class MCodeView(FilteredCommonView):  # TODO use django forms.Form
    log = Log.get_logger('qa.views')
    template_name = 'qa/mcode.html'

    search_field = ['psmid', 'mcode', 'publication_title']
    sort_fields_list = ['psmid', 'mcode', 'publication_title']
    sort_name_list = ['psmid', 'mcode', 'publication title']

    psmid_pattern = 'cho_[a-z]{4}_([0-9-]+|[0-9-]+[a-zA-Z])_(\d{4}|\d{4}[a-z]|[a-zA-Z]+)_\d{3}_\d{4}'
    MSG_ROW_ADDED = 'row added'
    MSG_ROWS_DELETED = 'row(s) deleted'
    MSG_ROWS_NOT_SELECTED = 'no row(s) selected'
    MSG_ALL_FIELDS_ARE_BLANK = 'all fields are blank'
    MSG_PSMID_MUST_PASS_REGEX = 'psmid must match regex, unless its blank'
    MSG_PSMDS_MUST_PASS_REGEX = 'psmid(s) must match regex, unless blank'
    MSG_PSMID_NOT_UNIQUE = 'psmid must be unique, unless blank'
    MSG_PSMIDS_NOT_UNIQUE = 'psimd(s) must be unique, unless blank'
    MSG_CHANGES_APPLIED = 'change(s) applied, excluding blank rows'

    def get_data(self):
        return MCodes.objects.order_by('psmid', 'mcode', 'publication_title')

    def get_context_data(self, **kwargs):
        context = super(MCodeView, self).get_context_data(**kwargs)
        context['queryset'] = self.data
        context['filter_types'] = self.get_filter_list(self.get_data(), self.filter_field)
        context['msg'] = self.msg
        context['error'] = self.error

        sort_dict = OrderedDict(zip(self.sort_name_list, self.sort_fields_list))

        context['sort_fields_list'] = sort_dict

        if self.date_filter_field:
            context['date_filter_name_list'] = self.date_filter_name_list
        return context

    def post(self, request, *args, **kwargs):
        request_post = request.POST
        self.msg = ''
        self.error = ''

        if 'delete_item' in request_post:
            self._delete_item(request_post)
        elif 'add_item' in request_post:
            self._add_item(request_post)
        elif 'apply_changes' in request_post:
            self._apply_changes(request_post)

        return self.get(RequestContext(request, {}), *args, **kwargs)

    def _psmid_pass_regex(self, psmids):
        psmid_list_clone = [value for value in copy.copy(psmids) if value != u'']
        for psmid in psmid_list_clone:
            if re.match(self.psmid_pattern, psmid) is None:
                return False
        return True

    def _psmids_unique(self, psmids):
        psmid_list_clone = [value for value in copy.copy(psmids) if value != u'']
        if len(psmid_list_clone) != len(set(psmid_list_clone)):
            return False
        return True

    def _delete_item(self, request_post):
        delete_items = request_post.getlist('delete_selected')

        if len(delete_items) > 0:
            for delete_item in delete_items:
                delete_item = MCodes.objects.filter(id=delete_item)
                self.log.info('delete_item', user=self.request.user, delete_item=delete_item)
                delete_item.delete()
                self.msg = self.MSG_ROWS_DELETED
        else:
            self.error = self.MSG_ROWS_NOT_SELECTED
            self.log.warn(self.error)

    def _add_item(self, request_post):
        psmid = request_post.get('add_psmid')
        mcode = request_post.get('add_mcode')
        publication_title = request_post.get('add_publication_title')

        # strip whitespace for SH
        psmid = psmid.strip()
        mcode = mcode.strip()

        if psmid == u'' and mcode == u'' and publication_title == u'':
            self.error = self.MSG_ALL_FIELDS_ARE_BLANK
            self.log.warn(self.error)
            return

        if psmid != u'' and self._psmid_pass_regex([psmid]) == False:
            self.error = self.MSG_PSMID_MUST_PASS_REGEX
            self.log.warn(self.error)
            return

        if psmid != u'' and MCodes.psmid_present([psmid]) == True:
            self.error = self.MSG_PSMID_NOT_UNIQUE
            self.log.warn(self.error)
            return

        mcode_entry = MCodes(psmid=psmid, mcode=mcode, publication_title=publication_title)
        mcode_entry.save()

        self.log.info('add_item', user=self.request.user, mcode=mcode)
        self.msg = self.MSG_ROW_ADDED

    def _apply_changes(self, request_post):
        primary_id = request_post.getlist('id')
        psmid = request_post.getlist('psmid')
        mcode = request_post.getlist('mcode')
        publication_title = request_post.getlist('publication_title')

        if self._psmid_pass_regex(psmid) == False:
            self.error = self.MSG_PSMDS_MUST_PASS_REGEX
            self.log.warn(self.error)
            return

        if self._psmids_unique(psmid) == False:
            self.error = self.MSG_PSMIDS_NOT_UNIQUE
            self.log.warn(self.error)
            return

        for index, value in enumerate(primary_id):
            current_psmid = psmid[index]
            current_mcode = mcode[index]
            current_publication_title = publication_title[index]

            if len(current_psmid) > 0 or len(current_mcode) > 0 or len(current_publication_title) > 0:
                update_item = MCodes.objects.get(id=value)
                update_item.psmid = current_psmid
                update_item.mcode = current_mcode
                update_item.publication_title = current_publication_title
                update_item.save()

                self.log.info('_apply_changes', user=self.request.user, psmid=current_psmid, mcode=current_mcode, publication_title=current_publication_title)

        self.msg = self.MSG_CHANGES_APPLIED
