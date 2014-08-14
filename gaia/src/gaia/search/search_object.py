from abc import ABCMeta

class SearchObject:
    __metaclass__ = ABCMeta

    def __init__(self, search_id, search_info, qa_link):
        self.search_id = search_id
        self.search_info = search_info
        self.qa_link = qa_link # Note: qa_link is a qa.qa_link object

        # TODO: push qa info into info?...
