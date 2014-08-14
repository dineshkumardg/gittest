from abc import abstractmethod
from qa.view_mixin import SortMixin, SearchMixin
from django.views.generic import ListView


class CommonView(ListView, SortMixin, SearchMixin):
    context_object_name = "context"
    template_name = "qa/template.html"    # override this in each view

    def get_queryset(self):
        self.items = self.get_data()

        # implement search mixin 
        if self.search_field:
            search_by = self.request.GET.get(self.search_url_name)
            self.items = self.get_queryset_search(self.items, search_by, self.search_field)

        # implement sort mixin 
        if self.sort_fields_list:
            sort_by =  self.request.GET.get(self.sort_url_name)
            self.items = self.get_queryset_sort(self.items, sort_by)
            # update sort fields (function to control sort url)
            self.sort_fields_list = self.update_sort_fields(sort_by, self.sort_fields_list)

        return self.items

    @abstractmethod
    def get_data(self):
        pass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        context['items'] = self.items
        sort_dict = dict(zip(self.sort_name_list, self.sort_fields_list))
        context['sort_fields_list'] = sort_dict

        return context
