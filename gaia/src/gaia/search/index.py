import json
import httplib
import urllib
from gaia.search.search_error import SearchError
from gaia.log.log import Log


class SearchRequestFailed(SearchError):
    pass


class Index:
    ''' This represents the Gaia Search Index.

        You can add and delete search objects to the Index
        and then do queries against objects in the Index.
    '''

    def __init__(self, server):
        ''' WARNING: The server MUST NOT have the http:// prefix!

            eg server='localhost:8983'
        '''
        self.server = server
        self._log = Log.get_logger(self)

    def add(self, search_object):
        ''' Add (or replace) one search object to the Search Index.
        '''
        self._log.enter(search_object=search_object)

        search_id = search_object.search_id
        search_info = search_object.search_info

        solr_doc = search_info  # Q. do we need to copy here?
        solr_doc['id'] = str(search_id)

        cmd = {'add':  {'doc': solr_doc,
                        'commitWithin': 10000,   # do a commit within 10 seconds (instead of an explicit commit)
                        'overwrite': True}, # any new version replaces the older version
               #'commit': {},   # force to commit immediately, but this causes problems with ServiceUnavailable (maxWarmingSearchers not warming up quickly enough)
               #'optimize': {'waitFlush': False, 'waitSearcher': False} # slow!
              }

        data = json.dumps(cmd)

        try:
            self._solr_send(data)

            self._log.info('search index: added (or replaced):', id=search_id, info=search_info)
        except Exception, e: # socket.error, gaierror, etc!
            #self._log.debug('e="%s"' % e)
            #raise SearchError('Could not add information to the search index', search_id=search_id, search_info=search_info, error=e)
            raise SearchError('Could not add information to the search index', search_id=search_id, error=e)
        finally:
            self._log.exit()

    def delete(self, search_id):
        ''' Remove one search object from the Search Index.
        '''
        #TODO: allow many...?
        # Note: This does a Solr "delete by id" (there is also "delete by query" ref: http://wiki.apache.org/solr/UpdateXmlMessages#A.22delete.22_documents_by_ID_and_by_Query )
        self._log.enter(search_id=search_id)

        cmd = {'delete':  {'id': search_id,
                           'commitWithin': 10000},
               #'commit': {}, 
               }
        data = json.dumps(cmd)

        try:
            self._solr_send(data)

            self._log.info('search index: DELETED:', id=search_id)
        except Exception, e: # socket.error, gaierror, etc!
            self._log.debug('e="%s"' % e)
            raise SearchError('Could not delete information from the search index', search_id=search_id, error=e)
        finally:
            self._log.exit()

    def _solr_send(self, data):
        h = httplib.HTTPConnection(self.server)
        headers = {'Content-type': 'application/json',}
        h.request('POST', '/solr/update?commit=true?wt=python', data, headers)

        r = h.getresponse()
        self._log.debug('status="%s", reason="%s", msg="%s"' % (r.status, r.reason, r.msg))

        #TODO: process response?
        if r.status != 200: # == OK
            if r.status == 400:
                solr_response = eval(r.read())  # WARNING: this is dangerous, but ok for now. (convert wt=python response msg to a python dict)
                msg = solr_response['error']['msg']
                code = solr_response['error']['code']
                raise SearchRequestFailed(error=msg, solr_code=code)
            else:
                raise SearchRequestFailed(http_status=r.status, http_reason=r.reason)


    def _DO_NOT_USE_status(self):
        data = urllib.urlencode({'q': 'Status'})

        try:
            h = httplib.HTTPConnection(self.server)
            headers = {'Content-type': 'application/json',}
            h.request('POST', '/solr/update?commit=true?wt=python', data, headers)
            r = h.getresponse()
            #TODO: process response
            print r.status
            print r.reason
            print r.read()
        except Exception, e: # socket.error, gaierror, etc!
            #raise SearchError('Could not add information to the search index', search_id=search_id, search_info=search_info, error=e)
            raise SearchError('Could not get the status of the index server!', error=e)
