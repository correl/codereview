import os
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from codereview.dashboard.models import Repository
from codereview.review.forms import NewCommitReviewForm
from codereview.browser import vcs

def _repo(request, name):
    try:
        repository = Repository.objects.get(name=name)
    except:
        raise Http404
    repo = vcs.create(repository.type, repository.path)
    ref = request.GET['c'] if 'c' in request.GET else repo.ref()
    return repo, ref
def _nav_data(request, repo, ref, path=None):
    path = path if path else ''
    navigation = dict(zip(('dirs', 'files'), repo.browse(ref, path)))
    return {'navigation': navigation}
def _log_data(request, repo, ref, path=None):
    offset = int(request.GET['o']) if 'o' in request.GET else 0
    limit = 20

    path = path if path else ''
    log = repo.log(ref, path=path, max=limit, offset=offset)

    newer = offset - limit if offset > limit else 0
    # Inspect the last commit. If it has no parents, we can't go any further
    # back.
    last = log[-1]
    older = offset + limit if last.parents else 0
    return {
            'path': path,
            'repo': repo,
            'log': log,
            'ref': ref,
            'offset': offset,
            'newer': newer,
            'older': older,
            }
@permission_required('dashboard.browse')
def log(request, repository, path=None):
    repo, ref = _repo(request, repository)
    data = RequestContext(request, {
        'repository': repository
    })
    data.update(_log_data(request, repo, ref, path))
    data.update(_nav_data(request, repo, ref, path))
    return render_to_response('browser/log.html', data)
@permission_required('dashboard.browse')
def commit(request, repository, ref):
    try:
        repository = Repository.objects.get(name=repository)
    except:
        raise Http404
    repo = vcs.create(repository.type, repository.path)
    commit = repo.commit(ref)
    diffs = repo.diff(ref)
    form = NewCommitReviewForm({
        'author': request.user.pk,
        'repo': repository.pk,
        'ref': ref
    })

    data = RequestContext(request, {
        'repository': repository,
        'repo': repo,
        'ref': ref,
        'commit': commit,
        'diffs': diffs,
        'form': form,
    })
    return render_to_response('browser/view.html', data)
@permission_required('dashboard.browse')
def diff(request, repository):
    if not request.GET:
        raise Http404
    if not request.GET['a']:
        raise Http404
    try:
        repository = Repository.objects.get(name=repository)
        repo = vcs.create(repository.type, repository.path)
        a = request.GET['a']
        commit_a = repo.commit(a)
        b = None
        if request.GET['b']:
            b = request.GET['b']
        elif commit_a.parents:
            b = commit_a.parents[0]
        commit_b = repo.commit(b)
        diffs = repo.diff(b, a)
    except:
        raise Http404
    data = RequestContext(request, {
        'repository': repository,
        'repo': repo,
        'a': commit_a,
        'b': commit_b,
        'diffs': diffs,
    })
    return render_to_response('browser/diff.html', data)
@permission_required('dashboard.browse')
def blob(request, repository, path):
    repo, ref = _repo(request, repository)
    data = RequestContext(request, {
        'repository': repository,
        'blob': repo.blob(ref, path),
    })
    data.update(_log_data(request, repo, ref, path))
    data.update(_nav_data(request, repo, ref, os.path.dirname(path)))
    return render_to_response('browser/blob.html', data)
