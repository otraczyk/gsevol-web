from django.conf.urls import patterns, include, url

from front import views as front_views
from api import views as api_views

urlpatterns = [
    url(r'^$', front_views.index),
    url(r'^rooted/diagram', front_views.diagram),
    url(r'^rooted', front_views.index),
    url(r'^unrooted', front_views.unrooted_index),
]

urlpatterns += [
    url(r'^api/draw/', api_views.draw),
    url(r'^api/embedding/', api_views.draw_embedding),
    url(r'^api/diagram/', api_views.draw_diagram),
    url(r'^api/unrooted/', api_views.draw_unrooted),
]
