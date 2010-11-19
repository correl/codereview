from django.shortcuts import render_to_response
from codereview.dashboard.models import Repository

def index(request):
    """ List available repositories
    """
    repositories = Repository.objects.all()
    return render_to_response('dashboard/index.html',
            {'repositories': repositories})
