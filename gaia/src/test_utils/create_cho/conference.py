# avoid db lookup
mcodes = {
    'cho_bcrc_1934_palmer_000_0000': '4XFG',
    'cho_bcrc_1933_0003_000_0000': '4XFK',
    'cho_bcrc_1933_0004_000_0000': '4XFL',
    'cho_bcrc_1934_toynbee_000_0000': '4XFH',
    'cho_bcrc_1933_0001_000_0000': '4XFN',
    'cho_bcrc_1933_0002_000_0000': '4XFO',
    'cho_bcrc_1938_0001_000_0000': '4XFS',
    'cho_bcrc_1938_0002_000_0000': '4XFT',
    'cho_bcrc_1938_0003_000_0000': '4XFV',
    'cho_bcrc_1938_0004_000_0000': '4XFW',
    'cho_bcrc_1938_0005_000_0000': '4XFX',
    'cho_bcrc_1938_0006_000_0000': '4XFY',
    'cho_bcrc_1938_0007_000_0000': '4XGR',
    'cho_bcrc_1938_0008_000_0000': '4XGS',
    'cho_bcrc_1937_cleeve_001_0000': '4XGU',
    'cho_bcrc_1938_cleeve_000_0000': '5YAH',
    'cho_bcrc_1938_cleeve_001_0000': '4XGV',
    'cho_brcr_1938_0000_000_0000': '4XGW',
    'cho_bcrc_1938_0001_001_0000': '4XGZ',
    'cho_bcrc_1938_0002_001_0000': '4XHA',
    'cho_bcrc_1938_0000_001_0000': '4XHB',
    'cho_bcrc_1945_0001_000_0000': '4XHF',
    'cho_bcrc_1945_0002_000_0000': '4XHG',
    'cho_bcrc_1945_0003_000_0000': '4XHI',
    'cho_bcrc_1949_0001_000_0000': '4XHL',
    'cho_bcrc_1949_0002_000_0000': '4XHM',
    'cho_bcrc_1949_0000_000_0000': '4XHO',
    'cho_bcrc_1954_0000_000_0000': '4XHQ',
    'cho_bcrc_1959_0001_000_0000': '4XHU',
    'cho_bcrc_1959_0002_000_0000': '4XHV',
    'cho_bcrc_1965_0000_000_0000': '4XHZ',
    'cho_bcrc_1962_0000_000_0000': '4XHX',
    'cho_iprx_1927_0000_000_0000': '4XID',
    'cho_iprx_1929_0000_000_0000': '4XIF',
    'cho_iprx_1929_0000_002_0000': '4XIG',
    'cho_iprx_1929_0000_001_0000': '4XIH',
    'cho_iprx_1931_0020_000_0000': '4XIJ',
    'cho_iprx_1931_0000_000_0000': '4XIK',
    'cho_iprx_1931_0001_000_0000': '4XIL',
    'cho_iprx_1931_0010_000_0000': '4XIU',
    'cho_iprx_1931_0011_000_0000': '4XIV',
    'cho_iprx_1931_0012_000_0000': '4XIW',
    'cho_iprx_1931_0013_000_0000': '4XIX',
    'cho_iprx_1931_0014_000_0000': '4XIY',
    'cho_iprx_1931_0015_000_0000': '4XIZ',
    'cho_iprx_1931_0016_000_0000': '4XJA',
    'cho_iprx_1931_0017_000_0000': '4XJB',
    'cho_iprx_1931_0019_000_0000': '4XJC',
    'cho_iprx_1931_0002_000_0000': '4XIM',
    'cho_iprx_1931_0003_000_0000': '4XIN',
    'cho_iprx_1931_0004_000_0000': '4XIO',
    'cho_iprx_1931_0005_000_0000': '4XIP',
    'cho_iprx_1931_0006_000_0000': '4XIQ',
    'cho_iprx_1931_0007_000_0000': '4XIR',
    'cho_iprx_1931_0008_000_0000': '4XIS',
    'cho_iprx_1931_0009_000_0000': '4XIT',
    'cho_iprx_1933_0000_002_0000': '4XJE',
    'cho_iprx_1933_0001_001_0000': '4XJF',
    'cho_iprx_1933_0010_000_0000': '4XJQ',
    'cho_iprx_1933_0011_000_0000': '4XJR',
    'cho_iprx_1933_0012_000_0000': '4XJS',
    'cho_iprx_1933_0013_000_0000': '4XJT',
    'cho_iprx_1933_0014_000_0000': '4XJU',
    'cho_iprx_1933_0015_000_0000': '4XJV',
    'cho_iprx_1933_0002_001_0000': '4XJG',
    'cho_iprx_1933_0003_001_0000': '4XJH',
    'cho_iprx_1933_0004_001_0000': '4XJI',
    'cho_iprx_1933_0005_000_0000': '4XJJ',
    'cho_iprx_1933_0006_000_0000': '4XJK',
    'cho_iprx_1933_0007_001_0000': '4XJM',
    'cho_iprx_1933_0007_002_0000': '4XJN',
    'cho_iprx_1933_0008_000_0000': '4XJO',
    'cho_iprx_1933_0009_000_0000': '4XJP',
    'cho_iprx_1936_0001_001_0000': '4XJY',
    'cho_iprx_1936_0002_001_0000': '4XJZ',
    'cho_iprx_1936_0003_001_0000': '4XKA',
    'cho_iprx_1936_0004_001_0000': '4XKC',
    'cho_iprx_1936_0000_001_0000': '4XKD',
    'cho_iprx_1936_0001_000_0000': '4XKE',
    'cho_iprx_1936_0010_000_0000': '4XKQ',
    'cho_iprx_1936_0011_000_0000': '4XKR',
    'cho_iprx_1936_0012_000_0000': '4XKT',
    'cho_iprx_1936_0013_000_0000': '4XKU',
    'cho_iprx_1936_0014_000_0000': '4XKV',
    'cho_iprx_1936_0015_000_0000': '4XKW',
    'cho_iprx_1936_0016_000_0000': '4XKX',
    'cho_iprx_1936_0017_000_0000': '4XKY',
    'cho_iprx_1936_0002_000_0000': '4XKG',
    'cho_iprx_1936_0003_000_0000': '4XKH',
    'cho_iprx_1936_0004_000_0000': '4XKJ',
    'cho_iprx_1936_0005_000_0000': '4XKK',
    'cho_iprx_1936_0006_000_0000': '4XKL',
    'cho_iprx_1936_0007_000_0000': '4XKM',
    'cho_iprx_1936_0008_000_0000': '4XKO',
    'cho_iprx_1936_0009_000_0000': '4XKP',
    'cho_iprx_1939_0001_001_0000': '4XLC',
    'cho_iprx_1939_0002_001_0000': '4XLE',
    'cho_iprx_1939_0003_001_0000': '4XLG',
    'cho_iprx_1939_0000_001_0000': '4XLH',
    'cho_iprx_1942_0001_000_0000': '4XLK',
    'cho_iprx_1942_0002_000_0000': '4XLL',
    'cho_iprx_1942_0003_000_0000': '4XLN',
    'cho_iprx_1942_0004_000_0000': '4XLO',
    'cho_iprx_1942_0005_000_0000': '4XLP',
    'cho_iprx_1942_0006_000_0000': '4XLQ',
    'cho_iprx_1942_0008_000_0000': '4XLS',
    'cho_iprx_1942_0009_000_0000': '4XLT',
    'cho_iprx_1942_0007_000_0000': '4XLR',
    'cho_iprx_1945_0001_001_0000': '4XLW',
    'cho_iprx_1945_0002_001_0000': '4XLX',
    'cho_iprx_1945_0003_001_0000': '4XLY',
    'cho_iprx_1945_0004_000_0000': '4XMA',
    'cho_iprx_1945_0005_000_0000': '4XMB',
    'cho_iprx_1945_0006_000_0000': '4XMC',
    'cho_iprx_1945_0007_000_0000': '6JWE',
    'cho_iprx_1945_0008_000_0000': '6JWF',
    'cho_iprx_1947_0001_000_0000': '6JWH',
    'cho_iprx_1947_0002_000_0000': '6JWI',
    'cho_iprx_1947_0003_000_0000': '6JWJ',
    'cho_iprx_1947_0004_000_0000': '6JWK',
    'cho_iprx_1947_0005_000_0000': '6JWL',
    'cho_iprx_1947_0006_000_0000': '6JWM',
    'cho_iprx_1950_0001_000_0000': '6JWO',
    'cho_iprx_1950_0002_000_0000': '6JWP',
    'cho_iprx_1950_0003_000_0000': '6JWQ',
    'cho_iprx_1954_0001_000_0000': '6JWS',
    'cho_iprx_1954_0002_000_0000': '6JWT',
    'cho_iprx_1954_0003_000_0000': '6JWU',
    'cho_iprx_1954_0000_000_0000': '6JWV',
    'cho_iprx_1958_0001_000_0000': '6JWX',
    'cho_iprx_1958_0002_000_0000': '6JWY',
    }


