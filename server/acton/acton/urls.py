from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tasks.api import v1_api

urlpatterns = patterns('',
    # url(r'^$', 'acton.views.home', name='home'),
    # url(r'^acton/', include('acton.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
