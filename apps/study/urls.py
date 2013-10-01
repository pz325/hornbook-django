# urlpatterns for hornbook_api
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.study.views',
    url(r'^$', 'index'),
    url(r'^api/$', 'api_index'),
    url(r'^save_study/$', 'save_study'),
    url(r'^get_study_between/$', 'get_study_between'),
)