bcrc_head = '''<?xml version="1.0" encoding="utf-8"?>
<!-- Created with Liquid XML Studio Designer Edition 9.1.11.3570 (http://www.liquid-technologies.com) -->
<chapter contentType="speech" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <metadataInfo>
        <PSMID>%s</PSMID>
        <mcode>%s</mcode>
        <language ocr="English" primary="Yes">English</language>
        <productContentType>Conference Series</productContentType>
        <contentDate>
            <contentComposed>1933</contentComposed>
            <contentDecade>1930-1939</contentDecade>
            <contentYear>1933</contentYear>
            <contentDateStart>1933-01-01</contentDateStart>
            <contentDateEnd>1933-12-31</contentDateEnd>
        </contentDate>
        <chathamHouseRule>No</chathamHouseRule>
        <ocr>75.30</ocr>
        <sourceLibrary>
            <libraryName>Chatham House</libraryName>
            <libraryLocation>London, UK</libraryLocation>
            <copyrightStatement>Copyright Statement</copyrightStatement>
        </sourceLibrary>
    </metadataInfo>
    <citation>
        <conference>
            <conferenceGroup>
                <conferenceName>British Commonwealth Relations. 1st Conference, Toronto, 1933. Vol. 1. Verbatim reports</conferenceName>
                <conferenceLocation>Toronto, Canada</conferenceLocation>
                <conferenceDate>
                    <conferenceComposed>September 1933</conferenceComposed>
                    <conferenceYear>1933</conferenceYear>
                    <conferenceMonth>September</conferenceMonth>
                    <conferenceDay>11</conferenceDay>
                </conferenceDate>
            </conferenceGroup>
            <pubDate>
                <composed>1933</composed>
                <year>1933</year>
                <pubDateStart>1933-01-01</pubDateStart>
                <pubDateEnd>1933-12-31</pubDateEnd>
            </pubDate>
            <titleGroup>
                <fullTitle>British Commonwealth Realtions Conference, Toronto %s</fullTitle>
            </titleGroup>
            <totalPages>%s</totalPages>
        </conference>
    </citation>
'''

bcrc_mid = '''<page id="%s" type="front_matter" firstPage="Yes">
        <pageImage pageIndicator="single" width="52" height="52" type="jpeg" colorimage="color" pagePosition="left">%s</pageImage>
        <sourcePage>%s</sourcePage>
        <article id="%s" type="front_matter" level="1">
            <clip pgref="%s" />
            <illustration pgref="0001" type="chart" colorimage="color">
                <caption>Caption # %s</caption>
            </illustration>
            <articleInfo>
                <title>Title # %s</title>
                <language ocr="english" primary="Yes">English</language>
                <ocr>99.99</ocr>
                <pageCount>%s</pageCount>
                <pageRange>1-%s</pageRange>
            </articleInfo>
            <text>
                <textclip>
                    <articlePage pgref="1" />
                    <p>
                        <word pos="45, 60, 47, 50">Front</word>
                        <word pos="47, 60, 49, 50">matter</word>
                    </p>
                </textclip>
            </text>
        </article>
    </page>
'''

bcrc_tail = '''</chapter>

'''
