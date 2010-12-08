import pam
from django.contrib.auth.models import User, Group

class PAMBackend:
    def authenticate(self, username=None, password=None):
        if pam.authenticate(username, password, service='login'):
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                # Create new django user
                user = User(username=username)
                user.set_password(password)
                user.save()
                user.groups.add(Group.objects.get(name='Users'))
                return user
        return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
