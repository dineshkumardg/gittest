from qa.models import Item, ItemError
from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from django.template.context import RequestContext


@class_view_decorator(permission_required('qa.can_qa'))
class ItemErrorView(FilteredCommonView):
    paginate_by = 35
    template_name = 'qa/report/item_errors.html'

    filter_field = 'err_type'
    search_field = 'err_msg'
    sort_fields_list = ['err_type', 'when', 'item.dom_id', 'err_msg']
    sort_name_list = ['error type', 'date', 'item name','error message']
    date_filter_field = 'when'

    def get_data(self):
        return ItemError.objects.filter(item__in=Item.in_error()).order_by('-when')

    def post(self, request, *args, **kwargs):
        items_to_move_back_into_qa = request.POST.getlist('move_back_into_qa')
        if len(items_to_move_back_into_qa) > 0:
            for item in items_to_move_back_into_qa:
                item = Item.objects.get(dom_id=item, is_live=True)
                item.ready_for_qa() # move back into QA state

        # return self.get(request, *args, **kwargs)
        return self.get(RequestContext(request, {}), *args, **kwargs)
