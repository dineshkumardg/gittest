meet_head = '''<?xml version="1.0" encoding="utf-8"?>
<!--
    xsi:noNamespaceSchemaLocation="../../../../gaia/config/dtds/chatham_house.xsd"
 -->
<chapter contentType="speech"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <metadataInfo>
        <PSMID>%s</PSMID>
        <assetID>MMM123456789</assetID>
        <mcode>1234</mcode>
        <language ocr="English" primary="Yes">English</language>
        <productContentType>Meetings</productContentType>
        <contentDate>
            <contentComposed>1968</contentComposed>
            <contentDecade>2000-2010</contentDecade>
            <contentIrregular>contentIrregular</contentIrregular>
            <contentYear>1968</contentYear>
            <contentMonth>04</contentMonth>
            <contentDay>01</contentDay>
            <contentDateStart>2002-08-24</contentDateStart>
            <contentDateEnd>2002-09-25</contentDateEnd>
        </contentDate>
        <chathamHouseRule>Yes</chathamHouseRule>
        <ocr>75.60</ocr>
        <isbn length='10'>1234567890</isbn>
        <issn>12345678</issn>
        <sourceLibrary>
            <libraryName>Chatham House</libraryName>
            <libraryLocation>London, UK</libraryLocation>
            <copyrightStatement>Copyright Statement</copyrightStatement>
        </sourceLibrary>
    </metadataInfo>
    <citation>
        <meeting>
            <pubDate>
                <composed>January 1963</composed>
                <irregular>irregular</irregular>
                <century>century</century>
                <year>1837</year>
                <month>05</month>
                <day>06</day>
                <dayofweek>Monday</dayofweek>
                <pubDateStart>1963-01-01</pubDateStart>
                <pubDateEnd>1963-01-31</pubDateEnd>
            </pubDate>
            <author role="author">
                <aucomposed>MR LEO LOVELL</aucomposed>
                <prefix>MR</prefix>
                <first>Leo</first>
                <last>Lovell</last>
            </author>
            <titleGroup>
                <fullTitle>fullTitle for %s</fullTitle>
            </titleGroup>
            <meetingGroup>
                <meetingNumber>RIIA/8/3174</meetingNumber>
                <meetingLocation>Chatham House, London, UK</meetingLocation>
                <meetingType>Speech</meetingType>
            </meetingGroup>
            <totalPages>%s</totalPages>
        </meeting>
    </citation>
'''
meet_head_related_media = '''<?xml version="1.0" encoding="utf-8"?>
<!--
    xsi:noNamespaceSchemaLocation="../../../../gaia/config/dtds/chatham_house.xsd"
 -->
<chapter contentType="speech"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <metadataInfo>
        <PSMID>%s</PSMID>
        <assetID>MMM123456789</assetID>
        <mcode>1234</mcode>
        <language ocr="English" primary="Yes">English</language>
        <productContentType>Meetings</productContentType>
        <contentDate>
            <contentComposed>1968</contentComposed>
            <contentDecade>2000-2010</contentDecade>
            <contentIrregular>contentIrregular</contentIrregular>
            <contentYear>1968</contentYear>
            <contentMonth>04</contentMonth>
            <contentDay>01</contentDay>
            <contentDateStart>2002-08-24</contentDateStart>
            <contentDateEnd>2002-09-25</contentDateEnd>
        </contentDate>
        <chathamHouseRule>Yes</chathamHouseRule>
        <ocr>75.60</ocr>
        <isbn length='10'>1234567890</isbn>
        <issn>12345678</issn>
        <sourceLibrary>
            <libraryName>Chatham House</libraryName>
            <libraryLocation>London, UK</libraryLocation>
            <copyrightStatement>Copyright Statement</copyrightStatement>
        </sourceLibrary>
        <relatedMedia id="%s" mediaType="%s" dataType="%s" duration="12.34" assetID=""/>
    </metadataInfo>
    <citation>
        <meeting>
            <pubDate>
                <composed>January 1963</composed>
                <irregular>irregular</irregular>
                <century>century</century>
                <year>1837</year>
                <month>05</month>
                <day>06</day>
                <dayofweek>Monday</dayofweek>
                <pubDateStart>1963-01-01</pubDateStart>
                <pubDateEnd>1963-01-31</pubDateEnd>
            </pubDate>
            <author role="author">
                <aucomposed>MR LEO LOVELL</aucomposed>
                <prefix>MR</prefix>
                <first>Leo</first>
                <last>Lovell</last>
            </author>
            <titleGroup>
                <fullTitle>fullTitle for %s</fullTitle>
            </titleGroup>
            <meetingGroup>
                <meetingNumber>RIIA/8/3174</meetingNumber>
                <meetingLocation>Chatham House, London, UK</meetingLocation>
                <meetingType>Speech</meetingType>
            </meetingGroup>
            <totalPages>%s</totalPages>
        </meeting>
    </citation>
'''
meet_page_01_header = '''<page id="%s" firstPage="Yes" type="body_page">
        <pageImage pageIndicator="single" width="2460" height="4385" type="jpeg" colorimage="color" pagePosition="stand_alone">%s</pageImage>
        <sourcePage>1</sourcePage>
        <article id="%s" type="article" level="1">
'''
meet_page_01_clip = '''            <clip pgref="%s" clipref="%s" />
'''
meet_page_01_articleInfo = '''        <articleInfo>
                <assetID>OOO123456789</assetID>
                <language ocr="english" primary="Yes">English</language>
                <ocr>77.77</ocr>
                <pageCount>%s</pageCount>
            </articleInfo>
            <text>
'''
meet_page_01_textclip = '''<textclip>
                    <articlePage pgref="%s" clipref="%s">%s</articlePage>
                    <p>
                        <word pos="15, 60, 47, 50">James</word>
                        <word pos="25, 60, 47, 50">was</word>
                        <word pos="35, 60, 47, 50">here </word>
                        <word pos="45, 60, 47, 50">%s</word>
                        <word pos="15, 60, 47, 51">quote: &quot;</word>
                        <word pos="25, 60, 47, 52">amp: &amp;</word>
                        <word pos="35, 60, 47, 53">apos: &apos;</word>
                        <word pos="45, 60, 47, 54">less than: &lt;</word>
                        <word pos="45, 60, 47, 54">greater than:&gt;</word>
                        <word pos="15, 60, 47, 56">quote: &quot; :quote</word>
                        <word pos="25, 60, 47, 56">amp: &amp; :amp</word>
                        <word pos="35, 60, 47, 57">apos: &apos; :apos</word>
                        <word pos="45, 60, 47, 58">less than: &lt; :less than</word>
                        <word pos="45, 60, 47, 59">greater than: &gt; :greater than</word>
                    </p>
                </textclip>
'''
meet_page_01_footer = '''</text>
        </article>
    </page>
'''
meet_mid_0n = '''<page id="%s" firstPage="No" type="body_page">
        <pageImage pageIndicator="single" width="2460" height="4385" type="jpeg" colorimage="color" pagePosition="stand_alone">%s</pageImage>
        <sourcePage>%s</sourcePage>
    </page>
'''
meet_tail = '''</chapter>
'''
