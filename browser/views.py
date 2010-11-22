import os
from django.http import Http404
from django.shortcuts import render_to_response
from codereview.dashboard.models import Repository
from codereview.browser import vcs

def log(request,repository, path=None):
    try:
        repository = Repository.objects.get(name=repository)
    except:
        raise Http404
    repo = vcs.create(repository.type, repository.path)
    ref = request.GET['c'] if 'c' in request.GET else repo.ref()
    offset = int(request.GET['o']) if 'o' in request.GET else 0
    limit = 20

    path = path if path else ''
    log = repo.log(ref, path=path, max=limit, offset=offset)
    navigation = dict(zip(('dirs', 'files'), repo.browse(ref, os.path.dirname(path))))

    newer = offset - limit if offset > limit else 0
    # Inspect the last commit. If it has no parents, we can't go any further
    # back.
    last = log[-1]
    older = offset + limit if last.parents else 0

    return render_to_response('browser/log.html',
            {
                'repository': repository,
                'path': path,
                'repo': repo,
                'log': log,
                'navigation': navigation,
                'ref': ref,
                'offset': offset,
                'newer': newer,
                'older': older,
            })
def view(request, repository, ref):
    try:
        repository = Repository.objects.get(name=repository)
    except:
        raise Http404
    repo = vcs.create(repository.type, repository.path)
    commit = repo.commit(ref)
    diffs = repo.diff(ref)

    return render_to_response('browser/view.html',
            {
                'repository': repository,
                'repo': repo,
                'ref': ref,
                'commit': commit,
                'diffs': diffs,
            })
