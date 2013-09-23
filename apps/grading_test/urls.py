# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.grading_test.views',
    url(r'^$', 'index'),
)
