import hashlib
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def gravatar(value, size):
    email = value.strip().lower()
    hash = hashlib.md5(email).hexdigest()
    url = "http://www.gravatar.com/avatar/{hash}?s={size}&r={rating}".format(
            hash=hash,
            size=size,
            rating='g')
    return url
