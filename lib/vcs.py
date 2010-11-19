import difflib
from datetime import datetime

class VCS(object):
    def __init__(self, path):
        self._path = path
        self._ref = None
    def branches(self):
        return []
    def tags(self):
        return []
    def ref(self):
        return self._ref
    def log(self, commit=None, path=None, max=50, offset=0):
        return []

class Blob(object):
    def __init__(self, path, data):
        self.path = path
        self.data = data

class Diff(object):
    Types = {
            'Add': 0,
            'Delete': 1,
            'Rename': 2,
            'Modify': 3,
            }
    def __init__(self):
        self.a = None
        self.b = None
        self.type = 0
    def unified(self):
        a = self.a.data.split('\n') if self.a else []
        b = self.b.data.split('\n') if self.b else []
        diff = difflib.unified_diff(
                a,
                b,
                fromfile=self.a.path,
                tofile=self.b.path)
        return '\n'.join(diff)
    def changes(self, context=3):
        a = self.a.data.split('\n') if self.a else []
        b = self.b.data.split('\n') if self.b else []
        differ = difflib.Differ()

        # Locate changes so we can mark context lines
        i = 0
        changes = []
        for change in differ.compare(a, b):
            if change[0] in ['+', '-']:
                changes.append(i)
            i += 1

        i = 0
        line_a = 0
        line_b = 0
        for change in differ.compare(a, b):
            type = change[:2].strip()
            text = change[2:]
            if type == '?':
                # Change information. Discard it for now.
                i += 1
                print 'skip ?'
                continue
            if type == '+':
                line_b += 1
            elif type == '-':
                line_a += 1
            else:
                line_a += 1
                line_b += 1
            if context and not type:
                # Check to see if we're in range of a change
                nearby = [c for c in changes if abs(i - c) <= context + 1]
                if not nearby:
                    i += 1
                    print 'skip nc'
                    continue
            result = {
                    'type': type,
                    'line_a': line_a,
                    'line_b': line_b,
                    'text': text,
                    }
            yield result
            i += 1
    def html(self):
        a = self.a.data.split('\n') if self.a.data else []
        b = self.b.data.split('\n') if self.b.data else []
        h = difflib.HtmlDiff()
        diff = h.make_table(
                a,
                b,
                fromdesc=self.a.path,
                todesc=self.b.path,
                context=True)
        return diff

class Commit(object):
    def __init__(self):
        self.id = None
        self.tree = None
        self.message = None
        self.author = None
        self.author_email = None
        self.committer = None
        self.committer_email = None
        self.authored_date = None
        self.committed_date = None
        self.parents = []

import git
class Git(VCS):
    def __init__(self, path):
        super(Git, self).__init__(path);
        self._repo = git.Repo(self._path)
        self._branches = None
        self._tags = None

        # Set default branch ref
        if 'master' in self.branches():
            self._ref = 'master'
        else:
            self.ref = self.branches()[0]
    def branches(self):
        if not self._branches:
            self._branches = dict([(head.name, self.commit(head.commit)) for head in self._repo.heads])
        return self._branches
    def tags(self):
        if not self._tags:
            self._tags = dict([(tag.name, self.commit(tag.commit)) for tag in self._repo.tags])
        return self._tags
    def commit(self, commit):
        if type(commit) in [str, unicode]:
            commit = self._repo.commit(commit)
        c = Commit()
        c.id = commit.hexsha
        c.tree = commit.tree.hexsha
        c.message = commit.message
        c.author = commit.author.name
        c.author_email = commit.author.email
        c.committer = commit.committer.name
        c.committer_email = commit.committer.email
        c.authored_date = datetime.fromtimestamp(commit.authored_date)
        c.committed_date = datetime.fromtimestamp(commit.committed_date)
        c.parents = [parent.hexsha for parent in commit.parents]
        return c
    def log(self, commit=None, path=None, max=50, offset=0):
        commit = commit if commit else self._ref
        result = []
        for c in self._repo.iter_commits(commit, path, max_count=max,
                skip=offset):
            result.append(self.commit(c))
        return result
    def diff(self, b, a=None):
        """Get the diff for ref b from ref a

        If ref a is not provided, b's parent refs will be used.

        *** Note: The parameter order is backwards, since we default the origin
        ref to the target's parents.
        """
        result = []
        b = self._repo.commit(b)
        if not a:
            # FIXME:
            # Only using the first parent for now. Some merge commits seem to be
            # causing nasty problems, while others diff just fine.
            a = b.parents[:1]
        else:
            a = self._repo.commit(a)
        for diff in b.diff(a):
            # b and a are swapped so the parent diff will work as a list of
            # parents. Therefore, we'll swap them back when we put them into our
            # Diff object.
            d = Diff()
            if diff.a_blob: d.b = Blob(diff.a_blob.path,
                    diff.a_blob.data_stream.read())
            if diff.b_blob: d.a = Blob(diff.b_blob.path,
                    diff.b_blob.data_stream.read())
            result.append(d)
        return result

if __name__ == '__main__':
    g = Git('/home/correlr/code/voiceaxis')
