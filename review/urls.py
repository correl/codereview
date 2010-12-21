from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<review_id>\d+)/$', 'codereview.review.views.edit'),
    (r'^new/$', 'codereview.review.views.new'),
    (r'^comment/new/$', 'codereview.review.views.add_comment'),
    (r'^comment/respond/$', 'codereview.review.views.add_response'),
)
