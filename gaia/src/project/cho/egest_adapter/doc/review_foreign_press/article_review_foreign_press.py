from project.cho.egest_adapter.doc.review_foreign_press.review_foreign_press import ReviewForeignPress
from project.cho.egest_adapter.doc.book.article_book import ArticleBook


class ArticleReviewForeignPress(ReviewForeignPress, ArticleBook):
    def _meta_descriptive_indexing(self, document_instance):
        return self.meta_descriptive_indexing(document_instance, '21819391', 'Journal')
