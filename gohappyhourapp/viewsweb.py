from models import *
from serializers import *
import numpy as np
import geocalcs as gc

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter



@api_view(['GET'])
def MapView(request,locid=None,offerid=None,locoption=None,offeroption=None):
    context = {}

    latval = request.query_params.get('lat', None)
    longval = request.query_params.get('long', None)
    zoom = request.query_params.get('zoom', None)

    if locid is not None:
        context['locid']=locid
        if offerid is not None:
            context['offerid']=offerid
        elif offeroption is not None:
            context['offeroption']=offeroption
    elif locoption is not None:
            context['locoption']=locoption

    if latval is not None and longval is not None:
        context['lat']=latval
        context['long']=longval

    if zoom is not None:
        context['zoom']=zoom
    
    return render(request, 'gohappyhourapp/mapview.html', context)
    
@api_view(['GET', 'POST'])
def LocationView(request,pk):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        location = get_object_or_404(Location,id=pk)
        serializer = LocationFullDataSerializer(location)        
        context = {'location': serializer.data}
        
        return render(request, 'gohappyhourapp/locationview.html', context)
        #return Response(serializer.data,template_name='gohappyhourapp/locationview.html')
        
        
    