from project.cho.egest_adapter.doc.refugee_survey.refugee_survey import RefugeeSurvey
from project.cho.egest_adapter.doc.book.article_book import ArticleBook


class ArticleRefugeeSurvey(RefugeeSurvey, ArticleBook):  # left to right order important!
    pass
