from django import template
register = template.Library()


@register.filter(name='as_range')
def as_range( value ):
    return [v + 1 for v in range(value)]
