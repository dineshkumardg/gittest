#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_survey.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_survey.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname_siax = os.path.join(os.path.dirname(__file__), '../test_samples/cho_siax_1963_0000_000_0000.xml')
>>> asset = Asset(fname_siax)
>>> dom_adapter_siax = Cho(asset)
>>> print(dom_adapter_siax.document().dom_id)
cho_siax_1963_0000_000_0000

>>> pages = dom_adapter_siax.pages()
>>> len(pages)
356

>>> print pages[len(pages) - 1]
Page(dom_id="356", dom_name="351", info="{'/chapter/page[356]/sourcePage': u'351', '_asset_fname': u'cho_siax_1963_0000_000_0356.jpg', '/chapter/page[356]/article/text/textclip/footnote/word': '_IS_ABSENT_', '@id': '356', '_id': 356}")

>>> chunks = dom_adapter_siax.chunks()
>>> print len(chunks)
52

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="52", dom_name="Index", clip_ids="None", is_binary="False", page_ids="[324, 324, 324, 325, 325, 326, 326, 327, 327, 328, 328, 329, 329, 330, 330, 331, 331, 332, 332, 333, 333, 334, 334, 335, 335, 336, 336, 337, 337, 338, 338, 339, 339, 340, 340, 341, 341, 342, 342, 343, 343, 344, 344, 345, 345, 346, 346, 347, 347, 348, 348, 349, 349, 350, 350, 351, 351, 352, 352, 353, 353, 354, 354, 355, 355, 356, 356]", info="{'/chapter/page[324]/article/articleInfo/pageCount': u'33', '/chapter/page[324]/article/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page[324]/article/articleInfo/language': u'English', '/chapter/page[324]/article/@level': u'1', '/chapter/page[324]/article/articleInfo/byline': '_IS_ABSENT_', '/chapter/page[324]/article/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page[324]/article/articleInfo/title': u'Index', '/chapter/page[324]/article/articleInfo/startingColumn': u'A', '/chapter/page[324]/article/@id': u'52', '/chapter/page[324]/article/@type': u'back_matter', '/chapter/page[324]/article/articleInfo/issueTitle': '_IS_ABSENT_'}")

>>> print(dom_adapter_siax.clips())
[]

