from django.db import models

# Create your models here.

class TradeMeLocality(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class TradeMeDistrict(models.Model):

    locality = models.ForeignKey(TradeMeLocality, related_name='districts')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

class TradeMeSuburb(models.Model):

    district = models.ForeignKey(TradeMeDistrict, related_name='suburbs')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    adjacent_suburbs = models.ManyToManyField('self')

class TradeMeMember(models.Model):

    id = models.IntegerField(primary_key=True)
    nickname = models.TextField()
    email = models.EmailField()
    suburb = models.TextField()
    region = models.TextField()


class TradeMeListing(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    category = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    generated_at = models.DateTimeField() ## AsAt
    stored_at = models.DateTimeField(auto_now=True)
    ## properties - From a FK relation on TradeMeListingProperty
    agency = models.ManyToManyField('TradeMeAgency')
    location = models.ForeignKey('TradeMeListingLocation')
    price = models.ForeignKey('TradeMeListingPrice')
    member = models.ForeignKey('TradeMeMember', null=True)
    description = models.TextField() ## Body
    thumbnail_href = models.URLField(null=True) ## PictureHref
    photos = models.ManyToManyField('TradeMeListingPhoto')




class TradeMeListingPrice(models.Model):
    class Meta:
        unique_together = ('value', 'period',)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.ForeignKey('TradeMeListingPricePeriods')




class TradeMeListingPricePeriods(models.Model):

    name = models.TextField(unique=True)


class TradeMeListingLocation(models.Model):
    class Meta:
        unique_together = ('latitude', 'longitude', 'accuracy')
    latitude = models.DecimalField(max_digits=11, decimal_places=8, unique=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, unique=True)
    accuracy = models.IntegerField(choices=(
        ## These are out of order in the docs.
        (0, "None"),
        (1, "Address"),
        (3, "Street"),
        (2, "Suburb"),
    ), unique=True)


class TradeMeListingPhoto(models.Model):

    id = models.IntegerField(primary_key=True)
    thumbnail = models.URLField()
    list = models.URLField()
    medium = models.URLField()
    gallery = models.URLField()
    large = models.URLField()
    full_size = models.URLField()
    original_width = models.IntegerField()
    original_height = models.IntegerField()

class TradeMeAgency(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField()
    logo = models.URLField()
    ## agents
    is_real_estate_agency = models.BooleanField()
    is_licensed_property_agency = models.BooleanField()


class TraceMeAgencyAgent(models.Model):

    agency = models.ForeignKey(TradeMeAgency, related_name='agents')
    full_name = models.TextField()
    position = models.TextField()
    mobile_number = models.CharField(max_length=20)
    office_number = models.CharField(max_length=20)
    email = models.EmailField()
    fax_number = models.CharField(max_length=20)


class TradeMeListingProperty(models.Model):

    listing = models.ForeignKey(TradeMeListing, related_name='properties')
    name = models.TextField()
    display_name = models.TextField()
    value = models.TextField()
