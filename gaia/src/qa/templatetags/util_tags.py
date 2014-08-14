from django import template

register = template.Library()


@register.filter(name='slice_string')
def slice_string(value, arg):
    if value is None:
        return ''

    if len(value) > arg:
        return '%s...' % value[:int(arg) - 3]
    else:
        return value


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg
