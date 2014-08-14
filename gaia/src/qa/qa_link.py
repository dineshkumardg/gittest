import django.core.urlresolvers
from gaia.error import GaiaCodingError


class QaLink:
    ''' This holds the information necessary to back-link to a specific page in the QA App

        Use this class to put info into a dictionary then extract that info later as a url.
        (used by Search).
    '''
    field_name = '_gaia_qa_link'

    def __init__(self, item_index_id, chunk_index_id, first_page_index_id):
        # Note: we don't use all this info currently, but we'll need it if
        # we want to link to the chunk page, so I'm including it now so that
        # it gets into the search db.

        self.item_index_id = str(item_index_id)
        self.chunk_index_id = str(chunk_index_id)
        self.first_page_index_id = str(first_page_index_id)
 
    def decorate_info(self, info):
        ' add link data into the info dictionary. '
        info[self.field_name] = '|'.join([self.item_index_id, self.chunk_index_id, self.first_page_index_id])

    @staticmethod
    def link_info(info):
        ''' return a link built from data inserted into the info dict by the decorate method,
            together with other qa-based link information.

            NOTE: This has the side-effect of REMOVING the data from the info dict.
        '''
        # at the moment, we link back to the Page view (maybe want the Chunk view later?)
        try:
            item_id, chunk_id, page_id = info[QaLink.field_name].split('|')
            url = django.core.urlresolvers.reverse('page', args=[page_id,])
            #url = django.core.urlresolvers.reverse('chunk', args=[item_id, chunk_id])
            del info[QaLink.field_name]

            return url, item_id, chunk_id, page_id
        except KeyError, e:
            raise GaiaCodingError('missing "%s" key from info dict!' % QaLink.field_name, info=info)
