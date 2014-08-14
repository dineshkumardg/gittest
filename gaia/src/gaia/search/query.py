import urllib
from urllib2 import urlopen, URLError
from gaia.log.log import Log
from gaia.search.search_error import SearchError
from gaia.search.search_object import SearchObject
from qa.qa_link import QaLink

class Query:

    def __init__(self, search_server, search_collection):
        self.server = search_server
        self.collection = search_collection
        self._log = Log.get_logger(self)

    def _get(self, query, return_facets=False):
        ' returns num_found, index_of_first_result, page_of_matched_search_objects '
        #url = 'http://localhost:8983/solr/collection1/select?q=%s&fl=id,_version_&wt=python' % query
        #Note: might need to filter on __version__ somewhere/how # TODO
        # Or add an is_live????? (how to keep it current, etc :( )
        # Ignore for now! (TODO: when is_live changes, the search index should be updated too))
        # .. and we need to add afilter here on is_live=True
        # (Note that this is handled for now by filtering on display instead).
        query = urllib.quote(query, safe="&=") # & and = need to be passed on to Solr
        
        url = 'http://%s/solr/%s/select?q=%s&wt=python' % (self.server, self.collection, query)
        self._log.debug('search', url=url)

        try:
            str_response = self._read(url)
            full_response = eval(str_response)  # dangerous!!
            self._log.debug('search returned:', full_response=full_response)
            response = full_response['response'] # there's also a 'responseHeader' with status and QTime, etc..

            if return_facets:
                return response['numFound'], response['start'], response['docs'], response['facet_counts']
            else:
                return response['numFound'], response['start'], response['docs']
        except URLError, e: 
            raise SearchError('Cannot Analyse due to a SEARCH SERVER PROBLEM', error=e, url=url)
        except Exception, e:    # catching Exception due to the use of eval above.
            raise SearchError('unexpected general error trying to run an Analysis (search)', error=e, url=url)

    def _read(self, url):  # used to support a unit test
        return urlopen(url).read()

    def get(self, search_id):   # TODO: test
        ''' Get a search object by id (should only ever be one match)
        '''
        query = 'id:' + search_id
        num_found, start, search_objects = self._get(query)

        if num_found > 0:
            self._log.warning('Search Query found multiple matches for a get request (should only be one match)!', search_id=search_id, num_found=num_found, search_objects=search_objects)

        if num_found == 0:
            self._log.warning("didn't find any matches - possible the solr db been emptied?" , search_id=search_id, num_found=num_found, search_objects=search_objects)
            return None

        search_info = search_objects[0] # the naming is confusing/wrong, but _get() actually return dicts not Search Objects.
        search_object = SearchObject(search_info['id'], search_info, search_info[QaLink.field_name])
        return search_object

    def find(self, query):
        #url = 'http://localhost:8983/solr/collection1/select?q=%s&wt=python' % query
        # filter on a "field list" (just id in this case)
        #url = 'http://localhost:8983/solr/collection1/select?q=%s&fl=id,_version_&wt=python' % query
        num_found, start, search_objects = self._get(query)
        return search_objects, num_found

    def count(self, query):
        num_found, start, search_objects = self._get(query)
        return num_found

    def facet(self, query, facet_field):    # EXPERIMENTAL!
        ''' do a search to get a result set; then see how many of each type
            of thing there are within the search.

            The "facet_field" is the thing you're counting instances of.

            EG: do a query and then see what set of pageCounts theer are in this set of Items:
                find_and_facet(query='id:*', facet_field='pageCount'):
            might return:
                {'4':13,
                 '1':6,
                 '2':5,
                 '3':5,
                 '5':3,
                 '6':2,
                 '7':1},
              which means there are 13 matches with a pageCount of '4', 6 with '1', etc.
        '''
        # use rows=0 to JUST get facets
        # http://localhost:8983/solr/cho/select?q=id%3A*&rows=0&wt=xml&facet=true&facet.field=pageCount
        # =>
        #{'responseHeader':{'status':0,'QTime':1,'params':{'facet':'true','facet.field':'pageCount','wt':'python','q':'id:*','rows':'0'}},
        # 'response':{'numFound':61,'start':0,'docs':[]},
        # 'facet_counts':{'facet_queries':{},
        #                 'facet_fields':{'pageCount':['4',13,'1',6,'2',5,'3',5,'5',3,'6',2,'7',1]},
        #                 'facet_dates':{},
        #                 'facet_ranges':{}}
        #}

        query = query + '&rows=0&facet=true&facet.field=' + facet_field
        num_found, start, search_objects, facet_counts = self._get(query, return_facets=True)

        counts = facet_counts['facet_fields'][facet_field] 
        # this is returned as a flat list, eg ['4',13,'1',6,'2',5,'3',5,'5',3,'6',2,'7',1]
        # we'll change this into a more useful dict..
        field_counts = {}
        for i in range(0, len(counts), 2):
            field_counts[counts[i]] = counts[i+1]

        return num_found, field_counts

    #def find_and_facet(self, query, facet_field):
        # use rows=0 to JUST get facets
        # http://localhost:8983/solr/cho/select?q=id%3A*&rows=0&wt=xml&facet=true&facet.field=pageCount
        # =>
        #{'responseHeader':{'status':0,'QTime':1,'params':{'facet':'true','facet.field':'pageCount','wt':'python','q':'id:*','rows':'0'}},
        # 'response':{'numFound':61,'start':0,'docs':[]},
        # 'facet_counts':{'facet_queries':{},
        #                 'facet_fields':{'pageCount':['4',13,'1',6,'2',5,'3',5,'5',3,'6',2,'7',1]},
        #                 'facet_dates':{},
        #                 'facet_ranges':{}}
        #}

        # TODO.... 
        # query = query + 'facet=true&facet.field=' + facet_field
        #num_found, start, search_objects = self._get(query)
        #return search_objects, num_found

    ##def count(self, query):#?
        ## 'http://localhost:8983/solr/collection1/select?q=%5C%2Fcitation%5C%2Fjournal%5C%2Fauthor%5C%2Flast%3APerrygrove%0A%0A%0A&wt=python'
        #raw_xpath = '/citation/journal/author/last'
        #xpath = raw_xpath.replace(r'/', r'\/')
        #value = 'Perrygrove'
        #query = xpath + ':' + value
        #query += 'facet=true&facet.field=%s' % raw_xpath    # note: no need to baclslash?
        #query = urllib.quote_plus(query)

        ## count matches using a facet field search, eg counting /citation/joutnal/imprint/imprintPublisher
        ##http://localhost:8983/solr/collection1/select?q=*%3A*&wt=xml&facet=true&facet.field=%2Fcitation%2Fjournal%2Fimprint%2FimprintPublisher

    #def find_missing(self, dom_id, json_info): # TODO
        # get fields WITHOUT a tag at all or an empty value?
        #xpath = '-title'    # note minus
        #value = '[* TO *]'
        #query = xpath + ':' + value
        #query = urllib.quote_plus(query)

        #url = 'http://localhost:8983/solr/collection1/select?q=%s&fl=id,_version_&wt=python' % query
        #response = urllib.urlopen(url).read()
        #pprint(eval(response))  # dangerous!!

        #print "-------------------------------------------"
        # NOOO: best solution is to use _BLANK_ and search for that token.
        # get fields WITH a tag AND an empty value? # shoudl just be id=13
        #query = '-title:["" TO *]'
        #query = urllib.quote_plus(query)

        #url = 'http://localhost:8983/solr/collection1/select?q=%s&fl=id,_version_&wt=python' % query
        #print "query url=", url
        #response = urllib.urlopen(url).read()
        #pprint(eval(response))  # dangerous!!
