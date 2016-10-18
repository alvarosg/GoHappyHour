from django.db import models
from django.db.models import signals
from django.core.validators import RegexValidator

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_published = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='locations')

    date_edited = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    postcode = models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    website = models.URLField(max_length=200,null=True,blank=True)
    phonenumber = models.CharField(max_length=200,null=True)
    timezoneid = models.CharField(max_length=50,null=True)
        
    GOHAPPYHOUR = 'GHH'
    GOOGLEPLACES= 'GP'
    ORIGIN_CHOICES = (
        (GOHAPPYHOUR, 'Go Happy Hour'),
        (GOOGLEPLACES, 'Google Places'),
    )
    origin =  models.CharField(max_length=4, choices=ORIGIN_CHOICES,default=GOHAPPYHOUR)
    originid = models.CharField(max_length=100,null=True,default=None)

    class Meta:
        ordering = ('date_published',)
        unique_together = ('origin', 'originid',)
        
    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)

class LocationPicture(models.Model):
    owner = models.ForeignKey('auth.User', related_name='locationpictures')
    location = models.ForeignKey(Location, related_name='locationpictures')
    picture = models.ImageField(upload_to="images/locations/fullsize",null=True,blank=True)
    thumbnail = models.ImageField(upload_to="images/locations/thumbnails",null=True,blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    GOHAPPYHOUR = 'GHH'
    GOOGLEPLACES = 'GP'
    EXTERNALLINK = 'LNK'
    ORIGIN_CHOICES = (
        (GOHAPPYHOUR, 'Go Happy Hour'),
        (GOOGLEPLACES, 'Google Places'),
        (EXTERNALLINK, 'External Link'),
    )
    origin =  models.CharField(max_length=4, choices=ORIGIN_CHOICES,default=GOHAPPYHOUR)
    originid = models.CharField(max_length=1000,null=True,default=None)

    class Meta:
        ordering = ('date_published',)
        unique_together = ('origin', 'originid','location')
        
    def save(self, *args, **kwargs):
        super(LocationPicture, self).save(*args, **kwargs)
        
class Offer(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500,null=True,blank=True)
    score = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    date_expire = models.DateField(null=True,blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, related_name='offers')
    owner = models.ForeignKey('auth.User', related_name='offers')
        
    class Meta:
        ordering = ('date_published',)
        
    def save(self, *args, **kwargs):
        super(Offer, self).save(*args, **kwargs)

class OfferPicture(models.Model):
    owner = models.ForeignKey('auth.User', related_name='offerpictures')
    offer = models.ForeignKey(Offer, related_name='offerpictures')
    picture = models.ImageField(upload_to="images/offers/fullsize",null=True,blank=True)
    thumbnail = models.ImageField(upload_to="images/offers/thumbnails",null=True,blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    
    GOHAPPYHOUR = 'GHH'
    GOOGLEPLACES = 'GP'
    EXTERNALLINK = 'LNK'
    ORIGIN_CHOICES = (
        (GOHAPPYHOUR, 'Go Happy Hour'),
        (GOOGLEPLACES, 'Google Places'),
        (EXTERNALLINK, 'External Link'),
    )
    origin =  models.CharField(max_length=4, choices=ORIGIN_CHOICES,default=GOHAPPYHOUR)
    originid = models.CharField(max_length=1000,null=True,default=None)

    class Meta:
        ordering = ('date_published',)
        unique_together = ('origin', 'originid','offer')
        
    def save(self, *args, **kwargs):
        super(OfferPicture, self).save(*args, **kwargs)
        
class OfferTimeRange(models.Model):
    #sequence of 7 0s or 1s with at least one 1
    weekdays = models.CharField(max_length=7,validators=[RegexValidator(regex='^(?=.*[1])[01]{7}$')])
    time_start = models.TimeField()
    time_end = models.TimeField()
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    offer = models.ForeignKey(Offer, related_name='offertimeranges')
    owner = models.ForeignKey('auth.User', related_name='offertimeranges')
    
    class Meta:
        ordering = ('date_published',)
        
    def save(self, *args, **kwargs):
        super(OfferTimeRange, self).save(*args, **kwargs)

        
class OfferUserVote(models.Model):
    value = models.IntegerField()
    offer = models.ForeignKey(Offer, related_name='offeruservotes')
    owner = models.ForeignKey('auth.User', related_name='offeruservotes')
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('date_published',)
        unique_together = ('offer', 'owner',)
        
    def save(self, *args, **kwargs):
        super(OfferUserVote, self).save(*args, **kwargs)

class OfferUserComment(models.Model):
    comment = models.CharField(max_length=500,null=True)
    offer = models.ForeignKey(Offer, related_name='offerusercomments')
    owner = models.ForeignKey('auth.User', related_name='offerusercomments')
    date_published = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date_edited',)
        unique_together = ('offer', 'owner',)
        
    def save(self, *args, **kwargs):
        super(OfferUserComment, self).save(*args, **kwargs)