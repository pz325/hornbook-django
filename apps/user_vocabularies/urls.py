# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.user_vocabularies.views',
    # url(r'^$', 'index'),
    url(r'^add_to_user_vocabulary/$', 'add_to_user_vocabulary'),
)
