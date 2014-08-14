import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.msg import Msg
from gaia.task.msg.job_request import JobRequest
from gaia.task.msg.job_reply import JobReply, OkReply, FailedReply, TryAgainReply

class TestOkReply(GaiaTest):

    def test_ok(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        reply = OkReply(encoded_request)

        self.assertEqual(JobReply.OK, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
    def test_encode_decode(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        msg = OkReply(encoded_request)

        encoded_msg = msg.encode()
        decoded_msg = Msg.decode(encoded_msg)
        reply = decoded_msg

        self.assertEqual(JobReply.OK, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
class TestTryAgainReply(GaiaTest):

    def test_ok(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        reply = TryAgainReply(encoded_request)

        self.assertEqual(JobReply.TRY_AGAIN, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
    def test_encode_decode(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        msg = TryAgainReply(encoded_request)

        encoded_msg = msg.encode()
        decoded_msg = Msg.decode(encoded_msg)
        reply = decoded_msg

        self.assertEqual(JobReply.TRY_AGAIN, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
class TestFailedReply(GaiaTest):

    def test_ok(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        reply = FailedReply(encoded_request)

        self.assertEqual(JobReply.FAILED, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
    def test_encode_decode(self):
        job_name = 'do_xyz_please'
        request = JobRequest(job_name)
        encoded_request = request.encode()

        msg = FailedReply(encoded_request)

        encoded_msg = msg.encode()
        decoded_msg = Msg.decode(encoded_msg)
        reply = decoded_msg

        self.assertEqual(JobReply.FAILED, reply.status)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestOkReply),
    unittest.TestLoader().loadTestsFromTestCase(TestTryAgainReply),
    unittest.TestLoader().loadTestsFromTestCase(TestFailedReply),
    ])

if __name__ == "__main__":
    unittest.main()
