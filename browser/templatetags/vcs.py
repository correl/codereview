import os
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def oneline(value):
    line = value.split('\n')[0].strip()
    return line

@register.filter
@stringfilter
def lines(value):
    return value.split('\n')

@register.filter
@stringfilter
def dirname(value):
    return os.path.dirname(value)

@register.filter
@stringfilter
def basename(value):
    return os.path.basename(value)
