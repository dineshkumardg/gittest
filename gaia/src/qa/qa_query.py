import urllib
from gaia.search.query import Query
from qa.qa_link import QaLink
from qa.models import Item


class QaQuery(Query):

    def find_items(self, search_expression, search_parameters):
        ''' return a set of Items matching a search expression with search_parameters (NOT a full query)
            Note: Only items that are still in QA status will be returned.

            eg find_items('title:Japan', 'fl=title')
        '''

        params = {'fl': QaLink.field_name,
                  'rows': '9999999', }

        search_parameters.update(params)   # replace any existing rows parameter with our new one, and limit the number of returned fields to just the one we need.
        query = '%s&%s' % (search_expression, urllib.urlencode(search_parameters))
        matches, num_found = self.find(query)

        items = set()
        for match in matches:
            url, item_index_id, chunk_index_id, page_index_id = QaLink.link_info(match)
            item = Item.objects.get(id=item_index_id)

            # Note: we may add the ability to reject items in other states (eg ready_for_release, exported)
            if item.is_live and item.in_qa():
                items.add(item)

        return list(items)
