from django.db import models
from django.contrib.auth.models import User
from codereview.dashboard.models import Repository
from codereview.browser import vcs

"""
Requirements: 

i. 
    Must be able to review a changeset as a collection of blobs at a certain
    revision, with diff information. Comments apply to any line of a unified diff
    containing all context.

     * Single revision plus parent revision
     * At least one valid (modified) path
     * Line based on diff with full context.

ii. 
    Must be able to review a blob or collection of blobs at a certain revision
    without diff information. Comments apply to any line of raw blob text.

     * Single revision
     * At least one valid path
     * Line based on raw path text
"""

class Review(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    repo = models.ForeignKey(Repository)
    ref = models.CharField(max_length=40)
    parent = models.CharField(max_length=40)

    def __unicode__(self):
        return 'Review #{0}'.format(self.pk)

class Comment(models.Model):
    review = models.ForeignKey(Review)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    line_a = models.IntegerField()
    line_b = models.IntegerField(null=True)
    text = models.TextField()
