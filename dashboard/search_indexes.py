from haystack.indexes import *
from haystack import site
from codereview.dashboard.models import Commit

class CommitIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Commit, CommitIndex)
