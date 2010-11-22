import os
import re
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

def create(type, path):
    cls = {
            0: Git,
    }.get(type, None)
    if not cls:
        raise Exception('Unknown VCS Type')
    return cls(path)

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
    def unified(self, context=3):
        a = self.a.data.split('\n') if self.a else []
        b = self.b.data.split('\n') if self.b else []
        diff = difflib.unified_diff(
                a,
                b,
                fromfile=self.a.path if self.a else '/dev/null',
                tofile=self.b.path if self.b else '/dev/null',
                n=context,
                lineterm='')
        return "\n".join(diff)
    def changes(self, context=3):
        "Parses the unified diff into a data structure for easy display"
        changes = []
        line_a = 0
        line_b = 0
        if context == None:
            context = max(
                    len(self.a.data.split('\n')) if self.a else 0,
                    len(self.b.data.split('\n')) if self.b else 0)
        for line in self.unified(context).split('\n')[2:]:
            if line.startswith('@@'):
                pattern = r'\-(\d+)(,\d+)? \+(\d+)(,\d+)?'
                info = re.findall(pattern, line)
                line_a = int(info[0][0])
                line_b = int(info[0][2])
                change = {
                        'type': '@',
                        'text': line,
                        'line_a': line_a,
                        'line_b': line_b,
                        }
                changes.append(change)
                continue
            type = line[0]
            text = line[1:]
            change = {
                    'type': type,
                    'text': text,
                    'line_a': line_a,
                    'line_b': line_b,
                    }
            if type == '+':
                line_b += 1
            elif type == '-':
                line_a += 1
            else:
                line_a += 1
                line_b += 1
            changes.append(change)
        return changes

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
    type = 'Git'
    def __init__(self, path):
        super(Git, self).__init__(path);
        self._repo = git.Repo(self._path)
        self._branches = None
        self._tags = None

        # Set default branch ref
        if 'master' in self.branches():
            self._ref = 'master'
        else:
            self._ref = self.branches()[0]
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
        for c in self._repo.iter_commits(rev=commit, paths=path, max_count=max,
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
    def browse(self, commit=None, path=''):
        if not commit:
            commit = self.ref()
        files = []
        dirs = []

        # Locate the tree matching the requested path
        tree = self._repo.commit(commit).tree
        if path:
            for i in tree.traverse():
                if type(i) == git.objects.Tree and i.path == path:
                    tree = i
        if path != tree.path:
            raise Exception('Path not found')

        for node in tree:
            if type(node) == git.objects.Blob:
                files.append(node.path)
            elif type(node) == git.objects.Tree:
                dirs.append(node.path)
        return dirs, files
    def blob(self, commit, path):
        tree = self._repo.commit(commit).tree
        dir = os.path.dirname(path)
        if dir:
            for i in tree.traverse():
                if type(i) == git.objects.Tree and i.path == dir:
                    tree = i
        if dir != tree.path:
            raise Exception('Path not found')
        for node in tree:
            if type(node) == git.objects.Blob and node.path == path:
                return Blob(node.path, node.data_stream.read())
        raise Exception('Blob Path not found')
if __name__ == '__main__':
    g = Git('/home/correlr/code/voiceaxis')
