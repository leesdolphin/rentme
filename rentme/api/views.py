from rest_framework import generics

from rentme.api.serializers import ListingShortSerializer
from rentme.data.models import Listing


class ListingList(generics.ListAPIView):

    queryset = Listing.objects.all()
    serializer_class = ListingShortSerializer
