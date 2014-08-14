import gaia.dom.adapter.factory
import project.cho.gaia_dom_adapter.cho

# binx 	Journal 	Bulletin of International News
# diax 	Journal 	Documents of International Affairs
# iaxx 	Journal 	International Affairs
# siax 	Journal 	Survey of International Affairs
# wtxx 	Journal 	World Today
# meet 	Meeting 	Meetings
# bcrc 	Monograph 	British Commonwealth Relations Conference
# chbp 	Monograph 	Chatham House Briefing Papers
# chrx 	Monograph 	Chatham House Reports
# dsca 	Monograph 	Documents and Speeches on Commonwealth Affairs
# iprx 	Monograph 	Institute of Pacific Relations
# rsxx 	Monograph 	Refugee Survey
# rwax 	Monograph 	Report on World Affairs
# rfpx 	Monograph 	Review of the Foreign Press
# rdpx 	Monograph 	RIIA Discussion Papers
# rpax 	Monograph 	RIIA Pamphlets
# sbca 	Monograph 	Survey of British Commonwealth Affairs


class Factory(gaia.dom.adapter.factory.Factory):
    ' return a suitable CHO Gaia DOM Adapter _class_ for a file name. '# a class factory not an object factory
    _adapters = {'any': project.cho.gaia_dom_adapter.cho.Cho, }
    #_adapters = {'iaxx': project.cho.gaia_dom_adapter.journal.Journal,
                 #'binx': project.cho.gaia_dom_adapter.journal.Journal,
                 ##'diax': project.cho.gaia_dom_adapter.journal.Journal,
                 #'siax': project.cho.gaia_dom_adapter.journal.Journal,
                 #'wtxx': project.cho.gaia_dom_adapter.journal.Journal,
                 #'meet': project.cho.gaia_dom_adapter.meeting.Meeting,
                 ## monographs?
                #}
    
    @classmethod
    def _adapter_type(cls, fname):
        ' return a project-specific key (eg a document type) to lookup an adapter.'
        return 'any'

        #try:
            #return fname.split('_')[1]
        #except Exception, e:
            #raise GaiaError('invalid file name for the Chatham House project.', file_name=fname, error=e)
