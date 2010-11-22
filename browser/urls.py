from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Root log
    (r'^(?P<repository>.*?)/log/$', 'codereview.browser.views.log'),
    # File (Blob) view
    (r'^(?P<repository>.*?)/blob/(?P<path>.*?)$', 'codereview.browser.views.blob'),
    # Path log
    (r'^(?P<repository>.*?)/log/(?P<path>.*?)/$', 'codereview.browser.views.log'),
    # Commit view
    (r'^(?P<repository>.*?)/commit/(?P<ref>.*?)/$',
        'codereview.browser.views.commit'),
)
