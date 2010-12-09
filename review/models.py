from django.db import models
from django.contrib.auth.models import User
from codereview.dashboard.models import Repository

class Review(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __unicode__(self):
        return 'Review #{0}'.format(self.pk)
class Item(models.Model):
    review = models.ForeignKey(Review)
    repo = models.ForeignKey(Repository)
    ref = models.CharField(max_length=40)
    path = models.TextField()
class Comment(models.Model):
    item = models.ForeignKey(Item)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    blob = models.IntegerField()
    offset = models.IntegerField()
    text = models.TextField()
