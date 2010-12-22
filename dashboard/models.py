from django.db import models
from codereview.browser import vcs

class Repository(models.Model):
    name = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=255)
    type = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ("browse", "Browse repositories"),
        )

    def update(self):
        repo = vcs.create(self.type, self.path)
        branches = repo.branches()
        for branch, commit in branches.iteritems():
            try:
                head = Head.objects.get(repository=self, name=branch)
            except:
                head = Head(repository=self, name=branch)
            try:
                c = Commit.objects.get(repository=self, ref=commit.id)
            except:
                c = Commit(repository=self, ref=commit.id)
            c.load(repo)
            head.commit = c
            head.save()
    def __unicode__(self):
        return self.name

class Commit(models.Model):
    ref = models.CharField(max_length=40)
    repository = models.ForeignKey(Repository)
    message = models.TextField()
    author = models.CharField(max_length=255)
    author_email = models.CharField(max_length=255)
    committer = models.CharField(max_length=255)
    committer_email = models.CharField(max_length=255)
    authored_date = models.DateTimeField()
    committed_date = models.DateTimeField()
    parents = models.ManyToManyField('self')

    def load(self, repo):
        commit = repo.commit(self.ref)
        self.message = commit.message
        self.author = commit.author
        self.author_email = commit.author_email
        self.committer = commit.committer
        self.committer_email = commit.committer_email
        self.authored_date = commit.authored_date
        self.committed_date = commit.committed_date
        self.save()
        for parent in commit.parents:
            try:
                p = Commit.objects.get(ref=parent, repository=self.repository)
            except:
                p = Commit(ref=parent, repository=self.repository)
                p.load(repo)
            self.parents.add(p)
        self.save()
    def __unicode__(self):
        return self.ref

class Head(models.Model):
    repository = models.ForeignKey(Repository)
    commit = models.ForeignKey(Commit)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
