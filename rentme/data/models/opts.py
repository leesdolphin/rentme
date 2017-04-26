from collections import OrderedDict
import re

from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
PHOTO_ID_REGEX = re.compile(r'[^0-9]*([0-9].*[0-9])[^0-9]*')


def photos_cleanup(photos):
    ph_id = OrderedDict()
    for photo in photos:
        m = PHOTO_ID_REGEX.match(photo)
        ph_id[m.group(1)] = photo
    return list(ph_id.values())


class TradeMeMember(models.Model):

    id = models.IntegerField(primary_key=True)
    nickname = models.TextField()
    email = models.EmailField()
    suburb = models.TextField()
    region = models.TextField()


class TradeMeListing(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    description = models.TextField(null=True)  # Body
    address = models.TextField(null=True)
    available_from = models.TextField(null=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    rent_per_week = models.IntegerField()
    category = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    generated_at = models.DateTimeField()  # AsAt
    stored_at = models.DateTimeField(auto_now=True)
    # attributes - From a FK relation on TradeMeListingProperty
    agency = models.ManyToManyField('TradeMeAgency')
    location = models.ForeignKey('TradeMeListingLocation')
    member = models.ForeignKey('TradeMeMember', null=True)
    thumbnail_href = models.URLField(null=True)   # PictureHref
    photos = models.ManyToManyField('TradeMeListingPhoto')

    def __str__(self):
        return '[%d] %s' % (self.id, self.title)


    def get_review_url(self, rating):
        rating = rating.lower()
        if rating in PropertyReview.MAPPING:
            return reverse('rentals.review', kwargs={'id': str(self.id),
                                                     'rating': rating})
        else:
            raise ValueError('Invalid Rating')

    def get_review_url_positive(self):
        return self.get_review_url('positive')

    def get_review_url_neutral(self):
        return self.get_review_url('neutral')

    def get_review_url_negative(self):
        return self.get_review_url('negative')


class TradeMeListingLocation(models.Model):

    class Meta:
        unique_together = ('latitude', 'longitude', 'accuracy')

    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    accuracy = models.IntegerField(choices=(
        # These are out of order in the docs.
        (0, 'None'),
        (1, 'Address'),
        (3, 'Street'),
        (2, 'Suburb'),
    ))


class TradeMeListingPhoto(models.Model):

    id = models.IntegerField(primary_key=True)
    thumbnail = models.URLField(null=True)
    list = models.URLField(null=True)
    medium = models.URLField(null=True)
    gallery = models.URLField(null=True)
    large = models.URLField(null=True)
    full_size = models.URLField(null=True)
    plus_size = models.URLField(null=True)
    original_width = models.IntegerField()
    original_height = models.IntegerField()

    @property
    def largest_image(self):
        for url in [self.plus_size, self.full_size, self.large, self.gallery,
                    self.medium, self.list, self.thumbnail]:
            if url:
                return url
        return None

    def __str__(self):
        return '[%d] <%r>' % (self.id, self.largest_image)


class TradeMeAgency(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    phone_number = models.CharField(max_length=20, null=True)
    website = models.URLField(null=True)
    logo = models.URLField(null=True)
    # agents
    is_real_estate_agency = models.BooleanField()
    is_licensed_property_agency = models.BooleanField()


class TraceMeAgencyAgent(models.Model):

    class Meta:
        unique_together = ('agency', 'full_name')

    agency = models.ForeignKey(TradeMeAgency, related_name='agents')
    full_name = models.TextField()
    position = models.TextField(null=True)
    mobile_number = models.CharField(max_length=20, null=True)
    office_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    fax_number = models.CharField(max_length=20, null=True)


class TradeMeListingAttribute(models.Model):

    class Meta:
        unique_together = ('listing', 'name')

    listing = models.ForeignKey(TradeMeListing, related_name='attributes')
    name = models.TextField()
    display_name = models.TextField()
    value = models.TextField()


class PropertyReview(models.Model):

    MAPPING = {
        'positive': 2,
        'neutral': 1,
        'negative': 0,
    }

    property = models.OneToOneField(TradeMeListing, related_name='review')
    rating = models.PositiveSmallIntegerField()

    def __getitem__(self, item):
        if item.startswith('is_') and item[3:] in self.MAPPING:
            return self.rating == self.MAPPING[item[3:]]
        else:
            raise KeyError(item)
