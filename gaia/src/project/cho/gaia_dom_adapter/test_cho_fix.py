import unittest
from gaia.asset.asset import Asset
from project.cho.gaia_dom_adapter.cho import Cho
import os
from gaia.dom.document_error import DocumentError


class TestChoFix(unittest.TestCase):
    """
    Test that the fix gaia xpaths + their value maps 1:1 onto the src - see: EG-469
    """
    def _compareEqual(self, file_count, src_fname, src_gdom_adapter, fix_dict):
        for key in fix_dict:
            fix_xpath = key

            if fix_xpath[0] == '/':
                fix_value = fix_dict[key]

                src_node = src_gdom_adapter._etree.xpath(fix_xpath)
                src_node_value = ''

                if fix_value != src_gdom_adapter.MISSING_FIELD_VALUE:
                    if src_node == []:
                            print '%s: MISSING NODE: %s: %s' % (file_count, src_fname, fix_xpath)
                    else:
                        if key.find('@') != -1:
                            # attr
                            src_node_value = src_node[0]
                        else:
                            # element
                            src_node_value = src_node[0].text

                        try:
                            self.assertEqual(src_node_value, fix_value, '%s: INVALID XPATH: %s: %s' % (file_count, src_fname, fix_xpath))
                        except Exception as e:
                            self.fail(str(e))

    def test_fix_can_be_applied(self):
        """
        find /mnt/nfs/gaia/outbox/ -type f -name '*.xml' -exec cp {} . \;
        py /home/jsears/GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter/test_cho_fix.py > probs

        sed '/relatedDocument/d' probs > probs.1
        sed '/aucomposed/d' probs.1 > probs.2
        sed '/marginalia/d' probs.2 > probs.3
        """
        root_dir = os.path.join(os.path.dirname(__file__), '../../../qa/ws/test_data')
        #root_dir = '<probs>
        for root, dirs, files in os.walk(root_dir):
            file_count = 0
            for fname in files:
                file_count += 1
                if fname.endswith('.xml'):
                    src_fname = os.path.join(root, fname)
                    try:
                        self.dom_adapter = Cho(Asset(src_fname))

                        # .info's store the fixes
                        self._compareEqual(file_count, fname, self.dom_adapter, self.dom_adapter.document().info)

                        try:
                            actual_chunks = self.dom_adapter.chunks()
                            for chunk in actual_chunks:
                                self._compareEqual(file_count, fname, self.dom_adapter, chunk.info)
                        except DocumentError as e:
                            if str(e).index('relatedDocument') == -1:
                                self.fail(str(e))

                        try:
                            actual_pages = self.dom_adapter.pages()
                            for page in actual_pages:
                                self._compareEqual(file_count, fname, self.dom_adapter, page.info)
                        except DocumentError as e:
                            if str(e).index('relatedDocument') == -1:
                                self.fail(str(e))
                    except Exception as e:
                        #print '%s: XMLSyntaxError: %s' % (file_count, fname)
                        self.fail(str(e))


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestChoFix),
    ])

if __name__ == "__main__":
    unittest.main()
