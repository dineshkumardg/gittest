from qa.models import Item
from qa.view_decorator import class_view_decorator
from qa.manage.release_view import ReleaseView
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext
from qa.manage.m2_cho_meet_psmids import m2_cho_meet_psmids


@class_view_decorator(permission_required('qa.can_manage'))
class UnreleaseView(ReleaseView):
    template_name = "qa/manage/unrelease.html"

    sort_fields_list = ['date', 'dom_id']
    sort_name_list = ['ingested', 'psmid']


    def get_data(self):
        # Note: the following 2 states are very volatile, so we do NOT allow these items
        # that are "on their way to being released" to be "un-released"
        # (to do this, we'd have to be very careful to not interrupt any background processing that's going on).
        #ready_for_release_items = Item.in_ready_for_release()
        #exporting_items = Item.in_exporting()
        self._data = Item.in_released()

    def get_context_data(self, **kwargs):
        return super(UnreleaseView, self).get_context_data(**kwargs)

    def _get_m2_cho_meet_psmids(self):
        return m2_cho_meet_psmids

    def post(self, request, *args, **kwargs):
        request_post = request.POST
        self.msg = ''
        self.error = ''

        items_selected_for_unrelease_on_page = request_post.getlist('selected')
        select_all = request_post.get('select_all')
        m2_cho_meet = request_post.get('unrelease_only_meet_m2')

        if len(items_selected_for_unrelease_on_page) == 0 and m2_cho_meet is None:
            self.error = 'please tick un-release or M2 cho_meet'
        else:
            if select_all is not None:
                items_to_release = self.get_queryset()  # everything
                self._release(items_to_release, m2_cho_meet)
            else:
                items_to_release = []
                for pk in items_selected_for_unrelease_on_page:
                    items_to_release.append(Item.objects.get(pk=pk))

                self._release(items_to_release, m2_cho_meet)

        return self.get(RequestContext(request, {}), *args, **kwargs)

    def _release(self, items_to_release, m2_cho_meet):
        unreleased_items_dom_name = ''

        if m2_cho_meet is not None:
            m2_cho_meet_psmids = self._get_m2_cho_meet_psmids()
            for psmid in m2_cho_meet_psmids:
                try:
                    item_in_gaia = Item.objects.get(dom_id=psmid, is_live=True)
                    item_in_gaia.ready_for_qa()
                    unreleased_items_dom_name += item_in_gaia.dom_name + '; '
                except Item.DoesNotExist:
                    pass

        for item in items_to_release:
            item_in_gaia = Item.objects.get(pk=item.id)
            item_in_gaia.ready_for_qa()
            unreleased_items_dom_name += item_in_gaia.dom_name + '; '

        self.msg = 'un-released: %s item(s): %s' % (len(items_to_release), unreleased_items_dom_name.rstrip('; '))
