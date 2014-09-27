# urlpatterns for dashboard
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.leitner.views',
    ###url(r'^$', 'index'),     # generate an overview of study
    url(r'^add/$', 'add'),   # add new Hanzi to Leitner system
    url(r'^get/$', 'get'),   # return list of Hanzi to recall
    url(r'^update/$', 'update'),   # update Hanzi level, or moving around decks
    url(r'^count/$', 'count'),   # return count Hanzi in a level
    url(r'^remove_duplicate/$', 'remove_duplicate'), # admin api, remove duplicate
)