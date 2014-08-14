from django.contrib.auth.decorators import permission_required
from qa.view_decorator import class_view_decorator
from qa.models import Item, ItemError
from qa.report.filtered_common_view import FilteredCommonView

@class_view_decorator(permission_required('qa.can_qa'))
class RejectionView(FilteredCommonView):
    paginate_by = 35
    template_name = 'qa/report/rejections.html'

    search_field = 'err_msg'
    sort_fields_list = ['when', 'err_msg']
    sort_name_list = ['date', 'report']
    date_filter_field = 'when' 

    def get_data(self):
        return ItemError.objects.filter(item__in=Item.rejections()).order_by('-when')  # newest first
