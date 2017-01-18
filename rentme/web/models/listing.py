from django.db import models

from trademe.models.enums import GeographicLocationAccuracy

from ._utils import EnumIntegerField
from .registry import model_registry


@model_registry.register_django_model
class Listing(models.Model):

    allows_pickups
    as_at
    attributes
    bidder_and_watchers
    body
    can_add_to_cart
    category_name
    category_path
    category
    embedded_content
    end_date
    geographic_location
    has_gallery
    is_bold
    is_classified
    is_featured
    is_highlighted
    listing_id
    listing_length
    member
    note_date
    open_homes
    payment_options
    photo_id
    photos
    price_display
    region_id
    region
    reserve_state
    shipping_options
    start_date
    start_price
    suburb_id
    suburb
    title
    view_count
       # broadband_technologies
    # contact_details =


@model_registry.register_django_model
class Attributes(models.Model):

    name = models.TextField(blank=False)
    value = models.TextField(blank=False)
    display_name = models.TextField(blank=False)


@model_registry.register_django_model
class BroadbandTechnology(models.Model):

    name = models.TextField(blank=False)
    completion = models.TextField()
    availability = models.TextField(blank=False)
    min_down = models.DecimalField(default=0)
    max_down = models.DecimalField(default=0)
    min_up = models.DecimalField(default=0)
    max_up = models.DecimalField(default=0)


@model_registry.register_django_model
class GeographicLocation(models.Model):
    accuracy = EnumIntegerField(GeographicLocationAccuracy)
    easting = models.IntegerField()
    northing = models.IntegerField()
    latitude = models.DecimalField()
    longitude = models.DecimalField()


@model_registry.register_django_model
class Member(models.Model):
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


@model_registry.register_django_model
class Photo(models.Model):
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
