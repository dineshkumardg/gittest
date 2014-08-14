import operator
import datetime


class FilterMixin(object):
    filter_url_name = "filter_by"   # name in url, override to change this.
    def get_queryset_filters(self, queryset, filter_by, attr_name):
        if filter_by:
            filted_queryset = []
            filted_queryset = self._check_filter_by_date(queryset, filter_by)

            if filted_queryset != []:   # filter by date
                queryset = filted_queryset
            else:
                # support multi-depth attribute (split by ".")
                attr = operator.attrgetter(attr_name)
                for item in queryset:
                    if filter_by in attr(item):
                        filted_queryset.append(item)

                queryset = filted_queryset
        return queryset

    # function to get the list of filters which will be displayed on template
    def get_filter_list(self, queryset, field):
        if field == None:   # filter field not override => no filter
            return []
        else:   # get all unique values in this field as filters
            filter_types = []
            field_data = queryset.values(field)
            for onetype in field_data:
                if onetype[field] not in filter_types:
                    filter_types.append(onetype[field])
            filter_types.sort()
        return filter_types

    def _check_filter_by_date(self, queryset, filter_by):
        today = datetime.date.today()
        if filter_by == "today":
            return queryset.filter(when__year=today.year, when__month=today.month, when__day=today.day)
        elif filter_by == "past-7-days":
            startdate = datetime.date.today()
            fromdate = startdate - datetime.timedelta(days=7)
            return queryset.filter(when__gte=fromdate)
        elif filter_by == "this-month":
            return queryset.filter(when__year=today.year, when__month=today.month)
        elif filter_by == "this-year":
            return queryset.filter(when__year=today.year)
        else:
            return []


class SearchMixin(object):
    search_url_name = "search_by"
    search_field = None  # a database field for search

    def get_queryset_search(self, queryset, search_by, attr_names):
        if search_by:
            search_by = search_by.strip()  # remove tailing and leading spaces
            searched_queryset = []
            attrs = []
            # support multi-depth attribute
            if type(attr_names) == str:
                attr = operator.attrgetter(attr_names)

                for item in queryset:
                    if search_by in attr(item):
                        searched_queryset.append(item)

                queryset = searched_queryset

            elif type(attr_names) == list:
                for attr_name in attr_names:
                    attrs.append(operator.attrgetter(attr_name))

                for item in queryset:
                    for attr in attrs:
                        if search_by in attr(item):
                            searched_queryset.append(item)

                queryset = sorted(list(set(searched_queryset)))

        return queryset


class SortMixin(object):
    sort_fields_list = []  # list of fields for sort
    sort_name_list = []  # a list of names which displayed in template and match the sort_field_list
    sort_url_name = "sort_by"

    def get_queryset_sort(self, queryset, sort_by):
        if sort_by:
            if sort_by[0] == "-":   # start with "-" means sort reverse.
                sort_by = sort_by[1:]
                queryset = sorted(list(queryset), key=operator.attrgetter(sort_by), reverse=True)
            else:
                queryset = sorted(list(queryset), key=operator.attrgetter(sort_by))
        return queryset

    # function to control sort url
    def update_sort_fields(self, sort_by, sort_fields_list):
        if sort_by:
            for field in sort_fields_list:
                if sort_by == field and field[0] == "-":
                    new_field = sort_by[1:]
                    index = sort_fields_list.index(field)
                    sort_fields_list.remove(field)
                    sort_fields_list.insert(index, new_field)
                elif sort_by == field and field[0] != "-":
                    new_field = "-" + sort_by
                    index = sort_fields_list.index(field)
                    sort_fields_list.remove(field)
                    sort_fields_list.insert(index, new_field)
        return sort_fields_list
