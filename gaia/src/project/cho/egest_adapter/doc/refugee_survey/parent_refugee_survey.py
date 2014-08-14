from project.cho.egest_adapter.doc.refugee_survey.refugee_survey import RefugeeSurvey
from project.cho.egest_adapter.doc.book.parent_book import ParentBook


class ParentRefugeeSurvey(RefugeeSurvey, ParentBook):  # left to right order important!
    pass
