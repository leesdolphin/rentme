from rest_framework import serializers

from rentme.data.models import Listing


class ListingShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ('listing_id', 'price_display', 'price', 'all_photos', 'suburb', 'title', 'agency')
