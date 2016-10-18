import numpy as np

EarthR=6371000


def NormalizeLat(lat):
    lat=np.max([-90,lat])
    lat=np.min([90,lat])
    return lat

def NormalizeLong(lon):
    if lon>180 or lon<-180:
        lon=np.mod(lon+180,360)-180
    return lon

def DistanceTwoPoints(lat1,long1,lat2,long2):

    lat1=NormalizeLat(lat1)/180*np.pi
    lat2=NormalizeLat(lat2)/180*np.pi

    long1=NormalizeLong(long1)/180*np.pi
    long2=NormalizeLong(long2)/180*np.pi
    
    dlat=lat1-lat2
    dlong=long1-long2

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlong/2)**2
    c = 2*np.arctan2( np.sqrt(a), np.sqrt(1-a) )
    return EarthR*c
    
def DistanceAlongParallel(lat,long1,long2):
    
    lat=lat/180*np.pi
    long1=np.mod(long1,360)/180*np.pi    
    long2=np.mod(long2,360)/180*np.pi
    
    dlong=long1-long2

    a = np.cos(lat)*np.cos(lat)*np.sin(dlong/2)**2
    c = 2*np.arctan2( np.sqrt(a), np.sqrt(1-a) )
    return EarthR*c
    
def DistanceAlongMeridian(lat1,lat2,long):
    
    lat1=lat1/180*np.pi   
    lat2=lat2/180*np.pi
    long=np.mod(long,360)/180*np.pi
    
    dlat=lat1-lat2

    a = np.sin(dlat/2)**2
    c = 2*np.arctan2( np.sqrt(a), np.sqrt(1-a) )
    return EarthR*dlat
    
def AngleAlongParallel(lat,long,dist):
    lat=lat/180*np.pi
    long=np.mod(long,360)/180*np.pi
    
    dlong=dist/(2*np.pi*EarthR*np.cos(lat))*360
    
    return dlong

def AngleAlongMeridian(lat,long,dist):
    lat=lat/180*np.pi
    long=np.mod(long,360)/180*np.pi
    
    dlat=dist/(2*np.pi*EarthR)*360
    
    return dlat
    
def RangeToCenterRadius(lat1,lat2,long1,long2):

    lat1=NormalizeLat(lat1)
    lat2=NormalizeLat(lat2)

    long1=NormalizeLong(long1)
    long2=NormalizeLong(long2)

    latcenter=(lat1+lat2)/2
    if long2>long1:
    	longcenter=(long1+long2)/2
    else:
    	longcenter=(long1+long2+360)/2
    	longcenter=NormalizeLong(longcenter)

    radlat=DistanceAlongMeridian(lat1,latcenter,longcenter)
    radlong=DistanceAlongParallel(latcenter,long1,longcenter)
    radius=max(radlat,radlong)
    return latcenter,longcenter,radius

    