from project.cho.egest_adapter.doc.meeting.mega_meeting import MegaMeeting
from project.cho.egest_adapter.doc.meeting.page_meeting import PageMeeting
from project.cho.egest_adapter.doc.report.mega_report import MegaReport
from project.cho.egest_adapter.doc.report.page_report import PageReport
from project.cho.egest_adapter.doc.book.parent_book import ParentBook
from project.cho.egest_adapter.doc.book.article_book import ArticleBook
from project.cho.egest_adapter.doc.book.page_book import PageBook
from project.cho.egest_adapter.doc.conference_series.parent_conference_series import ParentConferenceSeries
from project.cho.egest_adapter.doc.conference_series.article_conference_series import ArticleConferenceSeries
from project.cho.egest_adapter.doc.conference_series.page_conference_series import PageConferenceSeries
from project.cho.egest_adapter.doc.refugee_survey.article_refugee_survey import ArticleRefugeeSurvey
from project.cho.egest_adapter.doc.refugee_survey.page_refugee_survey import PageRefugeeSurvey
from project.cho.egest_adapter.doc.refugee_survey.parent_refugee_survey import ParentRefugeeSurvey
from project.cho.egest_adapter.doc.review_foreign_press.article_review_foreign_press import ArticleReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press.page_review_foreign_press import PageReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press.parent_review_foreign_press import ParentReviewForeignPress
from project.cho.egest_adapter.doc.journal.parent_journal import ParentJournal
from project.cho.egest_adapter.doc.journal.article_journal import ArticleJournal
from project.cho.egest_adapter.doc.journal.page_journal import PageJournal
from project.cho.egest_adapter.doc.survey.parent_survey import ParentSurvey
from project.cho.egest_adapter.doc.survey.article_survey import ArticleSurvey
from project.cho.egest_adapter.doc.survey.page_survey import PageSurvey
from project.cho.egest_adapter.doc.document_instances import DocumentInstances
from gaia.dom.document_error import DocumentError


class DocFactory():
    builders = {'Meetings': [MegaMeeting, PageMeeting],
                'Conference Series': [ParentConferenceSeries, ArticleConferenceSeries, PageConferenceSeries],
                'Pamphlets and Reports': [MegaReport, PageReport],
                'Books': [ParentBook, ArticleBook, PageBook,],
                'Special Publications/book': [ArticleRefugeeSurvey, PageRefugeeSurvey, ParentRefugeeSurvey],
                'Special Publications/journal': [ArticleReviewForeignPress, PageReviewForeignPress, ParentReviewForeignPress],
                'Journals': [ParentJournal, ArticleJournal, PageJournal],
                'Survey and Documents Series': [ParentSurvey, ArticleSurvey, PageSurvey],
               }

    @classmethod
    def _choose_builder(cls, source_xml_dict):
        choice_of_builder = source_xml_dict['/chapter/metadataInfo/productContentType']

        if choice_of_builder == 'Special Publications':
            chapter_citation_book_value = source_xml_dict['/chapter/citation/book']
            if chapter_citation_book_value is not None:
                specialisation = 'book'
            else:
                specialisation = 'journal'

            choice_of_builder = 'Special Publications/' + specialisation
        return choice_of_builder

    @classmethod
    def create(cls, config, source_xml_dict, extra_args):
        ' return an object that can create Document Instances for this type of xml '
        try:
            builders = cls.builders[cls._choose_builder(source_xml_dict)]

            return DocumentInstances(config, source_xml_dict, builders, extra_args)
        except KeyError, e:  # This is what happens if you try and egest stuff that's doesn't have a builder
            raise DocumentError('builder not available for: %s' % e.message)
