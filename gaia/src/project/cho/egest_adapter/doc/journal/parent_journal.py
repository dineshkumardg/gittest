from project.cho.egest_adapter.doc.journal.journal import Journal
from project.cho.egest_adapter.doc.book.parent_book import ParentBook


class ParentJournal(Journal, ParentBook):  # left to right order important!
    pass
