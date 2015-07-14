from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'front.views.index'),
    url(r'^demo/', 'front.views.demo'),
)
urlpatterns += patterns('',
    url(r'^api/draw', 'api.views.draw'),
)
