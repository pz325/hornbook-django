from django.conf.urls.defaults import *

# enable django admin
from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),

    url(r'^api/most_common_character/$', 'apps.hornbook_api.views.get_most_common_character'),
    url(r'^api/all_most_common_characters/$', 'apps.hornbook_api.views.get_all_most_common_characters'),
    
    url(r'^admin/', include(admin.site.urls)),
)
