from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from codereview.browser import vcs
from codereview.dashboard.models import Repository
from codereview.review.models import Review, Comment
from codereview.review.forms import NewReviewForm, CommentForm

@permission_required('review.add_review')
def new(request):
    if not request.POST:
        raise Http404
    form = NewReviewForm(request.POST)
    if form.is_valid():
        repository = Repository.objects.get(pk=form.cleaned_data['repo'])
        repo = vcs.create(repository.type, repository.path)
        commit = repo.commit(form.cleaned_data['ref'])
        if form.cleaned_data['description']:
            description = form.cleaned_data['description']
        else:
            description = commit.message.split('\n')[0].strip()
        if form.cleaned_data['parent']:
            parent = form.cleaned_data['parent']
        else:
            parent = commit.parents[0] if commit.parents else None
        review = Review.objects.create(
                author=request.user,
                repo=repository,
                ref=commit.id,
                parent=parent,
                description=description)
        return HttpResponseRedirect(reverse(edit, args=[review.pk]))
@permission_required('review.change_review')
def edit(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
    except:
        raise Http404
    repo = vcs.create(review.repo.type, review.repo.path)
    diffs = repo.diff(review.ref, review.parent if review.parent else None)
    data = RequestContext(request, {
        "review": review,
        "diffs": diffs,
    })
    return render_to_response('review/edit.html', data)
@permission_required('review.add_comment')
def add_comment(request):
    review_id = request.POST.get('review')
    try:
        review = Review.objects.get(pk=review_id)
        path = int(request.POST.get('path'))
    except:
        raise Http404
    repo = vcs.create(review.repo.type, review.repo.path)
    diffs = repo.diff(review.ref, review.parent if review.parent else None)

    form = CommentForm(request.POST)
    comment = form.save(commit=False)
    diff = diffs[path]
    comment.author = request.user
    comment.path = diff.b.path if diff.b else diff.a.path
    comment.save()
    data = RequestContext(request, {
        'comment': comment,
    })
    return render_to_response('components/comment.html', data)
