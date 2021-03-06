from django.conf.urls.defaults import *

# enable django admin
from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    
    # ('^$', 'django.views.generic.simple.direct_to_template',
    #  {'template': 'home.html'}),

    url(r'^$', 'apps.dashboard.views.index'),

    # log in/out
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'accounts/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    
    # Rest framewrok login/logout views
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^api/', include('apps.hornbook_api.urls')),
    url(r'^user_vocabularies/', include('apps.user_vocabularies.urls')),
    url(r'^grading_test/', include('apps.grading_test.urls')),
    url(r'^study/', include('apps.study.urls')),
    url(r'^leitner/', include('apps.leitner.urls')),
    url(r'^dashboard/', include('apps.dashboard.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
