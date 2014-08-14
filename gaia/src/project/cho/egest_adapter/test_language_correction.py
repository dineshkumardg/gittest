import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()


class Config:
    pass


from project.cho.egest_adapter.language_correction import LanguageCorrection
from django.test import TestCase
from qa.models import Language


class TestLanguageCorrection(TestCase):
    config = Config

    # override setUp as sometimes a method blats out self.config
    def setUp(self):
        self.config.CONFIG_NAME = 'UNIT_TEST'

    def test_get_language_missing(self):
        product_content_type = "Meetings"
        psmid = "cho_meet_1999_0000_000_0000"
        article_id = 1
        content_type = None
        expected_language = u""

        language = Language(psmid=psmid, article_id=article_id, lang='')
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Meetings(self):
        product_content_type = "Meetings"
        psmid = "cho_meet_1931_0157_000_0000"
        article_id = 1
        content_type = None
        expected_language = "English"

        language = Language(psmid=psmid, article_id=article_id, lang=expected_language)
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Meetings_NOT_EXIST(self):
        product_content_type = "Meetings"
        psmid = "cho_meet_0000_0000_000_0000"
        article_id = 1
        content_type = None
        expected_language = 'English'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Reports(self):
        product_content_type = "Pamphlets and Reports"
        psmid = "cho_chrx_1931_0001_016_0000"
        article_id = 1
        content_type = None
        expected_language = "English"

        language = Language(psmid=psmid, article_id=article_id, lang=expected_language)
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Reports_NOT_EXIST(self):
        product_content_type = "Pamphlets and Reports"
        psmid = "cho_chrx_0000_0001_000_0000"
        article_id = 1
        content_type = None
        expected_language = 'English'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_ConferenceSeries(self):
        product_content_type = "Conference Series"
        psmid = "cho_iprx_1931_0005_000_0000"
        article_id = 2
        content_type = None
        expected_language = "English"

        language = Language(psmid=psmid, article_id=1, lang=expected_language)
        language.save()
        language = Language(psmid=psmid, article_id=2, lang=expected_language)
        language.save()
        language = Language(psmid=psmid, article_id=3, lang=expected_language)
        language.save()
        language = Language(psmid=psmid, article_id=4, lang=expected_language)
        language.save()
        language = Language(psmid=psmid, article_id=5, lang=expected_language)
        language.save()
        language = Language(psmid=psmid, article_id=6, lang=expected_language)
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_ConferenceSeries_NOT_EXIST(self):
        product_content_type = "Conference Series"
        psmid = "cho_bcrc_0000_0001_000_0000"
        article_id = 2
        content_type = None
        expected_language = 'English'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_RefugeeSurvey(self):
        product_content_type = "Special Publications"
        psmid = "cho_rsxx_1937-1938_0001_000_0000"
        article_id = 2
        content_type = "book"
        expected_language = "French"

        language = Language(psmid=psmid, article_id=1, lang='English')
        language.save()
        language = Language(psmid=psmid, article_id=2, lang='French')
        language.save()
        language = Language(psmid=psmid, article_id=3, lang='English')
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Journal(self):
        product_content_type = "Journals"
        psmid = "cho_iaxx_1926_0005_000_0000"
        article_id = 2
        content_type = None
        expected_language = "English"

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_ForeignPressJournal(self):
        product_content_type = "Special Publications"
        psmid = "cho_iaxx_1926_0005_000_0000"
        article_id = 2
        content_type = "journal"
        expected_language = "English"

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_InternationalLawJournal(self):
        product_content_type = "Survey and Documents Series"
        psmid = "cho_sbca_1918-1936_0001_000_0000"
        article_id = 2
        content_type = "book"
        expected_language = "English"

        language = Language(psmid=psmid, article_id=1, lang='English')
        language.save()
        language = Language(psmid=psmid, article_id=2, lang='English')
        language.save()
        language = Language(psmid=psmid, article_id=3, lang='English')
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Books(self):
        product_content_type = "Books"
        psmid = "cho_book_1929_heald_000_0000"
        article_id = 1
        content_type = "book"
        expected_language = "English"

        language = Language(psmid=psmid, article_id=1, lang='English')
        language.save()
        language = Language(psmid=psmid, article_id=2, lang='English')
        language.save()
        language = Language(psmid=psmid, article_id=3, lang='English')
        language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_Books_NOT_EXIST(self):
        product_content_type = "Books"
        psmid = "cho_book_0000_heald_000_0000"
        article_id = 1
        content_type = "book"
        expected_language = 'English'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_TEST_ITEMS(self):
        product_content_type = "Books"
        psmid = "cho_meet_2010_7771_0010"
        article_id = 1
        content_type = "book"
        expected_language = "English"
        self.config.CONFIG_NAME = 'SYSTEM_TEST'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_language_TEST_ITEMS_bcrc(self):
        product_content_type = "Books"
        psmid = "cho_bcrc_2010_7771_0010"
        article_id = 1
        content_type = "book"
        expected_language = "English"
        self.config.CONFIG_NAME = 'SYSTEM_TEST'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_language(product_content_type, psmid, article_sequence=article_id, content_type=content_type)

        self.assertEqual(expected_language, language)

    # ================== Test get_parent_languages =====================================================
    def test_get_parent_language_Meetings(self):
        product_content_type = "Meetings"
        psmid = "cho_meet_1931_0157_000_0000"
        content_type = None
        expected_language = ["English"]

        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Meetings_NOT_EXIST(self):
        product_content_type = "Meetings"
        psmid = "cho_meet_0000_0000_000_0000"
        content_type = None
        expected_language = ['English']

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Reports(self):
        product_content_type = "Pamphlets and Reports"
        psmid = "cho_chrx_1931_0001_016_0000"
        content_type = None
        expected_language = ["English"]

        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Reports_NOT_EXIST(self):
        product_content_type = "Pamphlets and Reports"
        psmid = "cho_chrx_0000_0001_000_0000"
        content_type = None
        expected_language = ['English']

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)
        self.config.CONFIG_NAME = 'UNIT_TEST'

    def test_get_parent_language_ConferenceSeries(self):
        product_content_type = "Conference Series"
        psmid = "cho_bcrc_1959_0001_000_0000"
        content_type = None
        expected_language = ["English"]

        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=2, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=3, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=4, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=5, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=6, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=7, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=8, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=9, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=10, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=11, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=12, lang='English')
        _language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_ConferenceSeries_NOT_EXIST(self):
        product_content_type = "Conference Series"
        psmid = "cho_bcrc_0000_0001_000_0000"
        content_type = None
        expected_language = ['English']

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_RefugeeSurvey(self):
        product_content_type = "Special Publications"
        psmid = "cho_rsxx_1937-1938_0002_000_0000"
        content_type = "book"
        expected_language = ['French', 'English', 'Russian']

        _language = Language(psmid=psmid, article_id=1, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=2, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=3, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=4, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=5, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=6, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=7, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=8, lang='French')
        _language.save()
        _language = Language(psmid=psmid, article_id=9, lang='Russian')
        _language.save()
        _language = Language(psmid=psmid, article_id=10, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=11, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=12, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=13, lang='English')
        _language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Journal(self):
        product_content_type = "Journals"
        psmid = "cho_iaxx_1926_0005_000_0000"
        content_type = None
        expected_language = ["English"]

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_ForeignPressJournal(self):
        product_content_type = "Special Publications"
        psmid = "cho_iaxx_1926_0005_000_0000"
        content_type = "journal"
        expected_language = ["English"]

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_InternationalLawJournal(self):
        product_content_type = "Survey and Documents Series"
        psmid = "cho_iaxx_1926_0005_000_0000"
        content_type = "book"
        expected_language = ["English"]

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Books(self):
        product_content_type = "Books"
        psmid = "cho_book_1929_heald_000_0000"
        content_type = "book"
        expected_language = ["English"]

        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()
        _language = Language(psmid=psmid, article_id=1, lang='English')
        _language.save()

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_Books_NOT_EXIST(self):
        product_content_type = "Books"
        psmid = "cho_book_0000_heald_000_0000"
        content_type = "book"
        expected_language = ['English']

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_TEST_ITEMS(self):
        product_content_type = "Books"
        psmid = "cho_meet_2010_7771_0010"
        content_type = "book"
        expected_language = ["English"]
        self.config.CONFIG_NAME = 'SYSTEM_TEST'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)

    def test_get_parent_language_TEST_ITEMS_bcrc(self):
        product_content_type = "Books"
        psmid = "cho_bcrc_2010_7771_0010"
        content_type = "book"
        expected_language = ["English"]
        self.config.CONFIG_NAME = 'SYSTEM_TEST'

        language_correction = LanguageCorrection(self.config)
        language = language_correction.get_parent_languages(product_content_type, psmid, content_type=content_type)

        self.assertEqual(expected_language, language)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLanguageCorrection),
    ])

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
