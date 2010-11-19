from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def oneline(value):
    line = value.split('\n')[0].strip()
    return line
