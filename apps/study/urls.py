# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.study.views',
    url(r'^$', 'index'),
    url(r'^learnNew/$', 'learn_new'),
    url(r'^recap/$', 'recap'),
    
    url(r'^api.html/$', 'api_index'),
    url(r'^new_study/$', 'new_study'),
    url(r'^add_grasped/$', 'add_grasped'),
    url(r'^revise_study/$', 'revise_study'),
    url(r'^get_study_between/$', 'get_study_between'),
    url(r'^get_all/$', 'get_all'),
    url(r'^get_study_intelligent/$', 'get_study_intelligent'),
    url(r'^get_statistics/$', 'get_statistics'),
)
