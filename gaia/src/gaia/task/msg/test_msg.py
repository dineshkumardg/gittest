import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.msg import Msg

class TestMsg(GaiaTest):

    def test_create(self):
        msg = Msg('INGEST_JOB', provider='provider_a', item='item_123')

        self.assertEqual('INGEST_JOB', msg.msg_type())
        self.assertEqual('provider_a', msg.provider)
        self.assertEqual('item_123',   msg.item)
        
    def test_encode_decode(self):
        msg = Msg('INGEST_JOB', provider='provider_a', item='item_123')
        self.assertEqual('INGEST_JOB', msg.msg_type())
        self.assertEqual('provider_a', msg.provider)
        self.assertEqual('item_123',   msg.item)

        encoded_msg = msg.encode()
        decoded_msg = Msg.decode(encoded_msg)

        self.assertEqual('INGEST_JOB', decoded_msg.msg_type())
        self.assertEqual('provider_a', decoded_msg.provider)
        self.assertEqual('item_123',   decoded_msg.item)

    def test_getattr(self):
        msg = Msg('INGEST_JOB', provider='provider_a', item='item_123')

        self.assertRaises(AttributeError, msg.__getattr__, 'a_missing_field')   # same as msg.a_missing_field
        
    def test_eq_ne(self):
        msg1a = Msg('INGEST_JOB', provider='provider_a', item='item_123')
        msg1b = Msg('INGEST_JOB', provider='provider_a', item='item_123')
        msg2 = Msg('EGEST_JOB', provider='provider_a', item='item_123')

        self.assertEqual(msg1a, msg1a)
        self.assertEqual(msg1a, msg1b)
        self.assertEqual(msg2, msg2)
        self.assertNotEqual(msg1a, msg2)
        
    def test_str(self):
        # WARNING: the str() method is JUST for debugging use please!
        expected_str = "MSG:INGEST_JOB({'item': 'item_123', 'provider': 'provider_a'})" # WARNING: ordering might make this test fail! TODO

        msg = Msg('INGEST_JOB', provider='provider_a', item='item_123')

        self.assertEqual(expected_str, str(msg))
        
    def test_hash(self):
        # Note:  We need to be able to put Msg classes into dicts, so Msg must be "hashable"
        # here we're testing the __hash__ method indirectly using a dict
        msg1 = Msg('INGEST_JOB', provider='provider_a', item='item_123')
        msg2 = Msg('INGEST_JOB', provider='provider_a', item='item_123')

        msgs = {}
        msgs[msg1] = 1
        msgs[msg2] = 2

        # These should be hashed as the same object
        self.assertEqual(hash(msg1), hash(msg2))
        self.assertEqual(1, len(msgs))

        self.assertEqual(2, msgs[msg1])
        self.assertEqual(2, msgs[msg2])

        msg3 = Msg('INGEST_JOB', provider='provider_a', item='item_999')
        self.assertNotEqual(hash(msg1), hash(msg3))
        msgs[msg3] = 3

        self.assertEqual(2, len(msgs))
        self.assertEqual(3, msgs[msg3])

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestMsg),
    ])

if __name__ == "__main__":
    unittest.main()
