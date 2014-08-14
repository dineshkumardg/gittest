from gaia.utils.image_attributes import TiffImageAttributes, JpegImageAttributes
import project.cho.gaia_dom_adapter.factory
import project.stha.gaia_dom_adapter.factory


class CHOProject:
    ''' Chatham House LIVE PRODUCTION settings '''
    transfer_batch_size = 1500000000  # roughly 1.5Gb (1Gb = 1 073 741 824) (LST max is 2Gb, but we must stay below that limit)
    project_code = 'cho'
    content_set_name = 'CHOA'  # for images only
    av_content_set_name = 'CHOM'  # for mp3 audio files (and potentially video too)
    schema_name = 'chatham_house.xsd'
    dom_adapter_factory = project.cho.gaia_dom_adapter.factory.Factory

    image_file_ext = 'jpg'
    image_attrs = [JpegImageAttributes(300, 8), ]

    # Mon 15 April 2013: changed to handle data from hard drives now.
    content_providers = {'htc': {'server': 'clemea.htcindia.com', 'uid': 'clemea-gaia', 'pwd': 'CL3m3@123'},
                         # 'cengage': {'server': '127.0.0.1', 'uid': 'data_services', 'pwd': 'data_services'},  # is this password right?? (needs to be better strength!)
                        }

    max_requests_outstanding = 8  # should match number of running ingest workers.

    # time in seconds after which to assume responses are lost and to re-try (we assume a 1000 item ingest)
    response_threshold = 8 * 60 * 60  # 8 hours (in seconds) (This is important to avoid duplication in feed files)

    #poll_interval = 30 * 60 # delay (in seconds) before the Ingest Manager gets new jobs from providers (30 mins)
    poll_interval = 10 * 60  # delay (in seconds) before the Ingest Manager gets new jobs from providers (10 mins)

    retry_counter = 60  # no.of retrys
    retry_timer = 60  # time interval between each retry
    # Egest settings
    # WARNING! LIVE FTP Servers!
    #egest adapters are configured as a list of 2-tuples: class-name and parameters for that class.
    egest_adapters = [('project.cho.egest_adapter.cho_xml_adapter.ChoXmlAdapter',
                       {'server': '127.0.0.1', 'uid': 'lst_uat', 'pwd': 'lst_uat', 'initial_dir': '/', 'retry_counter': retry_counter, 'retry_timer': retry_timer}),

                      ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter',
                       {'server': 'callistoftp.ggsrv.com', 'uid': 'calftp', 'pwd': 'copy$img', 'initial_dir': '/data', 'retry_counter': retry_counter, 'retry_timer':retry_timer, }),    # WARNING: LIVE SETTINGS!
                      ]

    egest_max_requests_outstanding = 8  # # of running workers.
    # seconds after which Egest mgr assume responses are lost and to re-try (we assume a 1000 item egest)
    egest_response_threshold = 4 * 60 * 60  # 4 hours (in seconds)
    egest_poll_interval = 1 * 30  # seconds before the Egest mgr polls database for new jobs

    # http://stackoverflow.com/questions/7046979/telnet-to-locahost-refused-but-via-ip-works < also applies to refulsa on dns name
    search_server = '0.0.0.0:8983'    # IMPORTANT: do *NOT* include the http:// !!!
    qa_server = '0.0.0.0:8004'   # ukandgaia07 with port 8004 (for historical reasons)


class UAT_CHOProject(CHOProject):
    ''' User Acceptance Testing settings for CHO

        WARNING: usee LIVE HTC server (to help them test)
        TODO: test on callisto? test on gale feed parking dev area (xml)
    '''
    content_set_name = 'GAIA_TEST'  # We're now using a special "test" content set on the ***LIVE CALLISTO SERVER***
    av_content_set_name = 'MP3_TEST'  # for mp3 audio files

    # moved from 1 to 10 workers.
    max_requests_outstanding = 8  # should match number of running workers.
    egest_max_requests_outstanding = 8  # # of running workers.

    #poll_interval = 3 * 60 # delay (in seconds) before the Ingest Manager gets new jobs from providers (30 mins) #TMP 3 mins..to debug!

    # Note: we cannot load into LST Dev until we are allocating real asset ids.
    egest_adapters = [('project.cho.egest_adapter.cho_xml_adapter.ChoXmlAdapter',
                       {'server': '127.0.0.1', 'uid': 'lst_uat', 'pwd': 'lst_uat', 'initial_dir': '/', }),  # FOR UAT ONLY

                      ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter',
                       #{'server': '127.0.0.1', 'uid': 'callisto_uat', 'pwd': 'callisto_uat', 'initial_dir': '/', }),  # FOR UAT ONLY (internal EMEA ftp site on ukandgaia07)
                       #WARNING: testing ****LIVE CALLISTO**** upload!!!!
                       {'server': 'callistoftp.ggsrv.com', 'uid': 'calftp', 'pwd': 'copy$img', 'initial_dir': '/data', }),  # WARNING: LIVE Callisto SETTINGS!
                      ]

    # TUSH: 24th Jan: TMP: comment OUT HTC so that cengae (13 items) can be pulled in): for Rose.
    content_providers = {'htc': {'server': 'clemea.htcindia.com', 'uid': 'clemea-gaia', 'pwd': 'CL3m3@123'},
                         #'cengage': {'server': '127.0.0.1', 'uid': 'data_services', 'pwd': 'data_services'}, # is this password right?? (needs to be better strength!)
                        }


