import collections
from gaia.log.log import Log


class ValidationRules:
    def __init__(self):
        self._log = Log.get_logger(self)
        self.errors = []

    def _get_psmid(self, xml_tree):
        psmid = xml_tree.xpath('/chapter/metadataInfo/PSMID')
        self._log.info(psmd=psmid[0].text)
        return psmid

    def _get_duplicate_pgrefs(self, pgrefs):
        return sorted([int(x) for (x, y) in collections.Counter(pgrefs).items() if y > 1])

    def _are_pgrefs_duplicated(self, xml_tree, xpath, _print):
        for page_index in range(1, int(xml_tree.xpath('count(/chapter/page)')) + 1):
            for article_index in range(1, int(xml_tree.xpath('count(/chapter/page[%s]/article)' % page_index)) + 1):
                duplicate_pgrefs = self._get_duplicate_pgrefs(xml_tree.xpath(xpath % (page_index, article_index)))
                if len(duplicate_pgrefs) > 0:
                    self._log_pgrefs_duplicated(_print, xml_tree, page_index, article_index, duplicate_pgrefs)

        return self._are_any_errors()

    def _record_error(self, _print, error):
        self.errors.append(error)
        self._log.debug(error=error)
        if _print is True:
            print error

    def _log_pgrefs_duplicated(self, _print, xml_tree, page_index, article_index, duplicate_pgrefs):
        psmid = self._get_psmid(xml_tree)
        error = '%s|%s|%s|%s' % (psmid[0].text, page_index, article_index, duplicate_pgrefs)
        self._record_error(_print, error)

    def _log_clip_pgrefs_articlepage_pgrefs_not_matching(self, _print, xml_tree, page_index, article_index, clip_pgrefs, articlepage_pgrefs):
        psmid = self._get_psmid(xml_tree)
        error = '%s|%s|%s|%s|%s' % (psmid[0].text, page_index, article_index, clip_pgrefs, articlepage_pgrefs)
        self._record_error(_print, error)

    def _log_dangling_illustration_pgrefs(self, _print, xml_tree, page_index, article_index, dangling_illustration_pgrefs):
        psmid = self._get_psmid(xml_tree)
        error = '%s|%s|%s|%s' % (psmid[0].text, page_index, article_index, dangling_illustration_pgrefs)
        self._record_error(_print, error)

    def _are_any_errors(self):
        if self.errors == []:
            return True
        else:
            return False

    def are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(self, xml_tree, _print=False):
        return self._are_pgrefs_duplicated(xml_tree, '/chapter/page[%s]/article[%s]/text/textclip/articlePage/@pgref', _print)

    def are_chapter_page_article_clip_pgrefs_unique(self, xml_tree, xpath='/chapter/page[%s]/article[%s]/clip/@pgref', _print=False):
        return self._are_pgrefs_duplicated(xml_tree, '/chapter/page[%s]/article[%s]/clip/@pgref', _print)

    def are_clip_pgrefs_matching_articlepage_pgrefs(self, xml_tree, _print=False):
        for page_index in range(1, int(xml_tree.xpath('count(/chapter/page)')) + 1):
            for article_index in range(1, int(xml_tree.xpath('count(/chapter/page[%s]/article)' % page_index)) + 1):
                clip_pgrefs = xml_tree.xpath('/chapter/page[%s]/article[%s]/clip/@pgref' % (page_index, article_index))
                articlepage_pgrefs = xml_tree.xpath('/chapter/page[%s]/article[%s]/text/textclip/articlePage/@pgref' % (page_index, article_index))

                # there should not be any duplicates in clip_pgrefs or articlepage_pgrefs
                if len(self._get_duplicate_pgrefs(clip_pgrefs)) > 0 or len(self._get_duplicate_pgrefs(articlepage_pgrefs)) > 0:
                    self._log_clip_pgrefs_articlepage_pgrefs_not_matching(_print, xml_tree, page_index, article_index, clip_pgrefs, articlepage_pgrefs)

                # the sets should be the same
                if set(clip_pgrefs) != set(articlepage_pgrefs):
                    self._log_clip_pgrefs_articlepage_pgrefs_not_matching(_print, xml_tree, page_index, article_index, clip_pgrefs, articlepage_pgrefs)

        return self._are_any_errors()

    def are_illustration_pgrefs_matching_clip_pgrefs(self, xml_tree, _print=False):
        for page_index in range(1, int(xml_tree.xpath('count(/chapter/page)')) + 1):
            for article_index in range(1, int(xml_tree.xpath('count(/chapter/page[%s]/article)' % page_index)) + 1):
                clip_pgrefs = xml_tree.xpath('/chapter/page[%s]/article[%s]/clip/@pgref' % (page_index, article_index))
                illustration_pgrefs = xml_tree.xpath('/chapter/page[%s]/article[%s]/illustration/@pgref' % (page_index, article_index))

                # the illustration pgrefs must ALL exist in the clip_pgrefs
                dangling_illustration_pgrefs = set(illustration_pgrefs) - set(clip_pgrefs)
                if len(dangling_illustration_pgrefs) > 0:
                    self._log_dangling_illustration_pgrefs(_print, xml_tree, page_index, article_index, dangling_illustration_pgrefs)

        return self._are_any_errors()

    def _log_two_or_more_isbns_are_the_same_length(self, xml_tree, _print, isbns):
        psmid = self._get_psmid(xml_tree)
        error = '%s|%s' % (psmid[0].text, isbns)
        self._record_error(_print, error)

    def are_isbn_lengths_ok(self, xml_tree, _print=False):  # http://jira.cengage.com/browse/EG-533
        isbns = xml_tree.xpath('/chapter/metadataInfo/isbn/@length')
        if isbns.count('10') >= 2:
            self._log_two_or_more_isbns_are_the_same_length(xml_tree, _print, isbns)

        if isbns.count('13') >= 2:
            self._log_two_or_more_isbns_are_the_same_length(xml_tree, _print, isbns)

        return self._are_any_errors()
