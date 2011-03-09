from collections import deque
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
            print 'Updating', branch
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
    diffs = models.ManyToManyField('Diff')

    def load(self, repo):
        queue = deque([self])
        while queue:
            c = queue.popleft()
            commit = repo.commit(c.ref)
            c.message = commit.message
            c.author = commit.author
            c.author_email = commit.author_email
            c.committer = commit.committer
            c.committer_email = commit.committer_email
            c.authored_date = commit.authored_date
            c.committed_date = commit.committed_date
            c.save()
            print 'Loading', c.ref
            for parent in commit.parents:
                try:
                    p = Commit.objects.get(ref=parent, repository=c.repository)
                except:
                    p = Commit(ref=parent, repository=c.repository)
                    parent = repo.commit(parent)
                    p.message = parent.message
                    p.author = parent.author
                    p.author_email = parent.author_email
                    p.committer = parent.committer
                    p.committer_email = parent.committer_email
                    p.authored_date = parent.authored_date
                    p.committed_date = parent.committed_date
                    p.save()
                    queue.append(p)
                    print 'Queuing', p.ref
                c.parents.add(p)
            if not c.diffs.all():
                print 'Diffing', c.ref
                try:
                    for diff in repo.diff(c.ref):
                        d = Diff()
                        d.load(diff)
                        d.save()
                        c.diffs.add(d)
                except:
                    pass
            c.save()
    def __unicode__(self):
        return self.ref

class Diff(models.Model):
    context = models.IntegerField(default=3)
    path_a = models.TextField()
    path_b = models.TextField()
    
    def load(self, diff):
        self.context = diff.context
        if diff.a:
            self.path_a = diff.a.path
        if diff.b:
            self.path_b = diff.b.path
        self.save()
        for change in diff.changes():
            c = Change()
            c.diff = self
            c.type = change['type']
            c.text = change['text']
            c.line_a = change['line_a']
            c.line_b = change['line_b']
            c.save()

class Change(models.Model):
    diff = models.ForeignKey(Diff)
    type = models.CharField(max_length=1)
    text = models.TextField()
    line_a = models.IntegerField()
    line_b = models.IntegerField()

class Head(models.Model):
    repository = models.ForeignKey(Repository)
    commit = models.ForeignKey(Commit)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
