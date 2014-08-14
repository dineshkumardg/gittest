from project.cho.egest_adapter.doc.survey.survey import Survey
from project.cho.egest_adapter.doc.book.parent_book import ParentBook


class ParentSurvey(Survey, ParentBook):  # left to right order important!
    pass
