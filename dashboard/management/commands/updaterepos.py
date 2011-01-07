import sys
from django.core.management.base import BaseCommand, CommandError
from codereview.dashboard.models import Repository

class Command(BaseCommand):
    args = '<repositoryname repositoryname ...>'
    help = 'Updates commit information in the database required for searching'

    def handle(self, *args, **options):
        repos = []
        if len(args):
            # Loop through the arguments to get the repos to update
            for arg in args:
                try:
                    repo = Repository.objects.get(name=arg)
                    if repo not in repos:
                        repos.append(repo)
                except:
                    print >> sys.stderr, "Unknown repository '%s'" % arg
        else:
            repos = Repository.objects.all()
        for repo in repos:
            print 'Updating repo', repo
            repo.update()
