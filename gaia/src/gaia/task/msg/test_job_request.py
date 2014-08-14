import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.request import Request
from gaia.task.msg.job_request import JobRequest

class TestJobRequest(GaiaTest):

    def test_create(self):
        job_name = 'do_xyz_please'
        msg = JobRequest(job_name)

        self.assertEqual('JOB', msg.msg_type())
        self.assertEqual(job_name, msg.job_name)
        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())
        
    def test_create_EXTRA_ARGS(self):
        job_name = 'turn_on_telly'
        msg = JobRequest(job_name, channel=4, volume=12, programme='Two Ronnies')

        self.assertEqual('JOB', msg.msg_type())
        self.assertEqual(job_name, msg.job_name)
        self.assertTrue(msg.is_request())
        self.assertFalse(msg.is_reply())

        self.assertEqual(4, msg.channel)
        self.assertEqual(12, msg.volume)
        self.assertEqual('Two Ronnies', msg.programme)
        
    def test_encode_decode(self):
        job_name = 'do_xyz_please'
        msg = JobRequest(job_name)

        encoded_msg = msg.encode()
        decoded_msg = JobRequest.decode(encoded_msg)

        self.assertEqual('JOB', decoded_msg.msg_type())
        self.assertEqual(job_name, decoded_msg.job_name)
        self.assertTrue(decoded_msg.is_request())
        self.assertFalse(decoded_msg.is_reply())
        
        # Note that we can decode using the base class or any subclass:
        decoded_msg = Request.decode(encoded_msg)

        self.assertEqual('JOB', decoded_msg.msg_type())
        self.assertEqual(job_name, decoded_msg.job_name)
        self.assertTrue(decoded_msg.is_request())
        self.assertFalse(decoded_msg.is_reply())
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestJobRequest),
    ])

if __name__ == "__main__":
    unittest.main()
