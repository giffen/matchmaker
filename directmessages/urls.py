from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('directmessages.views',
		url(r'^compose/$', 'compose', name='compose'),
    url(r'^inbox/$', 'inbox', name='inbox'),
    url(r'^sent/$', 'sent', name='sent'),
    url(r'^view/(?P<dm_id>[\d]+)$', 'view_direct_message', name='view_direct_message'),
)
