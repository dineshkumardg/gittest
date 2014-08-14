# coding: utf-8

import re
import htmlentitydefs
from gaia.error import GaiaCodingError
from StringIO import StringIO


class EntityReference:
    """
    Various entity behaviour is centralised here.

    RE:
        http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references
        http://www.unicode.org/charts/PDF/U2000.pdf

    [jsears@ukandjsears-l2 test_samples]$ sed '/<word pos="15/d' cho_iaxx_1968_0044_000_0000.xml > cho_iaxx_1968_0044_000_0000.xml.1
    [jsears@ukandjsears-l2 test_samples]$ mv cho_iaxx_1968_0044_000_0000.xml.1 cho_iaxx_1968_0044_000_0000.xml

    sudo yum install perl-Archive-Extract
    sudo apt-get install libarchive-zip-perl

    make sure comprehensive_entity_list.html in .

    wrap .xml file with:
    <gold:feed xmlns:essay="http://www.gale.com/goldschema/essay" xmlns:gold="http://www.gale.com/gold" xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc" xmlns:dir="http://www.gale.com/goldschema/dir" xmlns:vault-link="http://www.gale.com/goldschema/vault-linking" xmlns:meta="http://www.gale.com/goldschema/metadata" xmlns:table="http://www.gale.com/goldschema/table" xmlns:xatts="http://www.gale.com/goldschema/xatts" xmlns:index="http://www.gale.com/goldschema/index" xmlns:mla="http://www.gale.com/goldschema/mla" xmlns:media="http://www.gale.com/goldschema/media" xmlns:tt="http://www.w3.org/ns/ttml" xmlns:list="http://www.gale.com/goldschema/list" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:etoc="http://www.gale.com/goldschema/etoc" xmlns:verse="http://www.gale.com/goldschema/verse" xmlns:pres="http://www.gale.com/goldschema/pres" xmlns:pub-meta="http://www.gale.com/goldschema/pub-meta" xmlns:shared="http://www.gale.com/goldschema/shared" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:math="http://www.w3.org/1998/Math/MathML" id="NOINDEX-CHOA_20131029_00629" xsi:schemaLocation="..\..\..\..\..\GIFT\feed_schemas\feed.xsd">
    ...
    <gold:metadata><gold:feed-type>NOINDEX</gold:feed-type><gold:document-schema>gift_document.xsd</gold:document-schema><gold:schema-version>2.5</gold:schema-version><gold:document-id-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value</gold:document-id-path><gold:document-mcode-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode</gold:document-mcode-path><gold:number-of-documents>1</gold:number-of-documents><gold:feed-status>New-Replace</gold:feed-status></gold:metadata></gold:feed>

    gzip the file

    perl choaEntityConversion.pl *.gz
    """

    # this aligns with how gaia dawn does escaping
    AMP_ESCAPE = '_zQz_AMP_QzQ_'
    QUOT_ESCAPE = '_zQz_QUOT_QzQ_'
    LT_ESCAPE = '_zQz_LT_QzQ_'
    GT_ESCAPE = '_zQz_GT_QzQ_'
    APOS_ESCAPE = '_zQz_APOS_QzQ_'
    AMP_HASH_PRESERVE = '_zQz_AMP_HASH_QzQ_'

    # for gift we have to preserve these and not escape them!
    GT_ESCAPE_KEEP = '_zQz_GT_KP_QzQ_'
    LT_ESCAPE_KEEP = '_zQz_LT_KP_QzQ_'

    @classmethod
    def escape(cls, text):
        # lxml automatically de-serialises &quote to " - where as we don't want this auto-magicical behaviour

        escaped_text = text  # TODO behind the scenes this is doing something!? Not sure what though: it means we can't refactor unescaped_text away and ref text directly

        if isinstance(escaped_text, basestring):
            escaped_text = escaped_text.replace('"', cls.QUOT_ESCAPE)
            escaped_text = escaped_text.replace("'", cls.APOS_ESCAPE)
            escaped_text = escaped_text.replace('<', cls.LT_ESCAPE)

            # RE: CHOA-1286
            # its possible we've got either "AV&#228;" or "AV&#" - a number or something that looks like a number
            if '&#' in escaped_text and ';' in escaped_text:
                # TODO - ideally parse the whole line for each occurance of &# to test if its a number or not.
                escaped_text = escaped_text.replace('&#', cls.AMP_HASH_PRESERVE)

            escaped_text = escaped_text.replace('&', cls.AMP_ESCAPE)

        else:
            raise GaiaCodingError('trying to escape a list, instead of word')

        return escaped_text

    @classmethod
    def prepare_for_lst(cls, xml):
        replacement_xml = ''
        sio = StringIO(xml)
        for line in sio.readlines():
            if re.search('<(meta:(prefix|first-name|middle-name|last-name|suffix|composed-name|name))>(.*?)<(/meta:(prefix|first-name|middle-name|last-name|suffix|composed-name|name))>', line):
                line = cls._escape_for_lst_platform(line)
            elif re.search('<(meta:(title-display|title-sort|title-open-url))>(.*?)<(/meta:(title-display|title-sort|title-open-url))>', line):
                line = cls._escape_for_lst_platform(line)

            replacement_xml += line

        return replacement_xml

    @classmethod
    def _escape_for_lst_platform(cls, text):
        if text is None:
            return None

        try:
            def fixup(m):
                # http://www.w3.org/blog/2008/04/unescape-html-entities-python/
                # http://effbot.org/zone/re-sub.htm#unescape-html
                # http://docs.python.org/2/howto/unicode.html
                text = m.group(0)
                if text[:2] == "&#":
                    # character reference
                    try:
                        if text[:3] == "&#x":
                            return unichr(int(text[3:-1], 16))
                        else:
                            return unichr(int(text[2:-1]))
                    except ValueError:
                        pass
                else:
                    # named entity,
                    try:
                        if text in ['&lt;', '&gt;', '&amp;', '&quot;', '&apos;']:  # fit in with photon's conversion script
                            return text
                        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                    except KeyError:
                        pass
                return text
            return re.sub("&#?\w+;", fixup, text)
        except Exception as e:
            raise GaiaCodingError(str(e))

    @classmethod
    def unescape(cls, text):
        unescaped_text = text  # TODO behind the scenes this is doing something!? Not sure what though: it means we can't refactor unescaped_text away and ref text directly

        if isinstance(unescaped_text, basestring):
            unescaped_text = unescaped_text.replace(cls.QUOT_ESCAPE, '&quot;')
            unescaped_text = unescaped_text.replace(cls.AMP_ESCAPE, '&amp;')
            unescaped_text = unescaped_text.replace(cls.AMP_HASH_PRESERVE, '&#')
            unescaped_text = unescaped_text.replace(cls.APOS_ESCAPE, '&apos;')
            unescaped_text = unescaped_text.replace(cls.LT_ESCAPE, '&lt;')
            unescaped_text = unescaped_text.replace(cls.GT_ESCAPE, '&gt;')
            unescaped_text = unescaped_text.replace(cls.LT_ESCAPE_KEEP, '<')
            unescaped_text = unescaped_text.replace(cls.GT_ESCAPE_KEEP, '>')
        else:
            raise GaiaCodingError('trying to escape a list, instead of word')

        return unescaped_text

    @classmethod
    def strip_out_various_entities(cls, text):
        """
        http://jira.cengage.com/browse/CHOA-1058 + http://jira.cengage.com/browse/CHOA-791
        """
        text = text.replace('\'', '')
        text = text.replace('\"', '')

        # DASHES - get replaced with a space
        text = text.replace('&#x2010;', ' ')
        text = text.replace('&#8208;', ' ')
        text = text.replace(u'‐', ' ')  # this is the really critical thing, as lxml - from xml_dict returns escaped glyph

        text = text.replace('&#x2012;', ' ')
        text = text.replace('&#8210;', ' ')
        text = text.replace(u'‒', ' ')

        text = text.replace('&#x2013;', ' ')
        text = text.replace('&#8211;', ' ')
        text = text.replace(u'–', ' ')

        text = text.replace('&#x2014;', ' ')
        text = text.replace('&#8212;', ' ')
        text = text.replace(u'—', ' ')

        text = text.replace('&#x2015;', ' ')
        text = text.replace('&#8213;', ' ')
        text = text.replace(u'―', ' ')

        # Quotation marks and apostrophe
        text = text.replace('&#x2018;', '')
        text = text.replace('&#8216;', '')
        text = text.replace(u'‘', '')

        text = text.replace('&#x02BB;', '')
        text = text.replace('&#699;', '')
        text = text.replace(u'ʻ', '')

        text = text.replace('&#x275B;', '')
        text = text.replace('&#10075;', '')
        text = text.replace(u'❛', '')

        text = text.replace('&#x2019;', '')
        text = text.replace('&#8217;', '')
        text = text.replace(u'’', '')

        text = text.replace('&#x02BC;', '')
        text = text.replace('&#700;', '')
        text = text.replace(u'ʼ', '')

        text = text.replace('&#x275C;', '')
        text = text.replace('&#10076;', '')
        text = text.replace(u'❜', '')

        text = text.replace('&#x201A;', '')
        text = text.replace('&#8218;', '')
        text = text.replace(u'‚', '')

        text = text.replace('&#x201B;', '')
        text = text.replace('&#8219;', '')
        text = text.replace(u'‛', '')

        text = text.replace('&#x02BD;', '')
        text = text.replace('&#701;', '')
        text = text.replace(u'ʽ', '')

        text = text.replace('&#x201C;', '')
        text = text.replace('&#8220;', '')
        text = text.replace(u'“', '')

        text = text.replace('&#x201F;', '')
        text = text.replace('&#8223;', '')
        text = text.replace(u'‟', '')

        text = text.replace('&#x275D;', '')
        text = text.replace('&#10077;', '')
        text = text.replace(u'❝', '')

        text = text.replace('&#x301D;', '')
        text = text.replace('&#12317;', '')
        text = text.replace(u'〝', '')

        text = text.replace('&#x201D;', '')
        text = text.replace('&#8221;', '')
        text = text.replace(u'”', '')

        text = text.replace('&#x2033;', '')
        text = text.replace('&#8243;', '')
        text = text.replace(u'′′', '')

        text = text.replace('&#x275E;', '')
        text = text.replace('&#10078;', '')
        text = text.replace(u'❞', '')

        text = text.replace('&#x301E;', '')
        text = text.replace('&#12318;', '')
        text = text.replace(u'〞', '')

        text = text.replace('&#x201E;', '')
        text = text.replace('&#8222;', '')
        text = text.replace(u'„', '')

        text = text.replace('&#x301F;', '')
        text = text.replace('&#12319;', '')
        text = text.replace(u'〟', '')

        text = text.replace('&#x201F;', '')
        text = text.replace('&#8223;', '')
        text = text.replace(u'‟', '')

        text = re.sub('<[^<]+?>', '', text)

        # SH told about these two but no JIRA's exist for them so we don't replace similar escaped glyphs
        text = text.rstrip('.')
        text = text.rstrip(',')

        text = text.replace(EntityReference.AMP_ESCAPE, '')
        text = text.replace(EntityReference.QUOT_ESCAPE, '')
        text = text.replace(EntityReference.LT_ESCAPE, '')
        text = text.replace(EntityReference.GT_ESCAPE, '')
        text = text.replace(EntityReference.APOS_ESCAPE, '')

        # belt and branches, but really xml_dict should have changed these to ' and " respectively
        text = text.replace('&quot;', '')
        text = text.replace('&apos;', '')

        text = text.replace('   ', ' ')
        text = text.replace('  ', ' ')

        return text
