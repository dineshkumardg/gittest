import unittest
from test_utils.gaia_test import GaiaTest
from gaia.egest.egest_request import EgestRequest

class TestEgestRequest(GaiaTest):

    def test_create(self):
        item_id = 'item_123'
        item_name = 'cho_meet_123'
        release_type = 'xml'
        expected_job_name = 'item_123|cho_meet_123'
        msg = EgestRequest(item_id, item_name, release_type)

        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())

        self.assertEqual(expected_job_name, msg.job_name)
        self.assertEqual(item_id, msg.item_id)
        self.assertEqual(item_name, msg.item_name)
        self.assertEqual(release_type, msg.release_type)
        
    def test_encode_decode(self):
        item_id = 'item_123'
        item_name = 'cho_meet_123'
        release_type = 'xml'
        expected_job_name = 'item_123|cho_meet_123'
        msg = EgestRequest(item_id, item_name, release_type)

        encoded_msg = msg.encode()
        decoded_msg = EgestRequest.decode(encoded_msg)

        self.assertTrue(decoded_msg.is_request())
        self.assertFalse(decoded_msg.is_reply())

        self.assertEqual(expected_job_name, decoded_msg.job_name)
        self.assertEqual(item_id, decoded_msg.item_id)
        self.assertEqual(item_name, decoded_msg.item_name)
        self.assertEqual(release_type, msg.release_type)
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestEgestRequest),
    ])

if __name__ == "__main__":
    unittest.main()
