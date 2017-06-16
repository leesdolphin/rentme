# from rest_framework import authentication, generics, mixins, permissions, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from rentme.api.serializers import AgencySerializer, ListingShortSerializer
# from rentme.data.models.listing import Agency, Listing
#
#
# class HealthcheckView(APIView):
#     permissions = (permissions.AllowAny, )
#
#     def get(self, request, format=None):
#         return Response({})
#
#
# class ListingViewSet(viewsets.ReadOnlyModelViewSet):
#
#     queryset = Listing.objects.all().order_by('listing_id')
#     serializer_class = ListingShortSerializer
#     lookup_field = 'listing_id'
#     lookup_value_regex = '[1-9][0-9]*'
#
#
# class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
#
#     queryset = Agency.objects.all().order_by('id')
#     serializer_class = AgencySerializer
#     lookup_field = 'id'
#     lookup_value_regex = '[1-9][0-9]*'
