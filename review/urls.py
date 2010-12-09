from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^new/$', 'codereview.review.views.new'),
    (r'^edit/(?P<review_id>\d+)/$', 'codereview.review.views.edit'),
)
