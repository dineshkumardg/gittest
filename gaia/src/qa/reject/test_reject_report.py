import unittest
from qa.reject.reject_report import RejectReport


class TestRejectReport(unittest.TestCase):
    def test_str(self):
        class TestableRejectReport(RejectReport):
            def _utcnow(self):
                return '31 Oct 2012, 11:58 am'

        expected_report = '''Item Rejected
----------
Item: cho_iaxx_0000_1111
User: chumphreys
----------
<reason for rejection>
----------
Report Date: 31 Oct 2012, 11:58 am'''

        reason = u'<reason for rejection>'
        item_index_id=123
        item_dom_id=777
        item_dom_name = 'cho_iaxx_0000_1111'
        page_id=9
        user_name='chumphreys'

        reject_report = TestableRejectReport(reason, item_index_id, item_dom_id, item_dom_name, user_name, page_id)

        self.assertEqual(str(expected_report), str(reject_report))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestRejectReport),
    ])

if __name__ == "__main__":
    unittest.main()
