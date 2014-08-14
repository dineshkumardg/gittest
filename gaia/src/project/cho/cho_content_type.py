class ChoContentType:
    ''' Would have liked to call this Cho but one of the users of it is also called Cho, and python doesn't like this! '''
    @classmethod
    def content_type(cls, chapter_citation_book_value, product_content_type):  # TODO instead of returning strings return some sort enum?
        if product_content_type in ['Books', 'Survey and Documents Series', 'Pamphlets and Reports', ]:
            return 'book'
        elif product_content_type == 'Meetings':
            return 'meeting'
        elif product_content_type == 'Journals':
            return 'journal'
        elif product_content_type == 'Conference Series':
            return 'conference'
        elif product_content_type == 'Special Publications':
            # in this one case, there are 2 possible options, only one of which will exist.
            if chapter_citation_book_value is not None:
                return 'book'
            else:
                return 'journal'
        else:
            return None
