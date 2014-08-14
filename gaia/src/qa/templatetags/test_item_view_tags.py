from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()

import unittest
from django.test import TestCase
from qa.templatetags.item_view_tags import get_bin_chunk


class TemplateTagsTestCase(TestCase):
    def test_get_bin_chunk_found(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual(1, get_bin_chunk(d, 'a'))

        # For information, the following reflects the real data...
        # In reality, this is what we're doing, ie looking up binary chunk info by text chunks:
        binary_chunk_tuples = [('bin_chunk.dom_name_1', 'bin_page_dom_id_1'),
                               ('bin_chunk.dom_name_2', 'bin_page_dom_id_2'),
                              ]
        d = {'text_chunk_dom_id': binary_chunk_tuples, 'b': 2}
        self.assertEqual(binary_chunk_tuples, get_bin_chunk(d, 'text_chunk_dom_id'))

    def test_get_bin_chunk_not_found(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual([], get_bin_chunk(d, 'c'))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TemplateTagsTestCase),
    ])

test.tearDown()
