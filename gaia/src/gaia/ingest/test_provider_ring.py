import unittest
from testing.gaia_test import GaiaTest
from gaia.config.fake_config import FakeConfig
from gaia.ingest.provider_ring import ProviderRing

class TestProvider():
    def __init__(self, name, transfer_agent, config):
        self.name = name
        self.transfer_agent = transfer_agent
        self.config = config


class TestTransferAgent():
    def __init__(self, server, uid, pwd):
        self.server = server
        self.uid = uid
        self.pwd = pwd


class TestProviderRing(GaiaTest):

    def test__init__(self):
        config = FakeConfig()
        config.content_providers = {'provider_one':   {'server': 'IP Address', 'uid': 'User name', 'pwd': 'Password'}, }

        pr = ProviderRing(config, _transfer_agent_class=TestTransferAgent, _provider_class=TestProvider)
        provider, transfer_agent = pr._providers[0]

        self.assertIsInstance(pr, ProviderRing)
        self.assertEqual(0, pr._index)
        self.assertEqual(1, len(pr._providers))
        self.assertIsInstance(provider, TestProvider)
        self.assertIsInstance(transfer_agent, TestTransferAgent)    

    def test_next(self):
        config = FakeConfig()
        config.content_providers = {'provider_one':   {'server': 'addr_one', 'uid': 'user_one', 'pwd': 'pwd_one'}, 
                                    'provider_two':   {'server': 'addr_two', 'uid': 'user_two', 'pwd': 'pwd_two'},
                                   }
        
        pr = ProviderRing(config, _transfer_agent_class=TestTransferAgent, _provider_class=TestProvider)
        
        provider, transfer_agent = pr.next()
        
        self.assertIsInstance(provider, TestProvider)
        self.assertIsInstance(transfer_agent, TestTransferAgent)
        self.assertEqual('provider_one', provider.name)
        self.assertEqual('addr_one', provider.transfer_agent.server)
        self.assertEqual('user_one', provider.transfer_agent.uid)
        self.assertEqual('pwd_one', provider.transfer_agent.pwd)
        
        provider, transfer_agent = pr.next()
        self.assertIsInstance(provider, TestProvider)
        self.assertIsInstance(transfer_agent, TestTransferAgent)
        self.assertEqual('provider_two', provider.name)
        self.assertEqual('addr_two', provider.transfer_agent.server)
        self.assertEqual('user_two', provider.transfer_agent.uid)
        self.assertEqual('pwd_two', provider.transfer_agent.pwd)
        

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestProviderRing),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
