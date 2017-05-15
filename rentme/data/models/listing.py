import enum

from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from trademe.models.enums import AllowsPickups, GeographicLocationAccuracy

from . import catalogue
from ._utils import default_debug_methods, EnumIntegerField
from .registry import model_registry


@model_registry.register_django_model
@default_debug_methods
class Attributes(models.Model):

    class Meta:
        ordering = ['name']

    name = models.TextField(blank=False)
    value = models.TextField(blank=False)
    display_name = models.TextField(blank=False)

    def __str__(self):
        return '{!r}: {!r}'.format(self.name, self.value)


@model_registry.register_django_model
@default_debug_methods
class BroadbandTechnology(models.Model):

    class Meta:
        ordering = ['max_down', 'max_up', 'name']

    name = models.TextField(blank=False)
    completion = models.TextField()
    availability = models.TextField(blank=False)
    min_down = models.DecimalField(default=0, decimal_places=4, max_digits=14)
    max_down = models.DecimalField(default=0, decimal_places=4, max_digits=14)
    min_up = models.DecimalField(default=0, decimal_places=4, max_digits=14)
    max_up = models.DecimalField(default=0, decimal_places=4, max_digits=14)


@model_registry.register_django_model
@default_debug_methods(str_fields=('latitude', 'longitude'))
class GeographicLocation(models.Model):

    accuracy = EnumIntegerField(GeographicLocationAccuracy)
    easting = models.IntegerField(default=-1)
    northing = models.IntegerField(default=-1)
    latitude = models.DecimalField(decimal_places=7, max_digits=10)
    longitude = models.DecimalField(decimal_places=7, max_digits=10)


@model_registry.register_django_model
@default_debug_methods
class Member(models.Model):

    class Meta:
        ordering = ['nickname', 'member_id']

    unique_positive = models.IntegerField()
    date_joined = models.DateTimeField()
    is_authenticated = models.BooleanField()
    member_id = models.IntegerField(primary_key=True)
    nickname = models.TextField()
    unique_negative = models.IntegerField()
    feedback_count = models.IntegerField()
    region = models.TextField()
    suburb = models.TextField()
    is_address_verified = models.BooleanField()
    date_address_verified = models.DateTimeField()
    photo = models.URLField()
    original_width = models.IntegerField(default=-1)
    original_height = models.IntegerField(default=-1)
    occupation = models.TextField(blank=True)


@model_registry.register_django_model
@default_debug_methods
class Photo(models.Model):

    class Meta:
        ordering = ['photo_id']

    photo_id = models.IntegerField(primary_key=True)
    thumbnail = models.URLField()
    list = models.URLField()
    medium = models.URLField()
    gallery = models.URLField()
    large = models.URLField()
    full_size = models.URLField()
    plus_size = models.URLField()
    original_width = models.IntegerField(default=-1)
    original_height = models.IntegerField(default=-1)


@model_registry.register_django_model
@default_debug_methods
class AgencyAgent(models.Model):

    agency = models.ForeignKey('Agency', related_name='agents', null=True)
    full_name = models.TextField()
    mobile_phone_number = models.TextField(blank=True)
    office_phone_number = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    url_slug = models.TextField(blank=True)


@model_registry.register_django_model
@default_debug_methods
class Agency(models.Model):

    id = models.IntegerField(primary_key=True)
    # agents
    branding_background_color = models.TextField()
    branding_large_banner_url = models.TextField()
    branding_office_location = models.TextField()
    branding_stroke_color = models.TextField()
    branding_text_color = models.TextField()
    branding_disable_banner = models.BooleanField(default=False)
    fax_number = models.TextField(blank=True)
    is_licensed_property_agency = models.BooleanField(default=False)
    is_real_estate_agency = models.BooleanField(default=False)
    logo = models.URLField(blank=True, null=True)
    logo2 = models.URLField(blank=True, null=True)
    name = models.TextField(blank=True)
    phone_number = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)


class PricePeriodEnum(enum.Enum):

    WEEKLY = 1
    MONTHLY = 2


class ListingPrice(models.Model):

    dollars = models.IntegerField()
    period = EnumIntegerField(PricePeriodEnum)

    @property
    def display(self):
        return '{} per {}'.format(self.dollars, self.period.name.lower())


@model_registry.register_django_model
@default_debug_methods
class Listing(models.Model):

    listing_id = models.IntegerField(primary_key=True)
    agency = models.ForeignKey('Agency', related_name='listings', null=True)
    allows_pickups = EnumIntegerField(AllowsPickups)
    as_at = models.DateTimeField()
    attributes = models.ManyToManyField('Attributes', related_name='listings')
    bidder_and_watchers = models.IntegerField(default=0)
    body = models.TextField(blank=True)
    broadband_technologies = models.ManyToManyField('BroadbandTechnology', related_name='listings')
    can_add_to_cart = models.BooleanField()
    category = models.ForeignKey(catalogue.Category, related_name='listings')
    end_date = models.DateTimeField()
    geographic_location = models.ForeignKey('GeographicLocation', related_name='listings')
    has_gallery = models.BooleanField(default=False)
    is_bold = models.BooleanField(default=False)
    is_classified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)
    is_super_featured = models.BooleanField(default=False)
    member = models.ForeignKey('Member', related_name='listings')
    note_date = models.DateTimeField()
    photo = models.ForeignKey('Photo', blank=True, null=True, related_name='listing_photo_set')
    photos = models.ManyToManyField('Photo', related_name='listings')
    price_display = models.TextField()
    price = models.ForeignKey('ListingPrice', null=True)
    # region = models.ForeignKey(catalogue.Locality, related_name='listings')
    start_date = models.DateTimeField()
    suburb = models.ForeignKey(catalogue.Suburb, related_name='listings', null=True)
    super_feature_end_date = models.DateTimeField(null=True)
    title = models.TextField()
    view_count = models.IntegerField(default=0)
    viewing_tracker_supported = models.BooleanField(default=False)

    @cached_property
    def thumbnail(self):
        if self.photo:
            return self.photo
        for photo in self.photos.all():
            return photo
        return None

    @cached_property
    def trademe_url(self):
        return ('https://preview.trademe.co.nz/property/trade-me-property' +
                '/residential-to-rent/' + str(self.listing_id))

    def get_absolute_url(self):
        return reverse('rentals.view', kwargs={'pk': self.listing_id})

    @cached_property
    def all_photos(self):
        all_photos = [self.photo] if self.photo else []
        for photo in self.photos.all():
            if photo not in all_photos:
                all_photos.append(photo)
        return all_photos
