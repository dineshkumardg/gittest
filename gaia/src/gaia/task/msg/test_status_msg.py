import unittest
from test_utils.gaia_test import GaiaTest
from gaia.task.msg.status_msg import StatusMsg

class TestStatusMsg(GaiaTest):

    def test_create(self):
        msg = StatusMsg(elephants=12, size='huge')

        self.assertEqual('STATUS', msg.msg_type())
        self.assertEqual(12, msg.elephants)
        self.assertEqual('huge',   msg.size)
        
    def test_encode_decode(self):
        msg = StatusMsg(elephants=12, size='huge')

        encoded_msg = msg.encode()
        decoded_msg = StatusMsg.decode(encoded_msg)

        self.assertEqual('STATUS', decoded_msg.msg_type())
        self.assertEqual(12, decoded_msg.elephants)
        self.assertEqual('huge', decoded_msg.size)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestStatusMsg),
    ])

if __name__ == "__main__":
    unittest.main()
