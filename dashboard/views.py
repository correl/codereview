from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from codereview.dashboard.models import Repository

@permission_required('dashboard.browse')
def index(request):
    """ List available repositories
    """
    repositories = Repository.objects.all()
    data = RequestContext(request, {
        'repositories': repositories,
    })
    return render_to_response('dashboard/index.html', data) 
