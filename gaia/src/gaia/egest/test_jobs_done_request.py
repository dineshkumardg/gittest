import unittest
from test_utils.gaia_test import GaiaTest
from gaia.egest.egest_request import EgestRequest
from gaia.egest.jobs_done_request import JobsDoneRequest

class TestJobsDoneRequest(GaiaTest):

    def test_create(self):
        msg = JobsDoneRequest()

        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())
        self.assertTrue(isinstance(msg, JobsDoneRequest,))
        self.assertFalse(isinstance(msg, EgestRequest,))
        
    def test_encode_decode(self):
        msg = JobsDoneRequest()

        encoded_msg = msg.encode()
        decoded_msg = JobsDoneRequest.decode(encoded_msg)

        self.assertTrue(decoded_msg.is_request())
        self.assertFalse(decoded_msg.is_reply())
        self.assertTrue(isinstance(decoded_msg, JobsDoneRequest))
        self.assertFalse(isinstance(msg, EgestRequest,))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestJobsDoneRequest),
    ])

if __name__ == "__main__":
    unittest.main()
