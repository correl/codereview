from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from haystack.views import search_view_factory
from codereview.dashboard.models import Repository
from codereview.review.models import Review

@permission_required('dashboard.browse')
def index(request):
    """ List available repositories
    """
    repositories = Repository.objects.all()
    reviews = Review.objects.all().order_by('-created')
    data = RequestContext(request, {
        'repositories': repositories,
        'reviews': reviews,
    })
    return render_to_response('dashboard/index.html', data) 
@permission_required('dashboard.browse')
def search(request):
    return search_view_factory()(request)
