from models import *
import numpy as np
from django.db.models import Q
from django.db.models import Sum


def CalculateScoreOffer(offer):
    queryset = OfferUserVote.objects.all()
    queryset = queryset.filter(offer=offer.id)
    queryset.filter(Q(value=1)&Q(value=-1));

    votes=len(queryset)
    score=queryset.aggregate(Sum('value'))['value__sum']

    return votes,score
