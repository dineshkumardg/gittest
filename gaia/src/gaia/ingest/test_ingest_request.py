import unittest
from test_utils.gaia_test import GaiaTest
from gaia.ingest.ingest_request import IngestRequest

class TestIngestRequest(GaiaTest):

    def test_create(self):
        provider_name = 'provider1'
        group = 'all'
        item_name = 'cho_meet_123'
        expected_job_name = 'provider1|all|cho_meet_123'
        msg = IngestRequest(provider_name, group, item_name)

        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())

        self.assertEqual(expected_job_name, msg.job_name)
        self.assertEqual(provider_name, msg.provider_name)
        self.assertEqual(group, msg.group)
        self.assertEqual(item_name, msg.item_name)
        
    def test_encode_decode(self):
        provider_name = 'provider1'
        group = 'all'
        item_name = 'cho_meet_123'
        expected_job_name = 'provider1|all|cho_meet_123'
        msg = IngestRequest(provider_name, group, item_name)

        encoded_msg = msg.encode()
        decoded_msg = IngestRequest.decode(encoded_msg)

        self.assertTrue(decoded_msg.is_request())
        self.assertFalse(decoded_msg.is_reply())

        self.assertEqual(expected_job_name, decoded_msg.job_name)
        self.assertEqual(provider_name, decoded_msg.provider_name)
        self.assertEqual(group, decoded_msg.group)
        self.assertEqual(item_name, decoded_msg.item_name)
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestIngestRequest),
    ])

if __name__ == "__main__":
    unittest.main()
