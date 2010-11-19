from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<repository>.*?)/log/$', 'codereview.browser.views.log'),
    (r'^(?P<repository>.*?)/view/(?P<ref>.*?)/$', 'codereview.browser.views.view'),
)
