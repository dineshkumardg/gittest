'''
The US Id Provider.

Single Fetch:
    http://nuxeo-ei.ggsrv.com/cap-rest/rest/generateId
returns:

BUYXCG519660310

    
Bulk Fetch:
    http://nuxeo-ei.ggsrv.com/cap-rest/rest/generateIds/20
returnes something like this:

<?xml version="1.0" encoding="UTF-8" standalone="yes"?><documentIds><id>OOSXKW685871004</id><id>PJEFVO023417015</id><id>CFPMDY502568169</id><id>PUWUDG320334771</id><id>NOKGLW719696995</id><id>BPEUJD760858543</id><id>EEABVB261733301</id><id>DJWFMD243752520</id><id>EZUKSO993500148</id><id>VZJRVF357326241</id><id>VBDLWT978178153</id><id>ISOYSY113268983</id><id>YPSRBQ147847154</id><id>SWPLYR145424423</id><id>WHRVUD220246109</id><id>XZACRW715053110</id><id>NFXLLN599611779</id><id>XADBOK664097261</id><id>JRVOVM111729067</id><id>EDSRLT030018634</id></documentIds>

'''
import urllib2
import socket
from lxml import etree
from gaia.log.log import Log
from gaia.error import GaiaError

class AssetIdFetchFailed(GaiaError): pass # Note can be treated as a warning or an Error

class _AssetIdProvider:
    ''' A private class that reprensents the central, US, Asset Id Service
        that is the real provider of ids.
    '''
    single_url = 'http://nuxeo-ei.ggsrv.com/cap-rest/rest/generateId'
    bulk_url   = 'http://nuxeo-ei.ggsrv.com/cap-rest/rest/generateIds' # + '/20' (eg)
    uid = 'ga1'
    pwd = 'ga1'

    def __init__(self, single_url=None, bulk_url=None, uid=None, pwd=None, timeout_seconds=60, num_retries=3):
        if single_url: self.single_url = single_url
        if bulk_url: self.bulk_url = bulk_url
        if uid: self.uid = uid
        if uid: self.pwd = pwd

        self.timeout = timeout_seconds
        self.num_retries = num_retries

        self._log = Log.get_logger(self)

    def fetch(self, how_many=1):
        ''' Fetch up to how_many ids (might get less).
            Throws AssetIdFetchFailed if none are fetchable.
        '''
        if how_many == 1:
            return self._fetch_one()
        else:
            return self._fetch_many(how_many)


    def _fetch_one(self):
        url = self.single_url
        response = self._request(url)
        return response # in tis case, the response is the plain asset id, so no need to parse :)

    def _fetch_many(self, how_many):
        url ='%s/%s'  % (self.bulk_url, how_many)
        response = self._request(url)
        ids = self._parse(response)

        if len(ids) == 0:
            raise AssetIdFetchFailed()
        else:
            return ids

    def _request(self, url):
        ''' Request Asset Ids from the centralised (US) service.

            The response is dependant on the url passed in.
            Bulk and single response have different respponse formats.
            Single requests return just tghe plain id (with no decoration)
            Bulk requests come back in an xml document.
        '''
        self._log.enter()

        response = None
        try_number = 1  # Note: we're using human-friendly numbers here (and couting up) to make the logging nicer.

        while try_number < self.num_retries + 2 and response is None:
            self._log.info('requesting Asset Ids from the US', url=url, try_number=try_number)

            try:
                password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
                password_manager.add_password(None, url, self.uid, self.pwd)
                auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
                opener = urllib2.build_opener(auth_handler)
                urllib2.install_opener(opener)

                response = urllib2.urlopen(url, timeout=self.timeout).read()

            except urllib2.HTTPError, e:
                self._log.warn('HTTP error: %d' % e.code)
            except urllib2.URLError, e:
                self._log.warn('Network error: %s' % e.reason)
            except ValueError, e:
                self._log.warn('URL error: %s' % e)
            except socket.timeout, e:
                self._log.warn('timeout: %s' % e)

            try_number += 1

        if response is None:
            self._log.warn('Asset Id fetch from US has failed.')
            self._log.exit()
            raise AssetIdFetchFailed()
        else:
            self._log.info('Got Asset Ids from US.', response=response)
            self._log.exit()
            return response

    def _parse(self, response):
        ''' parse a bulk request reqponse document into a list of asset ids.
            May return an empty list!
        '''
        self._log.enter()
        asset_ids = []

        xml = etree.fromstring(response)
        xml_asset_ids = xml.xpath('/documentIds/id')

        for xml_asset_id in xml_asset_ids:
            if len(xml_asset_id.text) > 0:  # TODO: check length == something (32?) ?
                asset_ids.append(xml_asset_id.text)

        self._log.exit('parsed asset_ids', asset_ids=asset_ids)
        return asset_ids
