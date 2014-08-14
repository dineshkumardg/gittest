"""
http://www.django-rest-framework.org/
/home/jsears/bin/python2.7.5/bin/pip install djangorestframework
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from django.utils.encoding import smart_text
from django.conf import settings
from django.shortcuts import get_object_or_404
from gaia.config.config import get_config
from gaia.dom.model.item import Item as DomItem
from gaia.web.web_box import WebBox
from gaia.egest.outbox import Outbox
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from gaia.log.log import Log
from gaia.dom.index.models import Item
from lxml import etree


class _ItemXMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_text(data)


class WSItem(APIView):
    """
    http://127.0.0.1:8889/qa/ws/v1.0/item/?item_id=1
    """
    renderer_classes = [_ItemXMLRenderer]
    config = get_config(settings.CONFIG_NAME)
    log = Log.get_logger('qa.views')

    def get(self, request, *args, **kw):  # TODO implement error handling in case arg not passed in!
        item_id = kw['item_id']

        self.log.info(item_id=item_id)

        original_xml_tree, possible_fixes = self.ingested_xml_and_fixes(item_id)

        """
        NOTE: lxml does the following (which makes fixed xml different from original xml)
        1. gets rid of: <?xml version='1.0' encoding='UTF-8'?>
        2. unescapes &quot; + &amp; + &apos; to " + & + '
        3. uses decimal &# values rather than hex

        None of these things affect the gift produced.
        """
        result = etree.tostring(self.patch(original_xml_tree, possible_fixes))
        return Response(result, status=status.HTTP_200_OK)

    def ingested_xml_and_fixes(self, item_id):
        item = get_object_or_404(Item, pk=item_id)
        item_name = item.dom_name
        outbox = Outbox(self.config.outbox)  # ideally use the web_box
        assets = outbox.assets(item_name)

        dom_item = DomItem(item_name, item_name, assets, self.config)  # inside the outbox
        original_xml_tree = dom_item._get_dom_adapter()._etree

        web_box = WebBox(self.config)
        fixes = web_box.get_changes(dom_item)  # Note: plain dicts (not json objects)

        return original_xml_tree, fixes

    def patch(self, original_xml_tree, possible_fixes):
        """
        Patch the orginal xml with possible fixes.

        The patch is tied to cho.py - and doesn't deal with _IS_ABSENT_ values (which might represent non existant nodes in the src)
        """
        for possible_item_change in possible_fixes:
            for key in possible_item_change.keys():
                # assuming that xpath always brings back a [] of elements but len of list is always 1
                if key[0] == '/' and possible_item_change[key] != GaiaDomAdapter.MISSING_FIELD_VALUE:
                    xpath = key
                    xpath_value = possible_item_change[key]

                    if xpath.find('aucomposed') > 0 or xpath.find('marginalia') > 0:  # EG-469
                        continue

                    if key.find('@') != -1:
                        # we've got an attribute, need to find element attr belongs to
                        xpath = key[0: key.rfind('/@')]
                        attr = key[key.rfind('/@') + 2:]

                        element_from_xpath = original_xml_tree.xpath(xpath)

                        if len(element_from_xpath) == 0:
                            #raise GaiaCodingError(msg='attempted to insert new attribute - not coded yet', xpath=xpath)
                            self.log.error(msg='attempted to insert new attribute - not coded yet', xpath=xpath)
                        else:
                            # element always existed in the source xml
                            element_from_xpath[0].set(attr, xpath_value)
                    else:
                        # we've got an element
                        element_from_xpath = original_xml_tree.xpath(xpath)
                        if len(element_from_xpath) == 0:
                            # raise GaiaCodingError(msg='attempted to insert new element - not coded yet', xpath=xpath)
                            self.log.error(msg='attempted to insert new element - not coded yet', xpath=xpath)
                        else:
                            element_from_xpath[0].text = xpath_value

        return original_xml_tree  # with fixes
