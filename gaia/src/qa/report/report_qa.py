from qa.common_view import CommonView
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from qa.models import Item, Page, PageActivity

@class_view_decorator(permission_required('qa.can_qa'))
class ReportQaView(CommonView):
    template_name = 'qa/report/reports_qa.html'

    search_field = 'dom_id'
    sort_fields_list = ['dom_id', 'id']
    sort_name_list = ['name', 'id']

    def get_data(self):
        return Item.in_qa()

    # Note: here only get the item information for current page
    def _get_extra_info(self, items):
        qa_items = list(items)
        num_items_in_qa = len(qa_items)
        args = {}
        args['items'] = {}
        args['average_num_pages_per_item'] = 0
        args['average_percent_page_qa_per_item'] = 0
        
        if num_items_in_qa > 0:

            total_pages = 0
            total_percentage_qad = 0
           
            for item in qa_items:
                pages = Page.objects.filter(document__item__id__exact=item.id)
                total_item_pages = pages.count()
                total_pages += total_item_pages
                page_qa_count = 0

                who = set()
                for page in pages:
                    activities = PageActivity.objects.filter(page=page)
                    if activities.count() > 0:
                        page_qa_count += 1
                        for activity in activities:
                            who.add(activity.username)
                who_string = ' '.join(who)

                percentage_qad =  ( float(page_qa_count) / float(total_item_pages) ) * 100
                total_percentage_qad += percentage_qad

                args['items'][item] = {'total_pages': total_item_pages,
                    'page_qa_count': page_qa_count,
                    'percent': '%.1f' % percentage_qad,
                    'who': who_string}

            average_pages_per_item = float(total_pages) / float(num_items_in_qa)
            average_percentage_page_qa_per_item = float(total_percentage_qad) / float(num_items_in_qa)

            args['average_num_pages_per_item'] = '%d' % average_pages_per_item
            args['average_percent_page_qa_per_item'] = '%.1f' % average_percentage_page_qa_per_item

        return args

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ReportQaView, self).get_context_data(**kwargs)
        # context[self.context_object_name] is the data after paginator. i.e.  data for this page not the whole data
        info_dict = self._get_extra_info(context[self.context_object_name])
        context['items_info'] = info_dict['items']

        sort_dict = dict(zip(self.sort_name_list, self.sort_fields_list))
        context['sort_fields_list'] = sort_dict

        context['average_num_pages_per_item'] = info_dict['average_num_pages_per_item']
        context['average_percent_page_qa_per_item'] = info_dict['average_percent_page_qa_per_item']

        return context
