from qa.report.filtered_common_view import FilteredCommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from qa.models import IngestError

@class_view_decorator(permission_required('qa.can_qa'))
class IngestErrorView(FilteredCommonView):
    paginate_by = 35
    template_name = 'qa/report/ingest_errors.html'

    filter_field = 'provider_name'
    search_field = 'report'
    sort_fields_list = ['provider_name', 'when', 'report']
    sort_name_list = ['provider name', 'when', 'error message']
    date_filter_field = 'when'

    def get_data(self):
        return IngestError.objects.all().order_by('-when')