>>> for link in dom_adapter_siax.links():
...     print link
DocumentLink(dom_id="1", dom_name="Documents, 1962, No. 128", info="{'/chapter/page[13]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[13]/article/text/textclip[4]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[13]/article/text/textclip[4]/relatedDocument/@pgref': u'16'}")
DocumentLink(dom_id="2", dom_name="Documents, 1963, pp. 28-31", info="{'/chapter/page[13]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[13]/article/text/textclip[6]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[13]/article/text/textclip[6]/relatedDocument/@pgref': u'18'}")
DocumentLink(dom_id="3", dom_name="Documents, 1963, pp. 156-7", info="{'/chapter/page[13]/article/text/textclip[7]/relatedDocument/@pgref': u'19', '/chapter/page[13]/article/text/textclip[7]/relatedDocument/@type': u'footnote', '/chapter/page[13]/article/text/textclip[7]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="4", dom_name="Documents, 1963, pp. 157-8", info="{'/chapter/page[13]/article/text/textclip[8]/relatedDocument/@pgref': u'20', '/chapter/page[13]/article/text/textclip[8]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[13]/article/text/textclip[8]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="5", dom_name="Documents, 1963, pp. 187-90", info="{'/chapter/page[13]/article/text/textclip[9]/relatedDocument/@pgref': u'21', '/chapter/page[13]/article/text/textclip[9]/relatedDocument/@type': u'footnote', '/chapter/page[13]/article/text/textclip[9]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="6", dom_name="Documents, 1963, pp. 14-19", info="{'/chapter/page[21]/article/text/textclip[2]/relatedDocument/@pgref': u'22', '/chapter/page[21]/article/text/textclip[2]/relatedDocument/@type': u'footnote', '/chapter/page[21]/article/text/textclip[2]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="7", dom_name="Documents, 1963, pp. 161-2", info="{'/chapter/page[21]/article/text/textclip[4]/relatedDocument[1]/@type': u'footnote', '/chapter/page[21]/article/text/textclip[4]/relatedDocument[1]/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[21]/article/text/textclip[4]/relatedDocument[1]/@pgref': u'24'}")
DocumentLink(dom_id="8", dom_name="Documents, 1963, pp. 162-4", info="{'/chapter/page[21]/article/text/textclip[4]/relatedDocument[2]/@pgref': u'24', '/chapter/page[21]/article/text/textclip[4]/relatedDocument[2]/@type': u'footnote', '/chapter/page[21]/article/text/textclip[4]/relatedDocument[2]/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="9", dom_name="Documents, 1963, pp. 34-40, 200-1", info="{'/chapter/page[21]/article/text/textclip[6]/relatedDocument[1]/@type': u'footnote', '/chapter/page[21]/article/text/textclip[6]/relatedDocument[1]/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[21]/article/text/textclip[6]/relatedDocument[1]/@pgref': u'26'}")
DocumentLink(dom_id="10", dom_name="Documents, 1963, pp. 34-4", info="{'/chapter/page[21]/article/text/textclip[6]/relatedDocument[2]/@type': u'footnote', '/chapter/page[21]/article/text/textclip[6]/relatedDocument[2]/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[21]/article/text/textclip[6]/relatedDocument[2]/@pgref': u'26'}")
DocumentLink(dom_id="11", dom_name="Documents, 1963, pp. 144-56", info="{'/chapter/page[21]/article/text/textclip[7]/relatedDocument/@type': u'footnote', '/chapter/page[21]/article/text/textclip[7]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[21]/article/text/textclip[7]/relatedDocument/@pgref': u'27'}")
DocumentLink(dom_id="12", dom_name="Documents, 1963, pp. 168-70", info="{'/chapter/page[27]/article/text/textclip[3]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[27]/article/text/textclip[3]/relatedDocument/@pgref': u'29', '/chapter/page[27]/article/text/textclip[3]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="13", dom_name="Documents, 1963, pp. 46-54", info="{'/chapter/page[27]/article/text/textclip[4]/relatedDocument/@pgref': u'30', '/chapter/page[27]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[27]/article/text/textclip[4]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000'}")
DocumentLink(dom_id="14", dom_name="Documents, 1963, pp. 170-3", info="{'/chapter/page[27]/article/text/textclip[5]/relatedDocument/@pgref': u'31', '/chapter/page[27]/article/text/textclip[5]/relatedDocument/@type': u'footnote', '/chapter/page[27]/article/text/textclip[5]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000'}")
DocumentLink(dom_id="15", dom_name="Documents, 1963, pp. 42-3", info="{'/chapter/page[31]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[31]/article/text/textclip[6]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[31]/article/text/textclip[6]/relatedDocument/@pgref': u'36'}")
DocumentLink(dom_id="16", dom_name="Documents, 1963, pp. 74-80", info="{'/chapter/page[37]/article/text/textclip[3]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[37]/article/text/textclip[3]/relatedDocument/@pgref': u'39', '/chapter/page[37]/article/text/textclip[3]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="17", dom_name="Documents, 1963, pp. 54-5", info="{'/chapter/page[39]/article/text/textclip[2]/relatedDocument/@pgref': u'40', '/chapter/page[39]/article/text/textclip[2]/relatedDocument/@type': u'footnote', '/chapter/page[39]/article/text/textclip[2]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000'}")
DocumentLink(dom_id="18", dom_name="Documents, 1963, pp. 55-7", info="{'/chapter/page[39]/article/text/textclip[3]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[39]/article/text/textclip[3]/relatedDocument/@pgref': u'41', '/chapter/page[39]/article/text/textclip[3]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="19", dom_name="Documents, 1962, pp. 631-5", info="{'/chapter/page[42]/article/text/textclip[8]/relatedDocument/@type': u'footnote', '/chapter/page[42]/article/text/textclip[8]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[42]/article/text/textclip[8]/relatedDocument/@pgref': u'49'}")
DocumentLink(dom_id="20", dom_name="Documents, 1963, pp. 212-17", info="{'/chapter/page[42]/article/text/textclip[14]/relatedDocument/@pgref': u'55', '/chapter/page[42]/article/text/textclip[14]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[42]/article/text/textclip[14]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="21", dom_name="Documents, 1963, pp. 218-28", info="{'/chapter/page[42]/article/text/textclip[15]/relatedDocument[1]/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[42]/article/text/textclip[15]/relatedDocument[1]/@pgref': u'56', '/chapter/page[42]/article/text/textclip[15]/relatedDocument[1]/@type': u'footnote'}")
DocumentLink(dom_id="22", dom_name="Documents, 1963, pp. 14-19", info="{'/chapter/page[42]/article/text/textclip[15]/relatedDocument[2]/@pgref': u'56', '/chapter/page[42]/article/text/textclip[15]/relatedDocument[2]/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[42]/article/text/textclip[15]/relatedDocument[2]/@type': u'footnote'}")
DocumentLink(dom_id="23", dom_name="Documents, 1963, pp. 287-90", info="{'/chapter/page[42]/article/text/textclip[18]/relatedDocument/@pgref': u'59', '/chapter/page[42]/article/text/textclip[18]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[42]/article/text/textclip[18]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="24", dom_name="Documents, 1963, pp. 84-5", info="{'/chapter/page[64]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[6]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[6]/relatedDocument/@pgref': u'69'}")
DocumentLink(dom_id="25", dom_name="Documents, 1963, No. 136", info="{'/chapter/page[64]/article/text/textclip[10]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[10]/relatedDocument/@pgref': u'73', '/chapter/page[64]/article/text/textclip[10]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000'}")
DocumentLink(dom_id="26", dom_name="Documents, 1963, pp. 85-97", info="{'/chapter/page[64]/article/text/textclip[15]/relatedDocument/@docref': u'cho_diax_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[15]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[15]/relatedDocument/@pgref': u'78'}")
DocumentLink(dom_id="27", dom_name="Documents, 1963, pp. 85-97", info="{'/chapter/page[64]/article/text/textclip[16]/relatedDocument/@pgref': u'79', '/chapter/page[64]/article/text/textclip[16]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[16]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="28", dom_name="Documents, 1963, p. 97", info="{'/chapter/page[64]/article/text/textclip[19]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[19]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[19]/relatedDocument/@pgref': u'82'}")
DocumentLink(dom_id="29", dom_name="Documents, 1963, pp. 98-107", info="{'/chapter/page[64]/article/text/textclip[22]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[22]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[22]/relatedDocument/@pgref': u'85'}")
DocumentLink(dom_id="30", dom_name="Documents, 1963, pp. 124-6", info="{'/chapter/page[64]/article/text/textclip[23]/relatedDocument/@pgref': u'86', '/chapter/page[64]/article/text/textclip[23]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[23]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="31", dom_name="Documents, 1963, pp. 128-9", info="{'/chapter/page[64]/article/text/textclip[24]/relatedDocument/@type': u'footnote', '/chapter/page[64]/article/text/textclip[24]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[64]/article/text/textclip[24]/relatedDocument/@pgref': u'87'}")
DocumentLink(dom_id="32", dom_name="Documents, 1963, pp. 41-2", info="{'/chapter/page[105]/article/text/textclip[6]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[105]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[105]/article/text/textclip[6]/relatedDocument/@pgref': u'110'}")
DocumentLink(dom_id="33", dom_name="Documents, 1963, pp. 344-5", info="{'/chapter/page[143]/article/text/textclip[9]/relatedDocument/@type': u'footnote', '/chapter/page[143]/article/text/textclip[9]/relatedDocument/@pgref': u'150', '/chapter/page[143]/article/text/textclip[9]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="34", dom_name="Documents, 1963, pp. 350-2", info="{'/chapter/page[154]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[154]/article/text/textclip[6]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[154]/article/text/textclip[6]/relatedDocument/@pgref': u'159'}")
DocumentLink(dom_id="35", dom_name="Documents, 1963, pp. 352-60", info="{'/chapter/page[154]/article/text/textclip[9]/relatedDocument/@pgref': u'162', '/chapter/page[154]/article/text/textclip[9]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[154]/article/text/textclip[9]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="36", dom_name="Documents, 1963, pp. 347-52", info="{'/chapter/page[154]/article/text/textclip[11]/relatedDocument[1]/@pgref': u'164', '/chapter/page[154]/article/text/textclip[11]/relatedDocument[1]/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[154]/article/text/textclip[11]/relatedDocument[1]/@type': u'footnote'}")
DocumentLink(dom_id="37", dom_name="Documents, 1955, pp. 429-38", info="{'/chapter/page[154]/article/text/textclip[11]/relatedDocument[2]/@pgref': u'164', '/chapter/page[154]/article/text/textclip[11]/relatedDocument[2]/@type': u'footnote', '/chapter/page[154]/article/text/textclip[11]/relatedDocument[2]/@docref': u'cho_dia_1955_000_000_0000'}")
DocumentLink(dom_id="38", dom_name="Documents, 1963, p. 291-315", info="{'/chapter/page[198]/article[2]/text/textclip[10]/relatedDocument/@pgref': u'207', '/chapter/page[198]/article[2]/text/textclip[10]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[198]/article[2]/text/textclip[10]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="39", dom_name="Documents, 1963, p. 315", info="{'/chapter/page[198]/article[2]/text/textclip[13]/relatedDocument/@pgref': u'210', '/chapter/page[198]/article[2]/text/textclip[13]/relatedDocument/@type': u'footnote', '/chapter/page[198]/article[2]/text/textclip[13]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="40", dom_name="Documents, 1963, pp. 315-21", info="{'/chapter/page[219]/article/text/textclip[3]/relatedDocument/@type': u'footnote', '/chapter/page[219]/article/text/textclip[3]/relatedDocument/@pgref': u'221', '/chapter/page[219]/article/text/textclip[3]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="41", dom_name="Documents, 1963, pp. 321-2", info="{'/chapter/page[219]/article/text/textclip[4]/relatedDocument/@pgref': u'222', '/chapter/page[219]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[219]/article/text/textclip[4]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="42", dom_name="Documents, 1963, pp. 322-8", info="{'/chapter/page[224]/article/text/textclip[14]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[224]/article/text/textclip[14]/relatedDocument/@pgref': u'237', '/chapter/page[224]/article/text/textclip[14]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="43", dom_name="Documents, 1963, pp. 331-2", info="{'/chapter/page[224]/article/text/textclip[15]/relatedDocument/@pgref': u'238', '/chapter/page[224]/article/text/textclip[15]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[224]/article/text/textclip[15]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="44", dom_name="Documents, 1963, pp. 323-5", info="{'/chapter/page[224]/article/text/textclip[17]/relatedDocument/@pgref': u'240', '/chapter/page[224]/article/text/textclip[17]/relatedDocument/@type': u'footnote', '/chapter/page[224]/article/text/textclip[17]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="45", dom_name="Documents, 1963, pp. 325-7", info="{'/chapter/page[224]/article/text/textclip[18]/relatedDocument/@pgref': u'241', '/chapter/page[224]/article/text/textclip[18]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[224]/article/text/textclip[18]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="46", dom_name="Documents, 1963, pp. 325-7", info="{'/chapter/page[224]/article/text/textclip[19]/relatedDocument/@type': u'footnote', '/chapter/page[224]/article/text/textclip[19]/relatedDocument/@pgref': u'242', '/chapter/page[224]/article/text/textclip[19]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="47", dom_name="Documents, 1963, pp. 327-8", info="{'/chapter/page[224]/article/text/textclip[20]/relatedDocument/@type': u'footnote', '/chapter/page[224]/article/text/textclip[20]/relatedDocument/@pgref': u'243', '/chapter/page[224]/article/text/textclip[20]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="48", dom_name="Documents, 1963, pp. 332-4", info="{'/chapter/page[224]/article/text/textclip[24]/relatedDocument/@type': u'footnote', '/chapter/page[224]/article/text/textclip[24]/relatedDocument/@pgref': u'247', '/chapter/page[224]/article/text/textclip[24]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="49", dom_name="Documents, 1961, pp. 767-9.", info="{'/chapter/page[249]/article[2]/text/textclip[2]/relatedDocument/@docref': u'cho_dia_1961_000_000_0000', '/chapter/page[249]/article[2]/text/textclip[2]/relatedDocument/@type': u'footnote', '/chapter/page[249]/article[2]/text/textclip[2]/relatedDocument/@pgref': u'250'}")
DocumentLink(dom_id="50", dom_name="Documents, 1962, pp. 862-3", info="{'/chapter/page[252]/article/text/textclip[3]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[252]/article/text/textclip[3]/relatedDocument/@pgref': u'254', '/chapter/page[252]/article/text/textclip[3]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="51", dom_name="Documents, 1962, pp. 863-4", info="{'/chapter/page[252]/article/text/textclip[4]/relatedDocument/@pgref': u'255', '/chapter/page[252]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[252]/article/text/textclip[4]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000'}")
DocumentLink(dom_id="52", dom_name="Documents, 1962, pp. 866-71", info="{'/chapter/page[252]/article/text/textclip[6]/relatedDocument/@pgref': u'257', '/chapter/page[252]/article/text/textclip[6]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[252]/article/text/textclip[6]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="53", dom_name="Documents, 1962, pp. 866-71", info="{'/chapter/page[252]/article/text/textclip[7]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[252]/article/text/textclip[7]/relatedDocument/@type': u'footnote', '/chapter/page[252]/article/text/textclip[7]/relatedDocument/@pgref': u'258'}")
DocumentLink(dom_id="54", dom_name="Documents, 1962, p. 876", info="{'/chapter/page[259]/article/text/textclip[5]/relatedDocument/@pgref': u'263', '/chapter/page[259]/article/text/textclip[5]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[259]/article/text/textclip[5]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="55", dom_name="Documents, 1962, pp. 878-9", info="{'/chapter/page[266]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[266]/article/text/textclip[4]/relatedDocument/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[266]/article/text/textclip[4]/relatedDocument/@pgref': u'269'}")
DocumentLink(dom_id="56", dom_name="Documents, 1962, pp. 896-906", info="{'/chapter/page[274]/article/text/textclip[5]/relatedDocument[1]/@pgref': u'278', '/chapter/page[274]/article/text/textclip[5]/relatedDocument[1]/@docref': u'cho_dia_1962_000_000_0000', '/chapter/page[274]/article/text/textclip[5]/relatedDocument[1]/@type': u'footnote'}")
DocumentLink(dom_id="57", dom_name="Documents, 1963, pp. 434-6", info="{'/chapter/page[274]/article/text/textclip[5]/relatedDocument[2]/@pgref': u'278', '/chapter/page[274]/article/text/textclip[5]/relatedDocument[2]/@type': u'footnote', '/chapter/page[274]/article/text/textclip[5]/relatedDocument[2]/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="58", dom_name="Documents, 1963, pp. 436-43", info="{'/chapter/page[291]/article/text/textclip[3]/relatedDocument/@type': u'footnote', '/chapter/page[291]/article/text/textclip[3]/relatedDocument/@pgref': u'293', '/chapter/page[291]/article/text/textclip[3]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="59", dom_name="Documents, 1963, pp. 444-7", info="{'/chapter/page[291]/article/text/textclip[4]/relatedDocument/@pgref': u'294', '/chapter/page[291]/article/text/textclip[4]/relatedDocument/@type': u'footnote', '/chapter/page[291]/article/text/textclip[4]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="60", dom_name="Documents, 1963, pp. 447-52", info="{'/chapter/page[291]/article/text/textclip[5]/relatedDocument/@pgref': u'295', '/chapter/page[291]/article/text/textclip[5]/relatedDocument/@type': u'footnote', '/chapter/page[291]/article/text/textclip[5]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="61", dom_name="Documents, 1963, pp. 453-5", info="{'/chapter/page[291]/article/text/textclip[6]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[291]/article/text/textclip[6]/relatedDocument/@type': u'footnote', '/chapter/page[291]/article/text/textclip[6]/relatedDocument/@pgref': u'296'}")
DocumentLink(dom_id="62", dom_name="Documents, 1963, pp. 444-6", info="{'/chapter/page[297]/article/text/textclip[2]/relatedDocument/@type': u'footnote', '/chapter/page[297]/article/text/textclip[2]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[297]/article/text/textclip[2]/relatedDocument/@pgref': u'298'}")
DocumentLink(dom_id="63", dom_name="Documents, 1963, pp. 455-6", info="{'/chapter/page[297]/article/text/textclip[9]/relatedDocument/@type': u'footnote', '/chapter/page[297]/article/text/textclip[9]/relatedDocument/@pgref': u'305', '/chapter/page[297]/article/text/textclip[9]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="64", dom_name="Documents, 1963, pp. 461-2", info="{'/chapter/page[297]/article/text/textclip[13]/relatedDocument[1]/@pgref': u'309', '/chapter/page[297]/article/text/textclip[13]/relatedDocument[1]/@type': u'footnote', '/chapter/page[297]/article/text/textclip[13]/relatedDocument[1]/@docref': u'cho_dia_1963_000_000_0000'}")
DocumentLink(dom_id="65", dom_name="Documents, 1963, pp. 462-3", info="{'/chapter/page[297]/article/text/textclip[13]/relatedDocument[2]/@type': u'footnote', '/chapter/page[297]/article/text/textclip[13]/relatedDocument[2]/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[297]/article/text/textclip[13]/relatedDocument[2]/@pgref': u'309'}")
DocumentLink(dom_id="66", dom_name="Documents, 1960, pp. 404-6", info="{'/chapter/page[297]/article/text/textclip[15]/relatedDocument/@docref': u'cho_dia_1960_000_000_0000', '/chapter/page[297]/article/text/textclip[15]/relatedDocument/@type': u'footnote', '/chapter/page[297]/article/text/textclip[15]/relatedDocument/@pgref': u'311'}")
DocumentLink(dom_id="67", dom_name="Documents, 1963, pp. 465-6", info="{'/chapter/page[297]/article/text/textclip[16]/relatedDocument/@pgref': u'312', '/chapter/page[297]/article/text/textclip[16]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[297]/article/text/textclip[16]/relatedDocument/@type': u'footnote'}")
DocumentLink(dom_id="68", dom_name="Documents, 1963, pp. 466-7", info="{'/chapter/page[313]/article/text/textclip[8]/relatedDocument/@docref': u'cho_dia_1963_000_000_0000', '/chapter/page[313]/article/text/textclip[8]/relatedDocument/@pgref': u'320', '/chapter/page[313]/article/text/textclip[8]/relatedDocument/@type': u'footnote'}")


>>> pprint(dom_adapter_siax.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/book/author/@role': u'author',
 '/chapter/citation/book/author/@type': '_IS_ABSENT_',
 '/chapter/citation/book/author/aucomposed': u'D. C. Watt',
 '/chapter/citation/book/author/first': u'D.',
 '/chapter/citation/book/author/last': u'Watt',
 '/chapter/citation/book/author/middle': u'C.',
 '/chapter/citation/book/byline': '_IS_ABSENT_',
 '/chapter/citation/book/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/book/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/book/imprint/imprintFull': u'Oxford University Press, Walton Street, Oxford OX2 6DP',
 '/chapter/citation/book/imprint/imprintPublisher': u'Oxford University Press',
 '/chapter/citation/book/pubDate/composed': u'1977',
 '/chapter/citation/book/pubDate/pubDateEnd': u'1977-12-31',
 '/chapter/citation/book/pubDate/pubDateStart': u'1977-01-01',
 '/chapter/citation/book/pubDate/year': u'1977',
 '/chapter/citation/book/publicationPlace/publicationPlaceCity': u'Oxford',
 '/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'Oxford, UK',
 '/chapter/citation/book/publicationPlace/publicationPlaceCountry': u'UK',
 '/chapter/citation/book/seriesGroup/seriesNumber': '_IS_ABSENT_',
 '/chapter/citation/book/seriesGroup/seriesTitle': '_IS_ABSENT_',
 '/chapter/citation/book/titleGroup/fullTitle': u'Survey of International Affairs',
 '/chapter/citation/book/totalPages': u'356',
 '/chapter/metadataInfo/PSMID': u'cho_siax_1963_0000_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1963',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1963-12-31',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1963-01-01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1960-1969',
 '/chapter/metadataInfo/contentDate/contentYear': u'1963',
 '/chapter/metadataInfo/isbn': u'0192147331',
 '/chapter/metadataInfo/issn': '_IS_ABSENT_',
 '/chapter/metadataInfo/language': u'English',
 '/chapter/metadataInfo/productContentType': u'Survey and Documents Series',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_siax_1963_0000_000_0000',
 '_dom_name': u'cho_siax_1963_0000_000_0000'}



# diax ================================================================================================

>>> fname_diax = os.path.join(os.path.dirname(__file__), '../test_samples/cho_diax_1963_0000_000_0000.xml')
>>> asset = Asset(fname_diax)
>>> dom_adapter_diax = Cho(asset)
>>> print(dom_adapter_diax.document().dom_id)
cho_diax_1963_0000_000_0000

>>> pages = dom_adapter_diax.pages()
>>> len(pages)
533

>>> print pages[len(pages) - 1]
Page(dom_id="533", dom_name="517", info="{'@id': '533', '_asset_fname': u'cho_diax_1963_0000_000_0533.jpg', '/chapter/page[533]/sourcePage': u'517', '_id': 533, '/chapter/page[533]/article/text/textclip/footnote/word': '_IS_ABSENT_'}")

>>> chunks = dom_adapter_diax.chunks()
>>> print len(chunks)
176

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="176", dom_name="Chronological List of Documents", clip_ids="None", is_binary="False", page_ids="[526, 527, 528, 529, 530, 531, 532, 533]", info="{'/chapter/page[526]/article/articleInfo/title': u'Chronological List of Documents', '/chapter/page[526]/article/articleInfo/startingColumn': u'A', '/chapter/page[526]/article/@id': u'176', '/chapter/page[526]/article/articleInfo/pageCount': u'8', '/chapter/page[526]/article/articleInfo/byline': '_IS_ABSENT_', '/chapter/page[526]/article/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page[526]/article/articleInfo/issueTitle': '_IS_ABSENT_', '/chapter/page[526]/article/articleInfo/language': u'English', '/chapter/page[526]/article/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page[526]/article/@level': u'1', '/chapter/page[526]/article/@type': u'back_matter'}")

>>> print(dom_adapter_diax.clips())
[]

>>> for link in dom_adapter_diax.links():
...     print link
DocumentLink(dom_id="1", dom_name="RELATED_DOC1: Survey, 1962, pp. 479-81.", info="{'/chapter/page[307]/article[3]/text/textclip/relatedDocument[1]/@pgref': u'1', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[1]/@docref': u'cho_sia_1962_000_000_0000', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[1]/@type': u'footnote'}")
DocumentLink(dom_id="2", dom_name="RELATED_DOC2: Survey, 1962, pp. 479-81.", info="{'/chapter/page[307]/article[3]/text/textclip/relatedDocument[2]/@docref': u'cho_sia_1962_000_000_0000', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[2]/@pgref': u'2', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[2]/@type': u'footnote'}")
DocumentLink(dom_id="3", dom_name="RELATED_DOC3: Survey, 1962, pp. 479-81.", info="{'/chapter/page[307]/article[3]/text/textclip/relatedDocument[3]/@type': u'footnote', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[3]/@docref': u'cho_sia_1962_000_000_0000', '/chapter/page[307]/article[3]/text/textclip/relatedDocument[3]/@pgref': u'3'}")
DocumentLink(dom_id="4", dom_name="Survey, 1962, pp. 350-2.", info="{'/chapter/page[381]/article[2]/text/textclip[1]/relatedDocument/@docref': u'cho_sia_1962_000_000_0000', '/chapter/page[381]/article[2]/text/textclip[1]/relatedDocument/@pgref': u'4', '/chapter/page[381]/article[2]/text/textclip[1]/relatedDocument/@type': u'footnote'}")

>>> pprint(dom_adapter_diax.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/book/author[1]/@role': u'Editor',
 '/chapter/citation/book/author[1]/@type': u'No',
 '/chapter/citation/book/author[1]/aucomposed': u'D. C. Watt',
 '/chapter/citation/book/author[1]/first': u'D.',
 '/chapter/citation/book/author[1]/last': u'Watt',
 '/chapter/citation/book/author[1]/middle': u'C.',
 '/chapter/citation/book/author[2]/@role': u'author',
 '/chapter/citation/book/author[2]/@type': u'No',
 '/chapter/citation/book/author[2]/aucomposed': u'James Mayall',
 '/chapter/citation/book/author[2]/first': u'James',
 '/chapter/citation/book/author[2]/last': u'Mayall',
 '/chapter/citation/book/author[3]/@role': u'Editor',
 '/chapter/citation/book/author[3]/@type': u'Yes',
 '/chapter/citation/book/author[3]/aucomposed': u'Carnelia Navari',
 '/chapter/citation/book/author[3]/first': u'Carnelia',
 '/chapter/citation/book/author[3]/last': u'Navari',
 '/chapter/citation/book/byline': '_IS_ABSENT_',
 '/chapter/citation/book/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/book/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/book/imprint/imprintFull': u'Oxford University Press, Ely House, London W. 1X 4AH',
 '/chapter/citation/book/imprint/imprintPublisher': u'Oxford University Press',
 '/chapter/citation/book/pubDate/composed': u'1973',
 '/chapter/citation/book/pubDate/pubDateEnd': u'1973-12-31',
 '/chapter/citation/book/pubDate/pubDateStart': u'1973-01-01',
 '/chapter/citation/book/pubDate/year': u'1973',
 '/chapter/citation/book/publicationPlace/publicationPlaceCity': u'Oxford',
 '/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'Oxford, UK',
 '/chapter/citation/book/publicationPlace/publicationPlaceCountry': u'UK',
 '/chapter/citation/book/seriesGroup/seriesNumber': '_IS_ABSENT_',
 '/chapter/citation/book/seriesGroup/seriesTitle': '_IS_ABSENT_',
 '/chapter/citation/book/titleGroup/fullTitle': u'Documents of International Affairs',
 '/chapter/citation/book/totalPages': u'533',
 '/chapter/metadataInfo/PSMID': u'cho_diax_1963_0000_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1963',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1963-12-31',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1963-01-01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1960-1969',
 '/chapter/metadataInfo/contentDate/contentYear': u'1963',
 '/chapter/metadataInfo/isbn': u'0192148184',
 '/chapter/metadataInfo/issn': '_IS_ABSENT_',
 '/chapter/metadataInfo/language': u'English',
 '/chapter/metadataInfo/productContentType': u'Survey and Documents Series',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_diax_1963_0000_000_0000',
 '_dom_name': u'cho_diax_1963_0000_000_0000'}

'''
