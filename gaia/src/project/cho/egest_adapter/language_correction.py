'''
NOTE LanguageMissing is thrown by callers NOT by this class
'''
import operator
from gaia.log.log import Log
from qa.models import Language


class LanguageCorrection:
    ENGLISH = 'English'

    def __init__(self, config):
        self.log = Log.get_logger(self)
        self.config = config

    def get_language(self, product_content_type, psmid, article_sequence=1, content_type=""):
        # get a language for one article

        self.log.info(product_content_type=product_content_type, psmid=psmid, article_sequence=article_sequence, content_type=content_type)
        _language = None

        try:
            language = Language.objects.get(psmid=psmid, article_id=article_sequence)
            _language = language.lang
        except Language.DoesNotExist:
            _language = LanguageCorrection.ENGLISH
        finally:
            if _language is None:
                _language = LanguageCorrection.ENGLISH
            self.log.info(language=_language)
            return _language

    def get_parent_languages(self, product_content_type, psmid, content_type=""):
        # get languages from one items for setting languages in parent feed file

        self.log.info(product_content_type=product_content_type, psmid=psmid, content_type=content_type)
        _languages = []

        try:
            langs = Language.langs(psmid)
            for lang in langs:
                _languages.append(lang)
        except Language.DoesNotExist:
            _languages = [LanguageCorrection.ENGLISH]
        finally:
            if _languages == []:
                _languages = [LanguageCorrection.ENGLISH]
            self.log.info(languages=_languages)
            return self._sort_by_primary(_languages)

    def _sort_by_primary(self, lang_list):
        # put primary language into the first index
        result = []

        try:
            self.log.enter(lang_list=lang_list)

            languages = {}

            for language in set(lang_list):
                languages[language] = 1  # each language starts with 0

            for language in lang_list:
                languages[language] = languages[language] + 1

            sorted_languages = sorted(languages.iteritems(), key=operator.itemgetter(1))
            sorted_languages.reverse()

            for language_tuple in sorted_languages:
                result.append(language_tuple[0])
            return result
        finally:
            self.log.exit(result=result)
