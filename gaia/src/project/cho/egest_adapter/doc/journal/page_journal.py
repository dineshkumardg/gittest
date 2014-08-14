from project.cho.egest_adapter.doc.journal.journal import Journal
from project.cho.egest_adapter.doc.book.page_book import PageBook


class PageJournal(Journal, PageBook):  # left to right order important!
    pass
