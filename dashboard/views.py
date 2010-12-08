from django.shortcuts import render_to_response
from django.template import RequestContext
from codereview.dashboard.models import Repository

def index(request):
    """ List available repositories
    """
    repositories = Repository.objects.all()
    data = RequestContext(request, {
        'repositories': repositories,
    })
    return render_to_response('dashboard/index.html', data) 
