from models import *
from datetime import datetime
import numpy as np
import pytz 

def TimeAtLocation(location):
    tz = pytz.timezone(location.timezoneid)
    now = datetime.utcnow()
    tzoffset = tz.utcoffset(now)
    mynow = now+tzoffset
    return mynow

def LocationOfferNow(location,time):
    queryset = Offer.objects.all()
    queryset = queryset.filter(location=location.id)
    retval= None
    for obj in queryset :
        onow=OfferNow(obj,time)
        if onow:
            return True
        elif (onow is not None):
            retval = False
    return retval

def OfferNow(offer,time):
    queryset = OfferTimeRange.objects.all()
    queryset = queryset.filter(offer=offer.id)
    retval= None
    for obj in queryset :
        retval = False
        if OfferTimeRangeNow(obj,time):
            return True
    return retval

def OfferTimeRangeNow(offertimerange,time):
    #If the time interval is within the same day
    if (offertimerange.time_start<offertimerange.time_end and
        #We check that the time is within the interval
        time.time()>offertimerange.time_start and time.time()<offertimerange.time_end and
        #And we check that the week day is one of the available weekdays
        offertimerange.weekdays[time.weekday()]=='1'):
        return True
    #If the time interval goes through midnigth
    elif offertimerange.time_start>offertimerange.time_end:
        #If the current time is between starting and midnight, and the week day has an offer
        if time.time()>offertimerange.time_start and offertimerange.weekdays[time.weekday()]=='1':
            return True
        #If the current time is  past midnig, but before the end of the happy hour, and and there was offer on the PREVIOUS weekday        
        elif time.time()<offertimerange.time_end and offertimerange.weekdays[np.mod(time.weekday()-1,7)]=='1':
            return True

    return False

