from project.cho.egest_adapter.doc.survey.survey import Survey
from project.cho.egest_adapter.doc.book.article_book import ArticleBook


class ArticleSurvey(Survey, ArticleBook):  # left to right order important!
    pass
