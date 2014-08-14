from django import template

register = template.Library()


@register.filter(name='get_bin_chunk')
def get_bin_chunk(d, key_name):
    ''' This template filter tag for the qa/item view only.

        This is required to lookup an item in a dictionary
        using a *variable* rather than a value.

        RE: https://code.djangoproject.com/ticket/3371
    '''
    if d.has_key(key_name):
        return d[key_name]
    else:
        return []
