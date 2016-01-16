from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'front.views.index'),
    url(r'^results/diagram', 'front.views.diagram'),
    url(r'^results', 'front.views.results'),
    url(r'^unrooted/results', 'front.views.unrooted_results'),
    url(r'^unrooted', 'front.views.unrooted_index'),

)
urlpatterns += patterns('',
    url(r'^api/draw/', 'api.views.draw'),
    url(r'^api/embedding/', 'api.views.draw_embedding'),
    url(r'^api/diagram/', 'api.views.draw_diagram'),
    url(r'^api/unrooted/', 'api.views.draw_unrooted'),
)

