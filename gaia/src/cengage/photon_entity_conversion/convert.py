# coding: utf-8

# unescape decimal entity code
# '<meta:last-name>Sch&#246;pflin</meta:last-name>'
# print unichr(246)
# ö

# http://www.w3.org/blog/2008/04/unescape-html-entities-python/
# http://effbot.org/zone/re-sub.htm#unescape-html
# http://docs.python.org/2/howto/unicode.html 

# sudo apt-get install language-support-fr
# gnome-language-selector
#
# without language support:
# <p>120571 &#120571;</p>       < should be "MATHEMATICAL ITALIC NABLA" 𝛻
#
# with language support
# <p>120571 &#120571;</p>
#
# jsears@ukandjsears-l2:~/Desktop/entity-problem/entity_escapign$ isutf8 '/home/jsears/Desktop/entity-problem/entity_escapign/gift_from_gaia/PSM-CHOA_20131028_00600.xml'
# jsears@ukandjsears-l2:~/Desktop/entity-problem/entity_escapign$ echo $?
# 0
#

import re, htmlentitydefs

def unescape(text):
    def fixup(m):
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
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is # TODO replace it with something else - i.e. whitepsace?
    return re.sub("&#?\w+;", fixup, text)

print unescape('<meta:last-name>Sch&#246;pflin</meta:last-name>')

#for i in range(1, 1114109):
#    print ('<p>%s %s</p>' % (i, unescape('&#%s;' % i))).encode('utf-8')

