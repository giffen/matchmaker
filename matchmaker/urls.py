from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'^members/$', 'profiles.views.all', name='all'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='single_user'),
    url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
    (r'^edit/jobs$', 'profiles.views.edit_jobs'),
    (r'^edit/locations$', 'profiles.views.edit_locations'),
    url(r'^subscribe/$', 'profiles.views.subscribe', name='subscribe'),
    url(r'^questions/$', 'questions.views.all_questions', name='questions'),
    url(r'^inbox/$', 'directmessages.views.inbox', name='inbox'),
    url(r'^sent/$', 'directmessages.views.sent', name='sent'),

)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)