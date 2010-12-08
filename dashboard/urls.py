from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login'),
)
