from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Location)
admin.site.register(LocationPicture)
admin.site.register(Offer)
admin.site.register(OfferPicture)
admin.site.register(OfferTimeRange)
admin.site.register(OfferUserVote)
admin.site.register(OfferUserComment)