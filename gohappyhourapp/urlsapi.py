from django.conf.urls import include,url
from rest_framework.urlpatterns import format_suffix_patterns
from gohappyhourapp import viewsapi


urlpatterns = [
	url(r'^users/', include('rest_auth.urls')),
    url(r'^users/registration/', include('rest_auth.registration.urls')),
	url(r'^users/facebook/$', viewsapi.FacebookLogin.as_view(), name='fb_login'),
    url(r'^users/google/$', viewsapi.GoogleLogin.as_view(), name='google_login'),
    url(r'^locations/$', viewsapi.LocationList.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/$', viewsapi.LocationDetail.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/detail$', viewsapi.LocationFullDetail.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/externalpictures$', viewsapi.LocationExternalPictures.as_view()),
    url(r'^locations/addgoogleplace$', viewsapi.LocationAddGoogle.as_view()),
	url(r'^locations/search$', viewsapi.LocationListSearch.as_view()),
    url(r'^locations/distribution$', viewsapi.LocationListDistribution.as_view()),
    url(r'^locations/searchplaces$', viewsapi.LocationListSearchPlaces.as_view()),

    
    url(r'^locations/(?P<location_pk>[0-9]+)/pictures/$', viewsapi.LocationPictureList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/pictures/upload$', viewsapi.UploadPictureLocation.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/pictures/(?P<pk>[0-9]+)/$', viewsapi.LocationPictureDetail.as_view()),
    
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/$', viewsapi.OfferList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<pk>[0-9]+)/$', viewsapi.OfferDetail.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<pk>[0-9]+)/detail$', viewsapi.OfferFullDetail.as_view()),

    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/pictures/$', viewsapi.OfferPictureList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/pictures/upload$', viewsapi.UploadPictureOffer.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/pictures/(?P<pk>[0-9]+)/$', viewsapi.OfferPictureDetail.as_view()),
    
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/timeranges/$', viewsapi.OfferTimeRangeList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/timeranges/(?P<pk>[0-9]+)/$', viewsapi.OfferTimeRangeDetail.as_view()),
       
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/votes/$', viewsapi.OfferUserVoteList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/votes/(?P<pk>[0-9]+)/$', viewsapi.OfferUserVoteDetail.as_view()),
    url(r'^users/user/votes/$', viewsapi.UserVoteList.as_view()),
    url(r'^users/user/votes/(?P<pk>[0-9]+)/$', viewsapi.OfferUserVoteDetail.as_view()),

    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/comments/$', viewsapi.OfferUserCommentList.as_view()),
    url(r'^locations/(?P<location_pk>[0-9]+)/offers/(?P<offer_pk>[0-9]+)/comments/(?P<pk>[0-9]+)/$', viewsapi.OfferUserCommentDetail.as_view()),
    url(r'^users/user/comments/$', viewsapi.UserCommentList.as_view()),
    url(r'^users/user/comments/(?P<pk>[0-9]+)/$', viewsapi.OfferUserCommentDetail.as_view()),
    
    
	
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]