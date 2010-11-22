from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<repository>.*?)/log/(?P<path>(.*?/)+)?$', 'codereview.browser.views.log'),
    (r'^(?P<repository>.*?)/view/(?P<ref>.*?)/$', 'codereview.browser.views.view'),
)
