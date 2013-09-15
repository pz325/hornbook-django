# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.hornbook_api.views',
    url(r'^most_common_character/$', 'get_most_common_character'),
    url(r'^all_most_common_characters/$', 'get_all_most_common_characters'),
    url(r'^most_common_word/$', 'get_most_common_word'),   
)
