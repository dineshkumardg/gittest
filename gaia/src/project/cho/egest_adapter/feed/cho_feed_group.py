
class ChoFeedGroup:
    ''' This is really Atlas info, the atlas id number below should be the real key.
        Functional Type             Functional ID   Product content type
        ---------------             -------------   --------------------
        Megametadocument            14214546        Meetings, Pamphlets and Reports
        Page view                   14214549        Meetings, Pamphlets and Reports
        Issue-volume record         21787859        Everything Else
        Issue-volume page record    21787857        Everything Else
        Issue-volume article record 21787856        Everything Else
    '''
    MEETING_MEGA = 'meeting_mega'
    MEETING_PAGE = 'meeting_page'
    ISSUE        = 'issue'  # aka 'PARENT' in data services terminology
    PAGE         = 'page'
    ARTICLE      = 'article'

    @classmethod
    def is_indexed(cls, group):
        if group == cls.MEETING_MEGA or group == cls.ARTICLE:
            return True # Meeting megadocuments and "newspaper" articles  are indexed
        else:
            return False # everything else is not indexed

    @classmethod
    def groups(cls):
        return [cls.MEETING_MEGA, cls.MEETING_PAGE, cls.ISSUE, cls.PAGE, cls.ARTICLE]
