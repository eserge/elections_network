from django.conf.urls.defaults import *

urlpatterns = patterns('locations.views',
    url(r'^(?P<loc_id>\d+)$', 'location', name='location_info', kwargs={'view': 'location_info'}),
    url(r'^(?P<loc_id>\d+)/wall$', 'location', name='location_wall', kwargs={'view': 'location_wall'}),
    url(r'^(?P<loc_id>\d+)/map$', 'location', name='location_map', kwargs={'view': 'location_map'}),
    url(r'^(?P<loc_id>\d+)/help$', 'location', name='location_help', kwargs={'view': 'location_help'}),

    url(r'^get_sub_regions$', 'get_sub_regions', name='get_sub_regions'),
    url(r'^goto_location$', 'goto_location', name='goto_location'),
)
