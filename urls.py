from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from front import views as front_views
from api import views as api_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/rooted')),
    url(r'^rooted/diagram', front_views.diagram),
    url(r'^rooted', front_views.index),
    url(r'^unrooted', front_views.unrooted_index),
    url(r'^scenario', front_views.scenario_index),
]

urlpatterns += [
    url(r'^api/draw/', api_views.draw),
    url(r'^api/draw_single/', api_views.draw_single),
    url(r'^api/embedding/', api_views.draw_embedding),
    url(r'^api/diagram/', api_views.draw_diagram),
    url(r'^api/unrooted/', api_views.draw_unrooted),
    url(r'^api/scenario/', api_views.scenario),
    url(r'^api/options/', api_views.options),
    url(r'^api/restyle/', api_views.restyle),
]
