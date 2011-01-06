from haystack.indexes import *
from haystack import site
from codereview.review.models import Review

class ReviewIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Review, ReviewIndex)
