import unittest
from test_utils.gaia_test import GaiaTest
from project.cho.egest_adapter.feed.feed_wrapper import FeedWrapper


class TestFeedWrapper(GaiaTest):
    def test_feed_wrapper(self):
        # EXPECTATION
        expected_header= '''<?xml version="1.0" encoding="UTF-8"?><gold:feed xmlns:essay="http://www.gale.com/goldschema/essay" xmlns:gold="http://www.gale.com/gold" xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc" xmlns:dir="http://www.gale.com/goldschema/dir" xmlns:vault-link="http://www.gale.com/goldschema/vault-linking" xmlns:meta="http://www.gale.com/goldschema/metadata" xmlns:table="http://www.gale.com/goldschema/table" xmlns:xatts="http://www.gale.com/goldschema/xatts" xmlns:index="http://www.gale.com/goldschema/index" xmlns:mla="http://www.gale.com/goldschema/mla" xmlns:media="http://www.gale.com/goldschema/media" xmlns:tt="http://www.w3.org/ns/ttml" xmlns:list="http://www.gale.com/goldschema/list" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:etoc="http://www.gale.com/goldschema/etoc" xmlns:verse="http://www.gale.com/goldschema/verse" xmlns:pres="http://www.gale.com/goldschema/pres" xmlns:pub-meta="http://www.gale.com/goldschema/pub-meta" xmlns:shared="http://www.gale.com/goldschema/shared" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:math="http://www.w3.org/1998/Math/MathML" id="cho_meet_1922_0010_000_0000_001" xsi:schemaLocation="..\\..\\..\\..\\..\\GIFT\\feed_schemas\\feed.xsd">'''

        expected_footer = '''<gold:metadata><gold:feed-type>NOINDEX</gold:feed-type><gold:document-schema>gift_document.xsd</gold:document-schema><gold:schema-version>2.5</gold:schema-version><gold:document-id-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value</gold:document-id-path><gold:document-mcode-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode</gold:document-mcode-path><gold:number-of-documents>1</gold:number-of-documents><gold:feed-status>New-Replace</gold:feed-status></gold:metadata></gold:feed>
'''

        # TEST
        wrapper = FeedWrapper(1, feed_id='cho_meet_1922_0010_000_0000_001', is_indexed=False)

        # ASSERTION
        self.assertEqual(expected_header, wrapper.header())
        self.assertEqual(expected_footer, wrapper.footer())


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestFeedWrapper),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
