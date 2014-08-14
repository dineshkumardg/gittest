import csv
import time
from qa.models import Item
from qa.common_view import CommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse


@class_view_decorator(permission_required('qa.can_qa'))
class ReleaseItemListView(CommonView):
    template_name = "qa/report/released_items.html"
    search_field = 'dom_id'
    sort_name_list=['id', 'name']
    sort_fields_list = ['id', 'dom_id']
    
    def get_data(self):
        return Item.in_released()


def csv_released_items(request):
    response = HttpResponse(mimetype='text/csv')
    fname = "released_items-%s.csv" % time.strftime("%Y%m%d")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    # EG-467
    response['Pragma'] = 'public'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Cache-Control'] = 'private'
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Transfer-Encoding'] = 'binary'

    writer = csv.writer(response, delimiter="|")
    writer.writerow(ReleaseItemListView.sort_name_list)

    released_items = Item.in_released()
    for item in released_items:
        writer.writerow([item.id, item.dom_name])

    return response
