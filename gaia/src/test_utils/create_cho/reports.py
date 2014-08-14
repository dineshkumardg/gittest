rpax_head = '''<?xml version="1.0" encoding="utf-8"?>
<!--
    xsi:noNamespaceSchemaLocation="../../../../gaia/config/dtds/chatham_house.xsd"
 -->
<chapter contentType="book"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <metadataInfo>
        <PSMID>%s</PSMID>
        <assetID>AAA123456789</assetID>
        <mcode>1234</mcode>
        <language ocr="English" primary="Yes">English</language>
        <productContentType>Pamphlets and Reports</productContentType>
        <contentDate>
            <contentComposed>1943</contentComposed>
            <contentDecade>1940-1949</contentDecade>
            <contentYear>1943</contentYear>
            <contentMonth>November</contentMonth>
            <contentDateStart>1943-11-01</contentDateStart>
            <contentDateEnd>1943-11-30</contentDateEnd>
        </contentDate>
        <chathamHouseRule>No</chathamHouseRule>
        <ocr>52.36</ocr>
        <isbn length="10">1234567890</isbn>
        <sourceLibrary>
            <libraryName>Chatham House</libraryName>
            <libraryLocation>London, UK</libraryLocation>
            <copyrightStatement>Copyright Statement</copyrightStatement>
        </sourceLibrary>
    </metadataInfo>
    <citation>
        <book>
            <pubDate>
                <composed>November 1943</composed>
                <year>1943</year>
                <month>November</month>
                <pubDateStart>1943-11-01</pubDateStart>
                <pubDateEnd>1943-11-30</pubDateEnd>
            </pubDate>
            <seriesGroup>
                <seriesTitle>Information Notes</seriesTitle>
                <seriesNumber>1</seriesNumber>
            </seriesGroup>
            <titleGroup>
                <fullTitle>fullTitle for %s</fullTitle>
            </titleGroup>
            <editionNumber>2</editionNumber>
            <imprint>
                <imprintFull>The Broadwater Press</imprintFull>
                <imprintPublisher>The Broadwater Press</imprintPublisher>
            </imprint>
            <publicationPlace>
                <publicationPlaceCity>Welwyn</publicationPlaceCity>
                <publicationPlaceState>Hertfordshire</publicationPlaceState>
                <publicationPlaceComposed>Welwyn, Hertfordshire</publicationPlaceComposed>
            </publicationPlace>
            <totalPages>%s</totalPages>
        </book>
    </citation>
'''
rpax_mid = '''<page id="%s" type="front_matter" firstPage="Yes">
        <pageImage pageIndicator="single" width="2460" height="4385"
            type="jpeg" colorimage="color" pagePosition="left">%s</pageImage>
        <sourcePage>%s</sourcePage>
        <assetID>BBB123456789</assetID>
        <article id="%s" type="front_matter" level="1">
            <clip pgref="%s" />
            <illustration pgref="0001" type="chart" colorimage="color">
                <caption>Caption # %s</caption>
            </illustration>
            <articleInfo>
                <assetID>CCC123456789</assetID>
                <title>Title # %s</title>
                <language ocr="english" primary="Yes">English</language>
                <ocr>99.99</ocr>
                <pageCount>%s</pageCount>
                <pageRange>1-%s</pageRange>
            </articleInfo>
            <text>
                <textclip>
                    <articlePage pgref="1" />
                    <relatedDocument type="article" docref="%s" pgref="0005" assetID="AAA12345678" articleref="3">Survey pp.5</relatedDocument>
                    <p>
                        <word pos="45, 60, 47, 50">Front</word>
                        <word pos="47, 60, 49, 50">matter</word>
                    </p>
                    <footnote>
                        <word pos="45, 45, 45, 45">WORD</word>
                    </footnote>
                </textclip>
            </text>
        </article>
    </page>
'''
rpax_tail = '''</chapter>
'''
