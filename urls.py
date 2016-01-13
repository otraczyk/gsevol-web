from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'front.views.index'),
    url(r'^results', 'front.views.results'),
)
urlpatterns += patterns('',
    url(r'^api/draw', 'api.views.draw'),
    url(r'^api/embedding', 'api.views.draw_embedding'),
    url(r'^api/diagram', 'api.views.draw_diagram'),
)
