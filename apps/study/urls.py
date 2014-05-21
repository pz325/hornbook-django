# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.study.views',
    url(r'^$', 'index'),
    url(r'^new/$', 'learn_new'),
    url(r'^recap/$', 'recap'),
    
    url(r'^api.html/$', 'api_index'),
    url(r'^save_new_study/$', 'save_new_study'),
    url(r'^save_revise/$', 'save_revise'),
    url(r'^add_grasped/$', 'add_grasped'),
    url(r'^get_study_between/$', 'get_study_between'),
    url(r'^get_all/$', 'get_all'),
    url(r'^get_study_intelligent/$', 'get_study_intelligent'),
    url(r'^get_statistics/$', 'get_statistics'),
    url(r'^get_new_from_500/$', 'get_new_from_500'),
)
