from models import *

from serializers import *
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
import numpy as np
import geocalcs as gc
import imageutils as iu
import requests
import json
from scipy.misc import imread, imsave, imresize
from django.conf import settings
import os
from PIL import Image
import time
import offernow as on
import votes as vot
from rest_framework.response import Response
from rest_framework import status
import scipy.stats




from datetime import datetime
import pytz   


from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView as SocialLogin
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Time zone for coordinates could not be found.'

class PlaceUnavailable(APIException):
    status_code = 503
    default_detail = 'Place id could not be found in google.'

class LocationAlreadyExists(APIException):
    status_code = 409
    default_detail = 'Location already in database.'

class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter
    
class GoogleLogin(SocialLogin):
    adapter_class = GoogleOAuth2Adapter

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LocationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    def perform_create(self, serializer):       

        lat=float(self.request.data['latitude'])
        lng=float(self.request.data['longitude']) 
        try:                   
            r = requests.get("http://api.geonames.org/timezoneJSON?lat=%g&lng=%g&username=gohappyhour"%(lat,lng))   
            data = json.loads(r.text)  
        except:
            raise  ServiceUnavailable()
            return
        serializer.save(owner=self.request.user,timezoneid=data['timezoneId'],origin=Location.GOHAPPYHOUR)


class LocationAddGoogle(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = LocationAddGoogleSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(self.finalserializer.data)
        if self.conflict:
            return Response(self.finalserializer.data, status=status.HTTP_409_CONFLICT, headers=headers)
        else:
            return Response(self.finalserializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):    
   
        placeid = self.request.data.get('placeid', None)
        #API_KEY=''
        API_KEY=''#Api key google maps
        if placeid is not None:             
            try: 

                try:
                    alreadyexisting=Location.objects.get(origin=Location.GOOGLEPLACES,originid=placeid)  
                    queryset=alreadyexisting
                    self.finalserializer= LocationAddGoogleSerializer(alreadyexisting)
                    self.conflict=True
                    return 
                except:
                    pass    

                self.conflict=False
                self.finalserializer= serializer
                r = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s"%(placeid,API_KEY))   
                data = json.loads(r.text) 
                name=data['result']['name']
                lat=data['result']['geometry']['location']['lat']
                lng=data['result']['geometry']['location']['lng']
                address=data['result'].get('formatted_address','')
                country=FindAddressComponent(data['result']['address_components'],'country')
                postcode=FindAddressComponent(data['result']['address_components'],'postal_code')
                phonenumber=data['result'].get('international_phone_number','')
                if not phonenumber:
                    phonenumber=data['result'].get('formatted_phone_number','')
                website=data['result'].get('website','')

                #To Do
                #Country and Post Code
                #Place id in new field in databasa
                
                try:                   
                    r = requests.get("http://api.geonames.org/timezoneJSON?lat=%g&lng=%g&username=gohappyhour"%(lat,lng))   
                    geodata = json.loads(r.text)  
                    timezoneid=geodata['timezoneId']
                except:
                    raise ServiceUnavailable()
                    return                  

            except:
                raise  PlaceUnavailable()
                return


            try:
                location=serializer.save(owner=self.request.user,name=name,latitude=lat,longitude=lng,address=address,phonenumber=phonenumber,postcode=postcode,country=country,timezoneid=timezoneid,origin=Location.GOOGLEPLACES,originid=placeid,website=website)
                #We try to store the picture              
                try:
                    #Decide on a photo
                    maxSizePhoto=0
                    maxSizeInd=-1
                    for i in range(len(data['result']['photos'])):
                        sizeAux=int(data['result']['photos'][i]['height'])*int(data['result']['photos'][i]['width'])
                        if sizeAux>maxSizePhoto:
                            maxSizePhoto=sizeAux
                            maxSizeInd=i

                    if (maxSizeInd>=0):
                        photoreference=data['result']['photos'][maxSizeInd]['photo_reference']
                        locationpicture=LocationPicture(owner=self.request.user, location=location,origin=LocationPicture.GOOGLEPLACES,originid=photoreference)
                        locationpicture.save()

                        r = requests.get("https://maps.googleapis.com/maps/api/place/photo?maxwidth=1000&photoreference=%s&key=%s"%(photoreference,API_KEY))  
                        imageurl=r.url
                        filename = str(location.id)
                        extension=os.path.splitext(imageurl)[1]
                        if extension=="":
                            extension='.jpg'
                        
                        temp=NamedTemporaryFile(suffix=extension)
                        
                        tempfilename=temp.name
                        temp.write(r.content)

                        im = Image.open(tempfilename)
                        temp.close()  
                        im.thumbnail(iu.ObtainSizeLocationPicture(im.size[0],im.size[1]))
                        im.save(tempfilename)

                        reopen = open(tempfilename, 'rb')
                        django_picture = ImageFile(reopen)
                        locationpicture.picture.save(filename+extension, django_picture, save=True)
                        reopen.close()                         
                                            
                        im = Image.open(tempfilename)
                        temp.close() 
                        im.thumbnail(iu.ObtainSizeLocationThumbnail(im.size[0],im.size[1]))
                        im.save(tempfilename)
                        
                        reopen = open(tempfilename, 'rb')
                        django_picture = ImageFile(reopen)
                        locationpicture.thumbnail.save(filename+extension, django_picture, save=True)
                        reopen.close()                    
                                                    
                        os.remove(tempfilename)
                                                         
                except:
                    pass
            except:
                raise LocationAlreadyExists()
                return

        else:
            raise PlaceUnavailable()
            return

def FindAddressComponent(components,field):
    for component in components:
        if field in component['types']:
            return component['short_name']
    return None
            

class LocationListSearch(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = LocationSearchSerializer        

    def get_queryset(self):
        queryset = Location.objects.all()
        latval = self.request.query_params.get('lat', None)
        longval = self.request.query_params.get('long', None)
        radius = self.request.query_params.get('radius', 500)
        distance = self.request.query_params.get('distance', True)
        lat1 = self.request.query_params.get('lat1', None)
        lat2 = self.request.query_params.get('lat2', None)
        long1 = self.request.query_params.get('long1', None)
        long2 = self.request.query_params.get('long2', None)
        name = self.request.query_params.get('name', "")
        offernow = self.request.query_params.get('offernow', None)

        
        if radius is not None and latval is not None and longval is not None:
            radiusfilter=True
        else:
            radiusfilter=False

        if lat1 is not None and lat2 is not None and long1 is not None and long2 is not None:
            rangefilter=True
        else:
            rangefilter=False

        if (not radiusfilter) and (not rangefilter):
            distance=False

        if radiusfilter:
            radius=float(radius)
            latval=float(latval)
            longval=float(longval)
            latval=gc.NormalizeLat(latval)
            longval=gc.NormalizeLat(longval)
            dlong=gc.AngleAlongParallel(latval,longval,radius)            
            dlat=gc.AngleAlongMeridian(latval,longval,radius)

            long1=longval-dlong
            long2=longval+dlong
            lat2=latval+dlat
            lat1=latval-dlat
            queryset=QueryFilterRegion(queryset,lat1,long1,lat2,long2)


        if not radiusfilter and rangefilter:
            lat1=float(lat1)
            lat2=float(lat2)
            long1=float(long1)
            long2=float(long2)
            latval,longval,radius=gc.RangeToCenterRadius(lat1,lat2,long1,long2)
            queryset=QueryFilterRegion(queryset,lat1,long1,lat2,long2)

        if name:
            queryset=queryset.filter(name__regex=r'(?i)^.*(%s).*$'%name)

        if offernow == 'yes' or offernow == 'no' or offernow == 'anytime'  :
            for obj in queryset:
                time=on.TimeAtLocation(obj)
                obj.offernow=on.LocationOfferNow(obj,time)
            if offernow == 'yes':
                queryset=filter(lambda x: x.offernow == True, queryset)
            elif offernow == 'no':
                queryset=filter(lambda x: x.offernow == False, queryset)
            elif offernow == 'anytime':
                queryset=filter(lambda x: x.offernow == False or x.offernow == True, queryset)
                

        dists=[]
        for obj in queryset :
            if distance:
                distance=gc.DistanceTwoPoints(latval,longval,obj.latitude,obj.longitude)
                dists.append(distance)
                obj.distance = distance
            else:
                obj.distance = None

        if distance:
            dists=np.sort(np.array(dists))            
            queryset=sorted(queryset, key=lambda x: x.distance)   
            queryset=queryset[0:sum(dists<=radius)]

        return queryset



class UploadPictureOffer(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request,location_pk,offer_pk, format=None):
            location= get_object_or_404(Location, id=self.kwargs['location_pk'])
            offer= get_object_or_404(Offer, id=self.kwargs['offer_pk'],location=location)

            offerpicture=OfferPicture(owner=self.request.user, offer=offer,origin=OfferPicture.GOHAPPYHOUR)
            offerpicture.save()

            picture=request.FILES['picture']
            imageurl=picture.name

                     
            filename = str(offer.id)
            extension=os.path.splitext(imageurl)[1]
            if extension=="":
                extension='.jpg'
            
            temp=NamedTemporaryFile(suffix=extension)
            tempfilename=temp.name
            temp.write(picture.read())

            im = Image.open(tempfilename)
            temp.close()  
            im.thumbnail(iu.ObtainSizeOfferPicture(im.size[0],im.size[1]))
            im.save(tempfilename)

            reopen = open(tempfilename, 'rb')
            django_picture = ImageFile(reopen)
            offerpicture.picture.save(filename+extension, django_picture, save=True)
            reopen.close()                         
                       
            im = Image.open(tempfilename)
            temp.close()  
            im.thumbnail(iu.ObtainSizeOfferThumbnail(im.size[0],im.size[1]))
            im.save(tempfilename)
            
            reopen = open(tempfilename, 'rb')
            django_picture = ImageFile(reopen)
            offerpicture.thumbnail.save(filename+extension, django_picture, save=True)
            reopen.close()                    
                                        
            os.remove(tempfilename)

            
            return Response({'status':'image posted'})

class UploadPictureLocation(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request,location_pk, format=None):

            location= get_object_or_404(Location, id=self.kwargs['location_pk'])

            locationpicture=LocationPicture(owner=self.request.user, location=location,origin=LocationPicture.GOHAPPYHOUR)
            locationpicture.save()
            picture=request.FILES['picture']
            imageurl=picture.name

                     
            filename = str(location.id)
            extension=os.path.splitext(imageurl)[1]
            if extension=="":
                extension='.jpg'
            
            temp=NamedTemporaryFile(suffix=extension)
            tempfilename=temp.name
            temp.write(picture.read())

            im = Image.open(tempfilename)
            temp.close()  
            im.thumbnail(iu.ObtainSizeLocationPicture(im.size[0],im.size[1]))
            im.save(tempfilename)

            reopen = open(tempfilename, 'rb')
            django_picture = ImageFile(reopen)
            locationpicture.picture.save(filename+extension, django_picture, save=True)
            reopen.close()                         
                       
            im = Image.open(tempfilename)
            temp.close()  
            im.thumbnail(iu.ObtainSizeLocationThumbnail(im.size[0],im.size[1]))
            im.save(tempfilename)
            
            reopen = open(tempfilename, 'rb')
            django_picture = ImageFile(reopen)
            locationpicture.thumbnail.save(filename+extension, django_picture, save=True)
            reopen.close()                    
                                        
            os.remove(tempfilename)

            
            return Response({'status':'image posted'})


class LocationExternalPictures(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request,pk, format=None):
            maxresults= self.request.query_params.get('max_results', None)
            offset= self.request.query_params.get('offset', None)

            location= get_object_or_404(Location, id=self.kwargs['pk'])

            if location.origin==Location.GOOGLEPLACES:
                API_KEY='AIzaSyDZRjyT9CjgxGUdpEdEg1MQBztR-XF23vk'
                placeid=location.originid;

                r = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s"%(placeid,API_KEY))   
                data = json.loads(r.text) 


                photos=data['result'].get('photos',[])

                count=0
                results=[]
                if offset is None:
                    offset=0
                else:
                    offset=int(offset)
                if maxresults is None:
                    maxresults=len(photos)
                else:
                    maxresults=int(maxresults)

                start=offset
                end=min(len(photos),offset+maxresults)

                for i in range(start,end,1):
                    photoreference=photos[i]['photo_reference']
                    r = requests.get("https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&photoreference=%s&key=%s"%(photoreference,API_KEY))  
                    result={}
                    result['url']=r.url

                    results.append(result)
                    count+=1;
                return Response({'count':count,'results':results})


            return Response({'count':0,'results':{}})

class LocationListDistribution(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):

        lat1 = self.request.query_params.get('lat1', None)
        lat2 = self.request.query_params.get('lat2', None)
        long1 = self.request.query_params.get('long1', None)
        long2 = self.request.query_params.get('long2', None)
        latbins = int(self.request.query_params.get('latbins', 20))
        longbins = int(self.request.query_params.get('longbins', 20))
        offernow = self.request.query_params.get('offernow', None)
        queryset = Location.objects.all()

        if lat1 is not None and lat2 is not None and long1 is not None and long2 is not None:
            rangefilter=True
        else:
            rangefilter=False

        if rangefilter:
            lat1=float(lat1)
            lat2=float(lat2)
            long1=float(long1)
            long2=float(long2)
            queryset=QueryFilterRegion(queryset,lat1,long1,lat2,long2)
        else:
            lat1=-90
            lat2=90
            long1=-180
            long2=180

        queryset=QueryFilterRegion(queryset,lat1,long1,lat2,long2)

        if offernow == 'yes' or offernow == 'no' or offernow == 'anytime'  :
            for i,obj in enumerate(queryset):
                time=on.TimeAtLocation(obj)
                obj.offernow=on.LocationOfferNow(obj,time)
            if offernow == 'yes':
                queryset=filter(lambda x: x.offernow == True, queryset)
            elif offernow == 'no':
                queryset=filter(lambda x: x.offernow == False, queryset)
            elif offernow == 'anytime':
                queryset=filter(lambda x: x.offernow == False or x.offernow == True, queryset)


        longlist=np.array([obj.longitude for obj in queryset])
        latlist=np.array([obj.latitude for obj in queryset])

        latedges=np.linspace(lat1,lat2,latbins+1)
        if long1>long2:
            longlist[longlist<long2]=longlist[longlist<long2]+360
            long2=long2+360
        longedges=np.linspace(long1,long2,longbins+1)


        counthistall=scipy.stats.binned_statistic_2d(latlist, longlist, latlist, statistic='count', bins=[latedges,longedges])
        counthist=counthistall[0]
        counthistbinnumbers=counthistall[3]
        meanlathist=scipy.stats.binned_statistic_2d(latlist, longlist, latlist, statistic='mean', bins=[latedges,longedges])[0]
        meanlonghist=scipy.stats.binned_statistic_2d(latlist, longlist, longlist, statistic='mean', bins=[latedges,longedges])[0]

        distributionpoints=[]
        count=0
        totalcount=0

        for lati in range(latbins):
            for longi in range(longbins):
                if counthist[lati,longi]>0:
                    distributionpoint={
                        'count': counthist[lati,longi],
                        'latitude': meanlathist[lati,longi],
                        'longitude':meanlonghist[lati,longi]
                    }
                    if counthist[lati,longi]==1:
                        binnum=(longi+1)+(lati+1)*(longbins+2)
                        ind=np.where(binnum==counthistbinnumbers)[0][0]
                        distributionpoint['name']=queryset[ind].name
                        distributionpoint['offernow']=queryset[ind].offernow

                        distributionpoint["id"]=queryset[ind].id
                    distributionpoints.append(distributionpoint)
                    count+=1
                    totalcount+=counthist[lati,longi]

        return Response({'count':count,'totalcount':totalcount,'results':distributionpoints})        

class LocationListSearchPlaces(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        latval = self.request.query_params.get('lat', None)
        longval = self.request.query_params.get('long', None)
        radius = self.request.query_params.get('radius', 500)
        distance = self.request.query_params.get('distance', True)
        lat1 = self.request.query_params.get('lat1', None)
        lat2 = self.request.query_params.get('lat2', None)
        long1 = self.request.query_params.get('long1', None)
        long2 = self.request.query_params.get('long2', None)
        name = self.request.query_params.get('name', "")
        minresults = int(self.request.query_params.get('minresults', 10))
        tokennext = self.request.query_params.get('tokennext', None)
        
        if radius is not None and latval is not None and longval is not None:
            radiusfilter=True
        else:
            radiusfilter=False

        if lat1 is not None and lat2 is not None and long1 is not None and long2 is not None:
            rangefilter=True
        else:
            rangefilter=False

        if (not radiusfilter) and (not rangefilter):
            distance=False

        if radiusfilter:
            radius=float(radius)
            latval=float(latval)
            longval=float(longval)

        if not radiusfilter and rangefilter:
            lat1=float(lat1)
            lat2=float(lat2)
            long1=float(long1)
            long2=float(long2)
            latval,longval,radius=gc.RangeToCenterRadius(lat1,lat2,long1,long2)

        if (tokennext or radiusfilter or rangefilter):
            
            #API_KEY='AIzaSyCNqZ8zMCaviz4IbHHl87uIjx-jR1QA8sY'
            API_KEY='AIzaSyDZRjyT9CjgxGUdpEdEg1MQBztR-XF23vk'
            output={}

            output['results']=[]
            dists=[]
            count=0
            
            if tokennext:
                first=False
                next_page_token=tokennext
            else:
                first=True
            while first or next_page_token:
                types='bar|night_club'
                if first:
                    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%g,%g&radius=%g&type=%s&name=%s&key=%s"%(latval,longval,radius,types,name,API_KEY))            
                    first=False
                else:           
                    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=%s&pagetoken=%s"%(API_KEY,next_page_token,))
                data = json.loads(r.text) 

                next_page_token = data.get('next_page_token',None)

                for place in data['results']:
                    placeid=place['place_id']

                    try:
                        alreadyexisting=Location.objects.get(origin=Location.GOOGLEPLACES,originid=placeid) 
                        continue 
                    except:
                        pass

                    result={}
                    result['name']=place['name']
                    result['offernow']=False
                    result['placeid']=place['place_id']
                    
                    result['longitude']=place['geometry']['location']['lng']
                    result['latitude']=place['geometry']['location']['lat']

                    if distance:
                        distance=gc.DistanceTwoPoints(latval,longval,result['latitude'],result['longitude'])
                        dists.append(distance)
                        result['distance']=distance

                    output['results'].append(result)
                    count+=1
                if count >= minresults or not next_page_token:
                    break
                time.sleep(2)

            output['count']=count
            
            if distance:
                dists=np.sort(np.array(dists))            
                output['results']=sorted(output['results'], key=lambda x: x['distance'])   
                output['tokennext']=next_page_token
            return Response(output)
        

def QueryFilterRegion(queryset,lat1,long1,lat2,long2):
    lat1=gc.NormalizeLat(lat1)
    lat2=gc.NormalizeLat(lat2)
    if lat1>lat2:
        aux=lat1
        lat1=lat2
        lat2=aux
    long1=gc.NormalizeLong(long1)
    long2=gc.NormalizeLong(long2)

    if long2>=long1:
        queryset = queryset.filter(latitude__lte=lat2,latitude__gte=lat1,longitude__lte=long2,longitude__gte=long1);
    else: 
        queryset = queryset.filter(Q(latitude__lte=lat2)&Q(latitude__gte=lat1)&(Q(longitude__lte=long2) | Q(longitude__gte=long1)));
    return queryset
        
class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationFullDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationFullDataSerializer

class OfferFullDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Offer.objects.all()
    serializer_class = OfferFullDataSerializer
        
class OfferList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OfferSerializer
    
    def perform_create(self, serializer):
        location=Location.objects.get(id=self.kwargs['location_pk'])
        serializer.save(owner=self.request.user,location=location)
        
    def get_queryset(self):    
        queryset = Offer.objects.all()
        location=Location.objects.get(id=self.kwargs['location_pk'])
        queryset = queryset.filter(location=location)
        return queryset
        
class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    def get_object(self):
        obj= get_object_or_404(Offer, id=self.kwargs['pk'])
        return obj

class OfferPictureList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OfferPictureSerializer
        
    def get_queryset(self):    
        queryset = OfferPicture.objects.all()
        location=Offer.objects.get(id=self.kwargs['offer_pk'])
        queryset = queryset.filter(offer=offer)
        return queryset
        
class OfferPictureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = OfferPicture.objects.all()
    serializer_class = OfferPictureSerializer
    def get_object(self):
        obj= get_object_or_404(OfferPicture, id=self.kwargs['pk'])
        return obj


class LocationPictureList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = LocationPictureSerializer
        
    def get_queryset(self):    
        queryset = LocationPicture.objects.all()
        location=Location.objects.get(id=self.kwargs['location_pk'])
        queryset = queryset.filter(location=location)
        return queryset
        
class LocationPictureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = LocationPicture.objects.all()
    serializer_class = LocationPictureSerializer
    def get_object(self):
        obj= get_object_or_404(LocationPicture, id=self.kwargs['pk'])
        return obj


    
class OfferTimeRangeList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OfferTimeRangeSerializer
    def perform_create(self, serializer):
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        serializer.save(owner=self.request.user,offer=offer)
    def get_queryset(self):
        queryset = OfferTimeRange.objects.all()
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        queryset = queryset.filter(offer=offer)
        return queryset

        
class OfferTimeRangeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = OfferTimeRange.objects.all()
    serializer_class = OfferTimeRangeSerializer
    def get_object(self):
        obj= get_object_or_404(OfferTimeRange, id=self.kwargs['pk'])
        return obj
    
class OfferUserVoteList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OfferUserVoteSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(self.finalserializer.data)
        if self.conflict:
            return Response(self.finalserializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
        else:
            return Response(self.finalserializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):  
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])  
        try:
            alreadyexisting=OfferUserVote.objects.get(owner=self.request.user,offer=offer)  
            queryset=alreadyexisting
            value=self.request.data.get('value',None)
            if (value is not None):
                alreadyexisting.value=value
            alreadyexisting.save()
            self.finalserializer= OfferUserVoteSerializer(alreadyexisting)
            self.conflict=True 
        except:
            serializer.save(owner=self.request.user,offer=offer)
            self.finalserializer=serializer
            self.conflict=False

        votes,score=vot.CalculateScoreOffer(offer)
        offer.votes=votes
        offer.score=score
        offer.save()

    def get_queryset(self):
        queryset = OfferUserVote.objects.all()
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        return queryset.filter(offer=offer)
        
        
class OfferUserVoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = OfferUserVote.objects.all()
    serializer_class = OfferUserVoteSerializer
    
    def perform_update(self, serializer):
        #If a vote is going to be modified, we get the previous value
        serializer.save()
        
        #Using the previous value update the total score
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        votes,score=vot.CalculateScoreOffer(offer)
        offer.votes=votes
        offer.score=score
        offer.save()
        
    def perform_destroy(self, instance):
        instance.delete()
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        votes,score=vot.CalculateScoreOffer(offer)
        offer.votes=votes
        offer.score=score
        offer.save()
        

class UserVoteList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = OfferUserVote.objects.all()
    serializer_class = OfferUserVoteSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    


class OfferUserCommentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OfferUserCommentSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(self.finalserializer.data)
        if not self.valid:
            return Response({'info':'Message must contain some text'}, status=status.HTTP_406_NOT_ACCEPTABLE, headers=headers)
        if self.conflict:
            return Response(self.finalserializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
        else:
            return Response(self.finalserializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):  
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])  
        self.valid=True
        comment=self.request.data.get('comment',None)
        if (comment is None or comment==""):
            self.valid=False
            return
        try:
            alreadyexisting=OfferUserComment.objects.get(owner=self.request.user,offer=offer)  
            queryset=alreadyexisting            
            alreadyexisting.comment=comment
            alreadyexisting.save()
            self.finalserializer= OfferUserCommentSerializer(alreadyexisting)
            self.conflict=True 
        except:
            serializer.save(owner=self.request.user,offer=offer)
            self.finalserializer=serializer
            self.conflict=False

    def get_queryset(self):
        queryset = OfferUserComment.objects.all()
        offer=Offer.objects.get(id=self.kwargs['offer_pk'])
        return queryset.filter(offer=offer)
        
        
class OfferUserCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = OfferUserComment.objects.all()
    serializer_class = OfferUserCommentSerializer
    
    def perform_update(self, serializer):
        #If a vote is going to be modified, we get the previous value
        serializer.save()
        
    def perform_destroy(self, instance):
        instance.delete()
        

class UserCommentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = OfferUserComment.objects.all()
    serializer_class = OfferUserCommentSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 
