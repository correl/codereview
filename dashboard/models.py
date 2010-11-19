from django.db import models
from codereview.lib import vcs

class Repository(models.Model):
    Types = {
            'Git': 0,
            }
    name = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=255)
    type = models.IntegerField(default=0)

    def get_vcs(self):
        if self.type == 0:
            return vcs.Git(self.path)
        else:
            raise Exception('Invalid VCS type')
