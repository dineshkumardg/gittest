import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.msg import Msg
from gaia.task.msg.request import Request
from gaia.task.msg.reply import Reply

class TestReply(GaiaTest):

    def test_create_DEFAULT_REPLY_TYPE(self):
        request = Request('INGEST_JOB', provider='provider_a', item='item_123')
        encoded_request = request.encode()
        reply = Reply(encoded_request, ok=True)

        self.assertEqual('REPLY', reply.msg_type())
        self.assertEqual(True, reply.ok)
        #self.assertEqual(encoded_request, reply.request())
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
    def test_create(self):
        # I'm not sure if we ever want/need a non-default reply typew, but it's possible like this:
        request = Request('INGEST_JOB', provider='provider_a', item='item_123')
        encoded_request = request.encode()
        reply_type = 'INGEST_JOB_REPLY'
        reply = Reply(encoded_request, reply_type, ok=True)

        self.assertEqual(reply_type, reply.msg_type())
        self.assertEqual(True, reply.ok)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
    def test_encode_decode(self):
        request = Request('INGEST_JOB', provider='provider_a', item='item_123')
        encoded_request = request.encode()
        msg = Reply(encoded_request, ok=True)

        encoded_msg = msg.encode()
        decoded_msg = Msg.decode(encoded_msg)   # TODO: Msg factory.. create Req/Reply classes... TODO
        reply = decoded_msg

        self.assertEqual('REPLY', reply.msg_type())
        self.assertEqual(True, reply.ok)
        self.assertEqual(request, reply.request())

        self.assertFalse(reply.is_request())
        self.assertTrue(reply.is_reply())
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestReply),
    ])

if __name__ == "__main__":
    unittest.main()