class TDAProject():
    ' parameters for the TDA (Times Digital Archive) project '
    project_code = '0FFO'
    content_set_name = 'LT'
    schema_name = 'EMEA_newspaper_0FFO.dtd'

    image_file_ext = 'tif'
    image_attrs = [TiffImageAttributes(300, 1), ]

    content_providers = {}
    dom_adapter_factory = None  # TODO

    # Ingest Manager settings
    max_requests_outstanding = 8  # only allow this many outstanding requests (basic throttling)
    response_threshold = 5 * 60  # time in seconds after which to assume responses are lost and to re-try
    poll_interval = 60 * 60  # Interval between polling providers in seconds

    categories = [
            'Arts and Entertainment',
            'Births',
            'Business and Finance',
            'Business Appointments',
            'Classified Advertising',
            'Court and Social',
            'Deaths',
            'Display Advertising',
            'Editorials/Leaders',
            'Feature Articles (aka Opinion)',
            'Index',
            'Law',
            'Letters to the Editor',
            'Marriages',
            'News',
            'News in Brief',
            'Obituaries',
            'Official Appointments and Notices',
            'Picture Gallery',
            'Politics and Parliament',
            'Property',
            'Publication Matter',
            'Reviews',
            'Sport',
            'Stock Exchange Tables',
            'Weather',
        ]

    illustration_types = [
            'Cartoons',
            'Drawing-Painting',
            'Graph',
            'Map',
            'Photograph',
            'Table',
        ]


class STHAProject:
    ' Sunday Times Project settings'
    project_code = 'STHA'
    content_set_name = 'STHA'
    av_content_set_name = None  # NO AV CONTENT in STHA
    schema_name = 'EMEA_newspaper_STHA.dtd'

    image_file_ext = 'tif'
    image_attrs = [TiffImageAttributes(300, 1),
                    TiffImageAttributes(400, 1), ]

    content_providers = {}  # TODO
    dom_adapter_factory = project.stha.gaia_dom_adapter.factory.Factory

    search_adapter_class_name = 'project.stha.search_adapter.stha_search_adapter.SthaSearchAdapter'

    # Ingest Manager settings
    max_requests_outstanding = 8  # only allow this many outstanding requests (basic throttling)
    response_threshold = 5 * 60  # time in seconds after which to assume responses are lost and to re-try
    poll_interval = 60 * 60  # Interval between polling providers in seconds
    search_server = '127.0.0.1:8983'  # IMPORTANT: do *NOT* include the http:// !!!

    categories = [
            'Arts, Literature and Entertainment',
            'Births, Deaths and Marriages',
            'Business, Finance and Markets',
            'Classified Advertising',
            'Contents',
            'Court and Society',
            'Display Advertising',
            'Editorials and Leaders',
            'Feature Articles',
            'Insight',
            'Law and Crime',
            'Letters and Correspondence',
            'News',
            'Obituaries',
            'Picture Gallery',
            'Poems',
            'Publication Matter',
            'Sport',
            'Weather',
        ]

    illustration_types = [
            'Cartoons',
            'Drawing-Painting',
            'Graph',
            'Map',
            'Photograph',
            'Table',
        ]


