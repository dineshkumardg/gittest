import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.request import Request

class TestRequest(GaiaTest):

    def test_create(self):
        msg = Request('INGEST_JOB', provider='provider_a', item='item_123')

        self.assertEqual('INGEST_JOB', msg.msg_type())
        self.assertEqual('provider_a', msg.provider)
        self.assertEqual('item_123',   msg.item)
        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())
        
    def test_encode_decode(self):
        msg = Request('INGEST_JOB', provider='provider_a', item='item_123')
        self.assertEqual('INGEST_JOB', msg.msg_type())
        self.assertEqual('provider_a', msg.provider)
        self.assertEqual('item_123',   msg.item)
        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())

        encoded_msg = msg.encode()
        decoded_msg = Request.decode(encoded_msg)

        self.assertEqual('INGEST_JOB', decoded_msg.msg_type())
        self.assertEqual('provider_a', decoded_msg.provider)
        self.assertEqual('item_123',   decoded_msg.item)
        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())

    def test_getattr(self):
        msg = Request('INGEST_JOB', provider='provider_a', item='item_123')

        self.assertRaises(AttributeError, msg.__getattr__, 'a_missing_field')   # same as msg.a_missing_field
        
        

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestRequest),
    ])

if __name__ == "__main__":
    unittest.main()
