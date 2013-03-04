from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from jsonrpc import jsonrpc_site

from tasks.api import v1_api
from tasks import views #loads the jsonrpc endpoints

urlpatterns = patterns('',
    url(r'^$', 'acton.views.home', name='home'),
    url(r'^inbox/.*$', 'acton.views.inbox', name='inbox'),
    url(r'^test/$', 'acton.views.test', name='test'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^rpc/v1/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
    url(r'^rpc/v1/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^rpc/v1/json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch), # for HTTP GET only, also omissible

    (r'^accounts/', include('registration.backends.default.urls')),

)

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
