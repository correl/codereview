from django.http import Http404
from django.shortcuts import render_to_response
from codereview.dashboard.models import Repository

def log(request,repository):
    try:
        repo = Repository.objects.get(name=repository)
    except:
        raise Http404
    vcs = repo.get_vcs()
    ref = request.GET['c'] if 'c' in request.GET else vcs.ref()
    offset = int(request.GET['o']) if 'o' in request.GET else 0
    limit = 20
    log = vcs.log(ref, max=limit, offset=offset)

    newer = offset - limit if offset > limit else 0
    # Inspect the last commit. If it has no parents, we can't go any further
    # back.
    last = log[-1]
    older = offset + limit if last.parents else 0

    return render_to_response('browser/log.html',
            {
                'repository': repository,
                'vcs': vcs,
                'log': log,
                'ref': ref,
                'offset': offset,
                'newer': newer,
                'older': older,
            })
def view(request, repository, ref):
    try:
        repo = Repository.objects.get(name=repository)
    except:
        raise Http404
    vcs = repo.get_vcs()
    commit = vcs.commit(ref)
    diffs = vcs.diff(ref)

    return render_to_response('browser/view.html',
            {
                'repository': repository,
                'vcs': vcs,
                'ref': ref,
                'commit': commit,
                'diffs': diffs,
            })
