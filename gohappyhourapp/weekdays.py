from models import *
import numpy as np

def WeekdayIntervals(weekdays):
    weekdayslist=[]

    status=0 #Means finding first 0
    startday=None
    endday=None
    firstzero=None
    for i in range(len(weekdays)):
        if status == 0:
            if weekdays[i]=='0':
                firstzero=i
                status=1 # Means finding first 1 after a 0
                continue
        if status == 1:
            if weekdays[i]=='1':
                startday=i
                status=2 # Means finding first 0 after a 1
                continue
        if status == 2:
            if weekdays[i]=='0':
                endday=i-1
                weekdayslist.append([startday,endday])
                startday=None
                endday=None
                status=1
                continue

    if startday is not None:
        if firstzero>0:
            endday=firstzero-1
            weekdayslist.append([startday,endday])
            startday=None
            endday=None
        else:
            endday=6
            weekdayslist.append([startday,endday])
            startday=None
            endday=None
    else:
        if weekdays[0]=='1':
            if firstzero is not None:
                weekdayslist.insert(0,[0,firstzero-1])
            else:
                weekdayslist.insert(0,[0,6])

    return weekdayslist

def NumToWeekday(num):
    if num==0:
        return "Mon"
    if num==1:
        return "Tue"
    if num==2:
        return "Wed"
    if num==3:
        return "Thu"
    if num==4:
        return "Fri"
    if num==5:
        return "Sat"
    if num==6:
        return "Sun"

def WeekdayStrings(weekdays):
    weekdaystringlist=[]
    intervals=WeekdayIntervals(weekdays)

    for interval in intervals:
        if interval[0]==interval[1]:
            weekdaystringlist.append({'dayrange':NumToWeekday(interval[0])})
            continue
        else:
            weekdaystringlist.append({'dayrange':"%s-%s"%(NumToWeekday(interval[0]),NumToWeekday(interval[1]))})
            continue
    return weekdaystringlist


