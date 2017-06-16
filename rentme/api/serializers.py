# from rest_framework import serializers
#
# from rentme.data.models import catalogue, listing
#
#
# class EnumChoiceField(serializers.ChoiceField):
#
#     def __init__(self, enum, **kwargs):
#         if 'choices' not in kwargs:
#             kwargs['choices'] = [
#                 (member, member.name) for member in enum
#             ]
#             print(kwargs['choices'])
#         super().__init__(**kwargs)
#         self.enum_cls = enum
#
#     to_internal_value = None
#
#     def to_representation(self, value):
#         try:
#             enum_val = self.enum_cls(value)
#             return self.choices[enum_val]
#         except:
#             return super().to_representation(value)
#
#
# class SuburbSerializer(serializers.ModelSerializer):
#
#     suburb = serializers.CharField(source='name')
#     district = serializers.CharField(source='district.name')
#     district_id = serializers.IntegerField(source='district.district_id')
#     locality = serializers.CharField(source='district.locality.name')
#     locality_id = serializers.IntegerField(source='district.locality.locality_id')
#
#     class Meta:
#         model = catalogue.Suburb
#         fields = (
#             'suburb',
#             'suburb_id',
#             'district',
#             'district_id',
#             'locality',
#             'locality_id',
#         )
#
#     to_internal_value = None
#
#
# class AgencyAgentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = listing.AgencyAgent
#         fields = (
#             'full_name',
#             'mobile_phone_number',
#             'office_phone_number',
#             'photo',
#             'url_slug',
#         )
#
#
# class AgencyShortSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = listing.Agency
#         fields = (
#             'branding_office_location',
#             'is_licensed_property_agency',
#             'is_real_estate_agency',
#             'name',
#             'branding_logo',
#             'phone_number',
#             'website',
#         )
#
#
# class AgencySerializer(serializers.ModelSerializer):
#
#     agents = AgencyAgentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = listing.Agency
#         fields = (
#             'agents'
#             'branding_background_color',
#             'branding_disable_banner',
#             'branding_large_banner_url',
#             'branding_logo',
#             'branding_office_location',
#             'branding_stroke_color',
#             'branding_text_color',
#             'fax_number',
#             'id',
#             'is_licensed_property_agency',
#             'is_real_estate_agency',
#             'logo',
#             'logo2',
#             'name',
#             'phone_number',
#             'website',
#         )
#
#
# class MemberSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = listing.Member
#         fields = (
#             'date_address_verified',
#             'date_joined',
#             'feedback_count',
#             'is_address_verified',
#             'is_authenticated',
#             'member_id',
#             'nickname',
#             'occupation',
#             'original_height',
#             'original_width',
#             'photo',
#             'region',
#             'suburb',
#             'unique_negative',
#             'unique_positive',
#         )
#
#
# class GeolocationSerializer(serializers.ModelSerializer):
#
#     accuracy = EnumChoiceField(
#         enum=listing.GeographicLocationAccuracy,
#     )
#
#     class Meta:
#         model = listing.GeographicLocation
#         fields = (
#             'accuracy',
#             'easting',
#             'northing',
#             'latitude',
#             'longitude',
#         )
#
#
# class PhotoSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = listing.Photo
#         fields = (
#             'photo_id',
#             'thumbnail',
#             'list',
#             'medium',
#             'gallery',
#             'large',
#             'full_size',
#             'plus_size',
#             'original_width',
#             'original_height',
#         )
#
#
# class PriceSerializer(serializers.ModelSerializer):
#
#     period = EnumChoiceField(
#         enum=listing.PricePeriodEnum,
#         choices=[
#             (p, p.title_name) for p in listing.PricePeriodEnum
#         ]
#     )
#     dollars_per_day = serializers.FloatField(min_value=0, read_only=True)
#     dollars_per_week = serializers.FloatField(min_value=0, read_only=True)
#     dollars_per_month = serializers.FloatField(min_value=0, read_only=True)
#     dollars_per_year = serializers.FloatField(min_value=0, read_only=True)
#
#     class Meta:
#         model = listing.ListingPrice
#         fields = (
#             'dollars',
#             'period',
#             'dollars_per_day',
#             'dollars_per_week',
#             'dollars_per_month',
#             'dollars_per_year',
#         )
#
#
# class ListingShortSerializer(serializers.ModelSerializer):
#
#     all_photos = PhotoSerializer(many=True, read_only=True)
#     price = PriceSerializer(read_only=True)
#     agency = AgencyShortSerializer(read_only=True)
#     suburb = SuburbSerializer(read_only=True)
#     member = MemberSerializer(read_only=True)
#     geographic_location = GeolocationSerializer(read_only=True)
#
#     class Meta:
#         model = listing.Listing
#         fields = ('listing_id', 'suburb', 'title', 'agency', 'price',
#                   'all_photos', 'trademe_url', 'member', 'geographic_location')
