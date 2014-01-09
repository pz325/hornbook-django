# urlpatterns for dashboard
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.dashboard.views',
    url(r'^$', 'index'),
    #url(r'^api.html$', 'api_index'),
    url(r'^get_statistics/$', 'get_statistics'),
    # url(r'^all_most_common_characters/$', 'get_all_most_common_characters'),
    # url(r'^most_common_word/$', 'get_most_common_word'),   
)