from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'front.views.index'),
)
urlpatterns += patterns('',
    url(r'^api/draw', 'api.views.draw'),
    url(r'^api/embedding', 'api.views.draw_embedding'),
)
