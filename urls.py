from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from front import views as front_views
from api import views as api_views
from styling import views as styling_views

from styling.admin import admin_site

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/rooted')),
    url(r'^admin/', include(admin_site.urls)),
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
    url(r'^api/options/', styling_views.options),
    url(r'^api/restyle/', styling_views.restyle),
]
