from datetime import datetime
from gaia.log.log import Log
from qa.models import Item, MCodes, Approval
from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from django.db import connection
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from qa.manage.m2_cho_meet_psmids import m2_cho_meet_psmids


@class_view_decorator(permission_required('qa.can_manage'))
class ReleaseView(FilteredCommonView):  # TODO stop using POST and use form.Form? AND rewrite Tushar's entire django framework
    template_name = "qa/manage/release.html"
    paginate_by = 99999  # so many as we don't have a grouping feature

    search_field = ['dom_id']
    sort_fields_list = ['date', 'dom_id', 'release', 'with_approval', 'notes', 'who', 'when']
    sort_name_list = ['ingested', 'psmid', 'release', 'approved', 'notes (40 chars. visible; max. 250 chars.)', 'who', 'when']

    def _get_data_using_model(self):
        all_items_in_qa = Item.in_qa()  # includes those that are not fully linked and do not have an mcode :-(

        releasable_items = []
        for item in all_items_in_qa:
            mcode = MCodes.get_mcodes([item.dom_id])

            if item.is_live == True and len(mcode) > 0 and item.is_fully_linked():  # very slow and inefficient query!
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

                releasable_items.append(item)

        self._data = releasable_items

    def _get_data_using_sql(self):  # TODO refactor - same code in item_views
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

            Log.get_logger('qa.views').info(rows_count=len(rows))

            for row in rows:
                if row[3][:8] in ['cho_meet', 'cho_chrx', 'cho_chbp', 'cho_rpax', 'cho_chdp']:
                    pass
                elif row[2] is None or len(row[2]) == 0:
                    continue  # skip iteration - we can only release things with an mcode

                sql_item = Item(id=row[0])

                # TODO try and improve performance of is_fully_linked
                if sql_item.is_fully_linked() == False:
                    continue  # skip iteration - we can only release things that are fully_linked

                sql_item.date = row[1]

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

                items_and_mcodes.append(sql_item)

        except Exception as e:
            Log.get_logger('qa.views').error(e)
        finally:
            cursor.close()
            Log.get_logger('qa.views').info(items_and_mcodes_count=len(items_and_mcodes))
            self._data = items_and_mcodes

    def get_data(self):
        return self._get_data_using_sql()
        #return self._get_data_using_model()  # example that using the ORM layer - in how its designed - is significantly slower the pure sql

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['queryset'] = self.data
        context['filter_types'] = self.get_filter_list(self._data, self.filter_field)

        context['msg'] = self.msg
        context['error'] = self.error

        sort_dict = list(zip(self.sort_name_list, self.sort_fields_list))  # not a dict :-)
        context['sort_fields_list'] = sort_dict

        if self.date_filter_field:
            context['date_filter_name_list'] = self.date_filter_name_list
        return context

    def get_queryset(self):
        self.get_data()
        self.data = self._before_filter_sort_search(self._data)

        # implement filter mixin
        if self.filter_field or self.date_filter_field:
            filter_by = self.request.GET.get(self.filter_url_name)
            self.data = self.get_queryset_filters(self.data, filter_by, self.filter_field)

        # implement search mixin
        if self.search_field:
            search_by = self.request.GET.get(self.search_url_name)
            self.data = self.get_queryset_search(self.data, search_by, self.search_field)

        # implement sort mixin
        if self.sort_fields_list:
            sort_by = self.request.GET.get(self.sort_url_name)
            self.data = self.get_queryset_sort(self.data, sort_by)
            # update sort fields (function to control sort url)
            self.sort_fields_list = self.update_sort_fields(sort_by, self.sort_fields_list)

        self.data = self._after_filter_sort_search(self.data)
        return self.data


    def _release_m2_cho_meet(self, m2_cho_meet, release_only_callisto, release_only_xml, items_to_release):
        if m2_cho_meet is not None:
            items_to_release.extend(self._get_m2_cho_meet())
        if len(items_to_release) > 0:
            self._release(items_to_release, release_only_callisto, release_only_xml)
        else:
            self.error = 'unable to release anything'

    def post(self, request, *args, **kwargs):  # TODO replace with a form.Form
        request_post = request.POST
        self.msg = ''
        self.error = ''

        items_selected_for_release_on_page = request_post.getlist('selected')

        select_all = request_post.get('select_all')
        m2_cho_meet = request_post.get('release_only_meet_m2')
        release_only_callisto = request_post.get('release_only_callisto')
        release_only_xml = request_post.get('release_only_xml')

        if len(items_selected_for_release_on_page) == 0 and (select_all is None and m2_cho_meet is None):
            self.error = 'please tick release or M2 cho_meet'
        elif release_only_callisto is None and release_only_xml is None:
            self.error = 'please tick callisto and / or xml '
        else:
            if select_all is not None:
                items_to_release = self.get_queryset()

                self._release_m2_cho_meet(m2_cho_meet, release_only_callisto, release_only_xml, items_to_release)
            else:
                items_to_release = []
                for pk in items_selected_for_release_on_page:
                    items_to_release.append(Item.objects.get(pk=pk))

                self._release_m2_cho_meet(m2_cho_meet, release_only_callisto, release_only_xml, items_to_release)

        # possible multi-page issue... its possible that, effectively the data behind the page has been removed from the query!
        get_query_dict = request.GET.copy()
        if get_query_dict.get(u'page'):
            get_query_dict.pop(u'page')
        get_query_dict.update({u'page': u'1'})
        request.GET = get_query_dict

        return self.get(RequestContext(request, {}), *args, **kwargs)

    def _get_m2_cho_meet_psmids(self):
        return m2_cho_meet_psmids

    def _get_m2_cho_meet(self):
        m2_cho_meet_psmids = self._get_m2_cho_meet_psmids()

        gaia_items = []
        for psmid in m2_cho_meet_psmids:
            try:
                item = Item.objects.get(dom_id=psmid, is_live=True)
                gaia_items.append(item)
            except Item.DoesNotExist:
                pass

        return gaia_items

    def _get_release_type(self, release_only_callisto, release_only_xml):
        released_type = ''
        if release_only_callisto is not None and release_only_xml is not None:
            released_type = 'callisto + xml'
        elif release_only_callisto is not None:
            released_type = 'callisto'
        elif release_only_xml is not None:
            released_type = 'xml'
        return released_type

    def _release(self, items_to_release, release_only_callisto, release_only_xml):
        released_items_dom_name = ''
        released_count = 0
        for item in items_to_release:
            item_in_gaia = Item.objects.get(pk=item.id)
            if item_in_gaia.is_fully_linked():  # belt and braces
                released_items_dom_name += item_in_gaia.dom_name + '; '
                released_count += 1

                if release_only_callisto is not None and release_only_xml is not None:
                    item_in_gaia.ready_for_release()
                elif release_only_callisto is not None:
                    item.ready_for_release_only_callisto()
                elif release_only_xml is not None:
                    item.ready_for_release_only_xml()

        self.msg = 'released: %s; %s item(s): %s' % (self._get_release_type(release_only_callisto, release_only_xml),
                                                     released_count, released_items_dom_name.rstrip('; '))