class FTProject:
    project_code = 'FTDA'
    content_set_name = 'FTIM'
    av_content_set_name = None  # NO AV CONTENT in FT
    schema_name = 'EMEA_newspaper_v16.dtd'

    image_file_ext = 'JPG'  # note: is caps (due to legacy specs)! :(
    image_attrs = [JpegImageAttributes(400, 8), ]    # Note: should be 60% but are not, so no check for quality

    content_providers = {}

    # Ingest Manager settings
    max_requests_outstanding = 8  # only allow this many outstanding requests (basic throttling)
    response_threshold = 5 * 60  # time in seconds after which to assume responses are lost and to re-try
    poll_interval = 60 * 60  # Interval between polling providers in seconds
    dom_adapter_factory = None  # TODO

    categories = [
            'Arts and Entertainment',    
            'Births, Deaths and Marriages',
            'Business and Finance',
            'Business Appointments',
            'Classified Advertising',
            'Commodity Prices',
            'Contents',
            'Display Advertising',
            'Editorials and Leaders',
            'Feature Articles',
            'Front matter',
            'Letters to the Editor',
            'Lex Column',
            'Lombard Column',
            'Management News',
            'Market News',
            'Mining News',
            'Money Markets',
            'News',
            'News in Brief',
            'Obituaries',
            'Observer Column',
            'Official Appointments',
            'Politics and Parliament',
            'Reviews',
            'Science and Technology',
            'Special Reports, Surveys and Supplements',
            'Sport',
            'Stock Exchange, Pricing and Foreign Exchange Tables',
            'Tombstone',
            'Travel',
            'Weather'
        ]

    illustration_types = [
            'Cartoons',
            'Drawing-Painting',
            'Graph',
            'Map',
            'Photograph',
            'Table',
        ]


class _BasicDevProject:
    ' Use this to set normal, "plain development (CHO-like)" settings '
    retry_counter = 60  # no.of retrys
    retry_timer = 60   # time interval between each retry
    content_providers = {'content_provider': {'server': '127.0.0.1', 'uid': 'htc', 'pwd': 'keepitunreal'}, }
    egest_adapters = [
        ('project.cho.egest_adapter.cho_xml_adapter.ChoXmlAdapter', {'server': '127.0.0.1', 'uid': 'lst', 'pwd': 'keepitunreal', 'retry_counter': retry_counter, 'retry_timer':retry_timer,}),
        ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter', {'server': '127.0.0.1', 'uid': 'callisto', 'pwd': 'keepitunreal', 'retry_counter': retry_counter, 'retry_timer':retry_timer,})]

    max_requests_outstanding = 8
    response_threshold = 60  # time in seconds after which to assume responses are lost and to re-try (1 min)
    poll_interval = 10  # delay before the Ingest Manager gets new jobs (10 secs)

    egest_max_requests_outstanding = 8  # # of running workers.
    egest_response_threshold = 120  # seconds after which Egest mgr assume responses are lost and to re-try (2 mins)
    egest_poll_interval = 30  # seconds before the Egest mgr polls database for new jobs (30 secs)

    project_code = 'cho'
    content_set_name = 'CHOA'  # for images only
    av_content_set_name = 'CHOM'  # for mp3 audio files (and potentially video too)
    schema_name = 'chatham_house.xsd'
    dom_adapter_factory = project.cho.gaia_dom_adapter.factory.Factory

    image_file_ext = 'jpg'
    image_attrs = [JpegImageAttributes(300, 8), ]  # unused? TODO: review and remove?

    search_server = '127.0.0.1:8983'  # IMPORTANT: do *NOT* include the http:// !!!
    qa_server = '127.0.0.1:8887'


class TushPcDevProject(_BasicDevProject):
    ' Tushars development settings for PC '
    content_providers = {'localhost_test_provider': {'server': '127.0.0.1', 'uid': 'tester', 'pwd': 'keepitunreal'}, }

    # THRASH settings...
    #response_threshold = 1 # time in seconds after which to assume responses are lost and to re-try (1 min) # set to THRASH!
    #poll_interval = 1       # delay before the Ingest Manager gets new jobs (10 secs)

    egest_adapters = [
        ('project.cho.egest_adapter.cho_xml_adapter.ChoXmlAdapter', {'server': '127.0.0.1', 'uid': 'tester', 'pwd': 'keepitunreal', 'initial_dir': '/LST', }),
        ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter', {'server': '127.0.0.1', 'uid': 'tester', 'pwd': 'keepitunreal', 'initial_dir': '/CALLISTO', })]


class TushNewspaperProject(STHAProject):
    ' Tushars settings for newspaper development '
    qa_server = '127.0.0.1:8887'    # TODO: push into other configs...

    content_providers = {'tush_pc': {'server': '127.0.0.1',  # 'ukandtwagle-l1.corp.local',
                                     'uid': 'tester',
                                     'pwd': 'keepitunreal'}, }
    max_requests_outstanding = 8
    response_threshold = 60  # time in seconds after which to assume responses are lost and to re-try (1 min)
    poll_interval = 10  # delay before the Ingest Manager gets new jobs (10 secs)

    # egest adapters are configured as a list of 2-tuples: class-name and parameters for that class.
    egest_adapters = [  # need a GOLD adapter here :)  TODO
          ('gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter', {'server': '127.0.0.1', 'uid': 'tush_callisto', 'pwd': 'tush_callisto', 'initial_dir': '/', })]


class TushLinuxDevProject(_BasicDevProject):
    ' Tushar development settings for Linux '
    pass


class JamesDevProject(_BasicDevProject):
    ' James development settings for Linux '
    pass
