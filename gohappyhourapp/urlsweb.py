from django.conf.urls import include,url
from rest_framework.urlpatterns import format_suffix_patterns
from gohappyhourapp import viewsweb

urlpatterns = [

    url(r'^$', viewsweb.MapView),
    url(r'^map$', viewsweb.MapView),
    url(r'^locations/(?P<locid>[0-9]+)/$', viewsweb.MapView),
    url(r'^locations/(?P<locoption>[a-zA-Z]+)/$', viewsweb.MapView),
    url(r'^locations/(?P<locid>[0-9]+)/offers/(?P<offerid>[0-9]+)/$', viewsweb.MapView),
    url(r'^locations/(?P<locid>[0-9]+)/offers/(?P<offeroption>[a-zA-Z]+)/$', viewsweb.MapView),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]