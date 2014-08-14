from project.cho.egest_adapter.doc.survey.survey import Survey
from project.cho.egest_adapter.doc.book.page_book import PageBook


class PageSurvey(Survey, PageBook):  # left to right order important!
    pass
