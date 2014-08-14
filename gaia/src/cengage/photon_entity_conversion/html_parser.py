print unichr(233)

s = 'Monsieur Andr&#233; G&#233;raud'

HTML Entity (decimal) 	&#233;

>>> import HTMLParser
>>> h = HTMLParser.HTMLParser()
>>> s = h.unescape('Monsieur Andr&#233; G&#233;raud')
>>> print s
Monsieur André Géraud


http://www.w3.org/TR/unicode-xml/#Suitable

