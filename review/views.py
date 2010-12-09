from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from codereview.browser import vcs
from codereview.dashboard.models import Repository
from codereview.review.models import Review, Item, Comment
from codereview.review.forms import NewCommitReviewForm

@permission_required('review.add_review')
def new(request):
    if not request.POST:
        raise Http404
    form = NewCommitReviewForm(request.POST)
    if form.is_valid():
        repository = Repository.objects.get(pk=form.cleaned_data['repo'])
        repo = vcs.create(repository.type, repository.path)
        commit = repo.commit(form.cleaned_data['ref'])
        description = commit.message.split('\n')[0].strip()
        review = Review.objects.create(author=request.user,
                description=commit.message)
        item = Item.objects.create(
                review=review,
                repo=repository,
                ref=commit.id)
        return HttpResponseRedirect(reverse(edit, args=[review.pk]))
@permission_required('review.change_review')
def edit(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
    except:
        raise Http404
    # TODO: Support multiple items per review (?)
    item = review.item_set.get()
    repo = vcs.create(item.repo.type, item.repo.path)
    commit = repo.commit(item.ref)
    diffs = repo.diff(commit.id)
    data = RequestContext(request, {
        "review": review,
        "commit": commit,
        "diffs": diffs,
    })
    return render_to_response('review/edit.html', data)
