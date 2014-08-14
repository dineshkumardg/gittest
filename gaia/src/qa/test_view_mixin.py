from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from qa.view_mixin import FilterMixin, SearchMixin, SortMixin
from django.test import TestCase
from qa.models import IngestError
from django.test.client import Client
from django.utils import unittest
import operator

class TestFilterMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.filter_mixin = FilterMixin()

        # create items
        self.ingest_err1 = IngestError(provider_name="FirstProvider", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0003_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0003_000_0000.xml, schema=chatham_house.xsd")
        self.ingest_err2 = IngestError(provider_name="SecondProvider", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0001_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0001_000_0000.xml, schema=chatham_house.xsd")
        self.ingest_today = IngestError(provider_name="FirstProvider", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0003_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0003_000_0000.xml, schema=chatham_house.xsd")

        self.ingest_err1.save()
        self.ingest_err2.save()
        self.ingest_today.save()

        self.query_set = IngestError.objects.all()

    def test_get_queryset_filters(self):
        expected_items = [self.ingest_err1, self.ingest_today]
        expected_num = 2
        filter_field = "provider_name"
        filter_by = "FirstProvider"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)
        for item in result:
            in_expected = item in expected_items
            self.assertTrue(in_expected, True)

    def test_get_queryset_filters_EMPTY(self):
        expected_num = 0
        filter_field = "provider_name"
        filter_by = "ThirdProvider"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    # NOTE: becaue auto_now_add = True in IngestError when field, the date seems unable to change. It will awlways be current timestamp. Improve in future?
    def test_get_queryset_filters_by_date_Today(self):
        expected_num = 3
        filter_field = "provider_name"
        filter_by = "today"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    def x_test_get_queryset_filters_by_date_PAST_7_DAYS(self):
        expected_num = 3
        filter_field = "provider_name"
        filter_by = "past-7-days"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    def x_test_get_queryset_filters_by_date_THIS_MONTH(self):
        expected_num = 3
        filter_field = "provider_name"
        filter_by = "this-month"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    def x_test_get_queryset_filters_by_date_THIS_YEAR(self):
        expected_num = 3
        filter_field = "provider_name"
        filter_by = "this-year"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    def test_get_queryset_filters_by_date_EMPTY(self):
        expected_num = 0
        filter_field = "provider_name"
        filter_by = "Tomorrow"

        result = self.filter_mixin.get_queryset_filters(self.query_set, filter_by, filter_field )

        self.assertEqual(len(result), expected_num)

    # test function get_filter_list()
    def test_get_filter_list_OK(self):
        field = "provider_name"
        expected_filter = ["FirstProvider", "SecondProvider"]

        result = self.filter_mixin.get_filter_list(self.query_set, field)

        self.assertEqual(result, expected_filter)

class TestSortMixin(TestCase):
    def setUp(self):
        self.test_query_set=[]
        self.test_query_set.append(IngestError.objects.create(provider_name="FirstProvider", when="13 May 2013", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0003_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0003_000_0000.xml, schema=chatham_house.xsd"))
        self.test_query_set.append(IngestError.objects.create(provider_name="SecondProvider", when="10 May 2013", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0001_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0001_000_0000.xml, schema=chatham_house.xsd"))

    def test_get_queryset_sort_BY_PROVIDER(self):# to test sort my provider name
        sort=SortMixin()
        result=sort.get_queryset_sort(self.test_query_set, "provider_name")
        self.expected = sorted(list(self.test_query_set), key=operator.attrgetter('provider_name'))
        for i in range (0, len(result)):
            self.assertEqual(result[i].report, self.expected[i].report)
            self.assertEqual(result[i].provider_name, self.expected[i].provider_name)

    def test_get_queryset_sort_BY_WHEN(self):# to test sort my when oldest first
        sort=SortMixin()
        result=sort.get_queryset_sort(self.test_query_set, "when")
        self.expected = sorted(list(self.test_query_set), key=operator.attrgetter('when'))
        for i in range (0, len(result)):
            self.assertEqual(result[i].provider_name, self.expected[i].provider_name)
            self.assertEqual(result[i].report, self.expected[i].report)

    def test_get_queryset_sort_BY_REVERSE_DATE(self):# to test sort my when newest first
        sort=SortMixin()
        result=sort.get_queryset_sort(self.test_query_set, "-when")
        self.expected = sorted(list(self.test_query_set), key=operator.attrgetter('when'), reverse=True)
        for i in range (0, len(result)):
            self.assertEqual(result[i].report, self.expected[i].report)
            self.assertEqual(result[i].provider_name, self.expected[i].provider_name)

    # test update_sort_fields function
    def test_update_sort_fields_OK(self):
        sort=SortMixin()
        sort_by = "when"
        sort_field_list = ["provider_name", "when", "report"]
        expected_sort_field_list = ["provider_name", "-when", "report"]
        
        result = sort.update_sort_fields(sort_by, sort_field_list)
        self.assertEqual(result, expected_sort_field_list)

class TestSearchMixin(TestCase):
    def setUp(self):
        self.test_query_set=[]
        self.test_query_set.append(IngestError.objects.create(provider_name="FirstProvider", when="13 May 2013", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0003_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0003_000_0000.xml, schema=chatham_house.xsd"))
        self.test_query_set.append(IngestError.objects.create(provider_name="SecondProvider", when="10 May 2013", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0001_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0001_000_0000.xml, schema=chatham_house.xsd"))

    def test_get_queryset_search(self):
        search=SearchMixin()
        result=search.get_queryset_search(self.test_query_set, "cho_bcrc_1933_0003_000_0000.xml", "report")
        self.expected = []
        self.expected.append(IngestError.objects.create(provider_name="FirstProvider", when="13 May 2013", report="Error Report for Fisrt_content_provider Problem with Item cho_bcrc_1933_0003_000_0000 in Group al InvalidXml: line=56, error=Element 'articleInfo': Missing child element(s). Expected is one of ( startingColumn, pageCount )., file=cho_bcrc_1933_0003_000_0000.xml, schema=chatham_house.xsd"))
        for i in range (0, len(result)):
            self.assertEqual(result[i].report, self.expected[i].report)
            self.assertEqual(result[i].provider_name, self.expected[i].provider_name)

    def test_get_queryset_search_EMPTY(self):
        search=SearchMixin()
        result=search.get_queryset_search(self.test_query_set, "not_exist.xml", "report")
        self.expected = []
        self.assertEqual(result, self.expected)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestSearchMixin),
    unittest.TestLoader().loadTestsFromTestCase(TestSortMixin),
    unittest.TestLoader().loadTestsFromTestCase(TestFilterMixin),
    ])
  

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)    
