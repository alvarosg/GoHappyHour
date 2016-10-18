from django.forms import widgets
from rest_framework import serializers
from django.db import models
from models import *
from django.contrib.auth.models import User
import offernow as on
import weekdays as wd
import userutils as uu


# Create your models here.

class OfferTimeRangeFullDataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    weekdaystrs = serializers.SerializerMethodField('CalculateWeekdays')
    time_start_format = serializers.TimeField(format="%H:%M",source='time_start')
    time_end_format = serializers.TimeField(format="%H:%M",source='time_end')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj.offer.location)
        return on.OfferTimeRangeNow(obj,time)
    def CalculateWeekdays(self, obj):
        return wd.WeekdayStrings(obj.weekdays)
    class Meta:
        model = OfferTimeRange
        fields = ('id','weekdays', 'time_start','time_end', 'time_start_format','time_end_format','date_published','date_edited','owner','offer','offernow','weekdaystrs','userlabel')

class OfferTimeRangeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offer = serializers.ReadOnlyField(source='offer.name')
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    weekdaystrs = serializers.SerializerMethodField('CalculateWeekdays')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj.offer.location)
        return on.OfferTimeRangeNow(obj,time)

    def CalculateWeekdays(self, obj):
        return wd.WeekdayStrings(obj.weekdays)


    class Meta:
        model = OfferTimeRange
        fields = ('id','weekdays', 'time_start','time_end','date_published','date_edited','owner','offer','offernow','weekdaystrs','userlabel')

class OfferPictureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offer = serializers.ReadOnlyField(source='offer.name')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    class Meta:
        model = OfferPicture
        fields = ('id','picture','thumbnail','date_published','date_edited','owner','offer','origin','originid','userlabel')

class OfferSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    location = serializers.ReadOnlyField(source='location.name')
    offerpictures = serializers.PrimaryKeyRelatedField(many=True, queryset=OfferPicture.objects.all())
    offertimeranges = serializers.PrimaryKeyRelatedField(many=True, queryset=OfferTimeRange.objects.all())
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj.location)
        return on.OfferNow(obj,time)
    class Meta:
        model = Offer
        fields = ('id','name','description','score','votes', 'date_expire','date_published','date_edited','owner','location','offertimeranges','offerpictures','offernow','userlabel')

class OfferFullDataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offertimeranges = OfferTimeRangeFullDataSerializer(many=True)
    offerpictures = OfferPictureSerializer(many=True)
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj.location)
        return on.OfferNow(obj,time)
    class Meta:
        model = Offer
        fields = ('id','name','description','score','votes', 'date_expire','date_published','date_edited','owner','location','offertimeranges','offerpictures','offernow','userlabel')

class LocationPictureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    location = serializers.ReadOnlyField(source='location.name')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    class Meta:
        model = LocationPicture
        fields = ('id','picture','thumbnail','date_published','date_edited','owner','location','origin','originid','userlabel')

class LocationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all())
    locationpictures = serializers.PrimaryKeyRelatedField(many=True, queryset=LocationPicture.objects.all())
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj)
        return on.LocationOfferNow(obj,time)
    class Meta:
        model = Location
        fields = ('id','name', 'latitude','longitude','address','postcode','country','website','phonenumber','date_published','date_edited','owner','offers','timezoneid','locationpictures','origin','originid','offernow','userlabel')

class LocationFullDataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offers = OfferFullDataSerializer(many=True)
    locationpictures = LocationPictureSerializer(many=True)
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj)
        return on.LocationOfferNow(obj,time)
    class Meta:
        model = Location
        fields = ('id','name', 'latitude','longitude','address','postcode','country','website','phonenumber','date_published','date_edited','owner','offers','timezoneid','locationpictures','origin','originid','offernow','userlabel')

class LocationAddGoogleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()
    locationpictures = serializers.PrimaryKeyRelatedField(many=True, queryset=LocationPicture.objects.all())
    offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all())
    offernow = serializers.SerializerMethodField('CalculateOfferNow')

    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj)
        return on.LocationOfferNow(obj,time)
    class Meta:
        model = Location
        fields = ('id','name', 'latitude','longitude','address','postcode','country','website','phonenumber','date_published','date_edited','owner','offers','timezoneid','locationpictures','origin','originid','offernow')

class LocationSearchSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all())
    distance = serializers.ReadOnlyField(allow_null=True)
    locationpictures = LocationPictureSerializer(many=True)
    offernow = serializers.SerializerMethodField('CalculateOfferNow')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    def CalculateOfferNow(self, obj):
        time=on.TimeAtLocation(obj)
        return on.LocationOfferNow(obj,time)
    class Meta:
        model = Location
        fields = ('id','name', 'latitude','longitude','address','postcode','country','website','phonenumber','date_published','date_edited','owner','offers','timezoneid','locationpictures','origin','originid','distance','offernow','userlabel')
    
        
class OfferUserVoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offer = serializers.ReadOnlyField(source='offer.name')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    class Meta:
        model = OfferUserVote
        fields = ('id','value','date_published','date_edited','owner','offer','userlabel')

class OfferUserCommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    offer = serializers.ReadOnlyField(source='offer.name')
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj.owner)
    class Meta:
        model = OfferUserComment
        fields = ('id','comment','date_published','date_edited','owner','offer','userlabel')

        
class UserSerializer(serializers.ModelSerializer):
    locations = serializers.PrimaryKeyRelatedField(many=True, queryset=Location.objects.all())
    offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all())
    offertimeranges = serializers.PrimaryKeyRelatedField(many=True, queryset=OfferTimeRange.objects.all())
    userlabel = serializers.SerializerMethodField('ObtainUserLabel')
    def ObtainUserLabel(self, obj):
        return uu.ObtainUserLabel(obj)
    class Meta:
        model = User
        fields = ( 'id','username', 'locations','offers','offertimeranges','userlabel')
        
