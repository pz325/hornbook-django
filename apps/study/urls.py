# urlpatterns for hornbook_api
from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.study.models import ReadingViewSet, RecitationViewSet

router = routers.DefaultRouter()
router.register(r'readings', ReadingViewSet)
router.register(r'recitations', RecitationViewSet)

urlpatterns = patterns('apps.study.views',
    url(r'^api/', include(router.urls)),

    url(r'^$', 'index'),
    url(r'^new/$', 'learn_new'),
    url(r'^recap/$', 'recap'),
    
    url(r'^api.html/$', 'api_index'),
    url(r'^save_new_study/$', 'save_new_study'),
    url(r'^get_study_intelligent/$', 'get_study_intelligent'),
    url(r'^get_statistics/$', 'get_statistics'),
    url(r'^get_new_from_500/$', 'get_new_from_500'),
    url(r'^update/$', 'update'),

    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework'))
)
