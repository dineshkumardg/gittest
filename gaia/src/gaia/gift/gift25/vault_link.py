from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker, attr
from lxml.builder import ElementMaker


class _VaultLink(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self, namespace='http://www.gale.com/goldschema/vault-linking', nsmap={'vault-link' : 'http://www.gale.com/goldschema/vault-linking', }, **kwargs)

def vault_link(_link_type=None, _data_type=None, term_id=None, term_source=None, _category=None, _action=None, where_path=None, _target=None, _display_point=None, _display_link=None):
    vault_links = []

    if _link_type is not None:
        vault_links.append(link_type(_link_type))

    if _category is not None:                
        vault_links.append(link_category(
            attr('term-id', term_id),
            attr('term-source', term_source),
            _category
            )
        )

    if _data_type is not None:
        vault_links.append(data_type(_data_type))

    if _action is not None:
        vault_links.append(action(_action))

    if where_path is not None:
        vault_links.append(where(
            path(where_path)
            )
        )

    if _target is not None:
        vault_links.append(select(
            document_nodes(target(_target)
                )
            )
        )

    if _display_point is not None:
        vault_links.append(display_point(_display_point))

    if _display_link is not None:
        vault_links.append(display_link(_display_link))

    return _vault_link(*vault_links)

E = _VaultLink()
_vault_link = E.vault_link
link_type = E.link_type
data_type = E.data_type
action = E.action
where = E.where
path = E.path
link_category = E.link_category
select = E.select
document_nodes = E.document_nodes
target = E.target
display_point = E.display_point
display_link = E.display_link
