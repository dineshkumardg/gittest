import json
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter

class FixForm():
    def __init__(self):
        self.dom_info_dicts = []
    
    def add_doc_info(self, json_info):
        self._add_info(json_info, 'D')

    def add_page_info(self, json_info):
        self._add_info(json_info, 'P')

    def add_chunk_info(self, json_info):
        self._add_info(json_info, 'C')

    def _add_info(self, json_info, dom_type):
        ' we have to add the object type so that we can apply changes later. '
        info_dict = json.loads(json_info)
        info_dict['_dom_type'] = dom_type
        self.dom_info_dicts.append(info_dict)

    def form(self, action_url):
        x = '<form action="%s" method="post">\n' % action_url

        for info in self.dom_info_dicts:
            dom_id = info['_dom_id']
            dom_type = info['_dom_type']
            dom_name = info['_dom_name']
            x += '<table border="0">\n'

            # get a set of keys which have duplicate keyname
            keys_dict = {}
            duplicate_keys = set()
            for key in sorted(info):
                if key.startswith('_'):
                    continue

                if key.find('aucomposed') > 0 or key.find('marginalia') > 0:  # EG-469
                    continue
                if key.startswith('@'):  # EG-469 (part of)
                    continue

                key_name = key.split('/')[-1]
                if key_name.startswith('@'):
                    key_name = key_name[1:]

                for prev_key in keys_dict:
                    if keys_dict[prev_key] == key_name: # if there is same values, add key to set
                        duplicate_keys.add(prev_key)
                        duplicate_keys.add(key)
                        break
                keys_dict[key] = key_name

            # display key and key names in that page
            for key in sorted(info):
                if key.startswith('_'):
                    continue

                if key.find('aucomposed') > 0 or key.find('marginalia') > 0:  # EG-469
                    continue
                if key.startswith('@'):  # EG-469 (part of)
                    continue

                split_num = len(key.split('/')) 
                if key in duplicate_keys and split_num > 2:
                    key_name = key.split('/')[-2] + "/" + key.split('/')[-1]
                else:
                    key_name = key.split('/')[-1]

                if key_name.startswith('@'):
                    key_name = key_name[1:]

                # We want to show the entity codes (ie as the data was entered) for editing
                # (and we add the visual version in a tooltip: 'title' enables a mouseover tooltip)
                displayable_value = info[key].replace('&', '&amp;')
                displayable_value = info[key].replace('"', '&#34;')  # EG-538

                if displayable_value != GaiaDomAdapter.MISSING_FIELD_VALUE:  # EG-469
                    display_key = '<span title="%s">%s:</span>' % (key, key_name)

                    params = (dom_type, dom_id, key, displayable_value)

                    input_field = '\n<input name="new|%s|%s|%s" value="%s" type="text" size="35">\n' % params
                    input_field += '<input name="old|%s|%s|%s" value="%s" type="hidden">\n' % params

                    input_field = '<span title="%s">%s</span>' % (info[key], input_field)

                    x += '<tr><td align="right">%s</td>\n<td>%s</td></tr>\n' % (display_key, input_field)

            x += '</table>\n'

        x += '<table width="100%">\n'
        x += '<tr>'
        x += '<td align="center"><input style="padding:7px; margin:3px; background-color: black; color: white; font-size:small" type="submit"  value="  fix  " /></td>'
        x += '</tr>'
        x += '</table>'

        x += '</form>\n'
        return x

    @staticmethod
    def parse(form_data):
        ''' Take data from a form and return a set of changed dom info.

            Note that form_data shoudl be a *plain dict* version of raw form-data (QueryDict.dict())
            Any unicode characters will be transformed into Xml Character Refs in the returned changes.

            changes = [doc_changes, page_changes, chunk_changes]
            Each is an empty dict if nothing changed.
        '''
        changes = {}
        changes['D'] = {}
        changes['P'] = {}
        changes['C'] = {}

        for key in form_data:
            old, dom_type, dom_id, xpath = key.split('|')

            if key.startswith('old'):
                new_key = 'new' + key[3:]

                if form_data[key] != form_data[new_key]:
                    if not changes[dom_type].has_key(dom_id):
                        changes[dom_type][dom_id] = {}

                    new_data = form_data[new_key]
                    new_data = unicode(new_data.encode('ascii', 'xmlcharrefreplace'))

                    changes[dom_type][dom_id][xpath] = new_data

        return changes['D'], changes['P'], changes['C']
