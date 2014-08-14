from abc import abstractmethod
from qa.view_mixin import SortMixin, SearchMixin, FilterMixin
from django.views.generic import ListView


class FilteredCommonView(ListView, SortMixin, SearchMixin, FilterMixin):
    context_object_name = "context"
    template_name = "qa/template.html"

    filter_field = None  # a database field for filter. TODO: support multi-filter fields in future?
    date_filter_field = None  # override this to create a filter for datetimefield
    date_filter_name_list = ['today', 'past 7 days', 'this month', 'this year']

    msg = ''
    error = ''

    paginate_by = 33

    def get_queryset(self):  # @override from ListView
        self.data = self.get_data()
        self.data = self._before_filter_sort_search(self.data)

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

    def _after_filter_sort_search(self, queryset):
        return queryset

    def _before_filter_sort_search(self, queryset):
        return queryset

    @abstractmethod
    def get_data(self):
        ''' MUST be overridden. For keep update with database.
            This function is to get original(without filter, search, sort) data for database
            returns data in a Queryset
        '''
        pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        context['queryset'] = self.data
        context['filter_types'] = self.get_filter_list(self.get_data(), self.filter_field)

        context['msg'] = self.msg
        context['error'] = self.error

        sort_dict = dict(zip(self.sort_name_list, self.sort_fields_list))
        context['sort_fields_list'] = sort_dict

        if self.date_filter_field:
            context['date_filter_name_list'] = self.date_filter_name_list
        return context
