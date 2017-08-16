import enum

from django.db import models

from rentme.data.models._utils import EnumIntegerField


class Agency(models.Model):

    address = models.TextField(
        null=True,
        help_text='The address of the company HQ.'
    )
    branding = models.ForeignKey(
        'Branding',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='agency_reverse_branding',
        help_text='The branding object for the company.'
    )
    city = models.TextField(
        null=True,
        help_text='The city where the company HQ is located.'
    )
    e_mail = models.TextField(
        null=True,
        help_text='A contact email address for the company.'
    )
    fax_number = models.TextField(
        null=True,
        help_text='A fax number for the company.'
    )
    id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the company.'
    )
    is_job_agency = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the agency does job listings.'
    )
    is_licensed_property_agency = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the agency is an REAA licensed property '
                  'agency'
    )
    is_real_estate_agency = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the agency does real estate.'
    )
    logo = models.TextField(
        null=True,
        help_text='A URL for the company logo.'
    )
    logo2 = models.TextField(
        null=True,
        help_text='A URL for the second company logo.'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the company.'
    )
    phone_number = models.TextField(
        null=True,
        help_text='A contact phone number for the company. For Motors '
                  'Dealership please use the PhoneNumbers collection instead'
    )
    suburb = models.TextField(
        null=True,
        help_text='The suburb where the company HQ is located.'
    )
    website = models.TextField(
        null=True,
        help_text='The URL of the company website.'
    )


class Agent(models.Model):

    agency = models.ForeignKey(
        'Agency',
        on_delete=models.CASCADE,
        related_name='agents',
        help_text='The agency that this agent is contactable at.'
    )
    e_mail = models.TextField(
        null=True,
        help_text='Gets the email of the dealer'
    )
    fax_number = models.TextField(
        null=True,
        help_text='Get the fax number of a contact'
    )
    full_name = models.TextField(
        null=True,
        help_text='Get the name of a contact'
    )
    home_phone_number = models.TextField(
        null=True,
        help_text='Get the home phone number of a contact'
    )
    mobile_phone_number = models.TextField(
        null=True,
        help_text='Get the mobile phone number of a contact'
    )
    office_phone_number = models.TextField(
        null=True,
        help_text='Get the office phone number of a contact'
    )
    photo = models.TextField(
        null=True,
        help_text='The Url to agents profile photo'
    )
    position = models.TextField(
        null=True,
        help_text='Get the position of a contact'
    )
    url_slug = models.TextField(
        null=True,
        help_text='The property agent profile url identifier used to know '
                  'which agent profile to display'
    )

    class Meta:

        unique_together = (
            (
                'e_mail',
                'fax_number',
                'full_name',
                'home_phone_number',
                'mobile_phone_number',
                'office_phone_number',
                'photo',
                'position',
                'url_slug',
            ),
        )


class Attribute(models.Model):

    display_name = models.TextField(
        null=True,
        help_text='The name of the attribute, in a form suitable for '
                  'displaying to users. Not required when selling or editing.'
    )
    display_value = models.TextField(
        null=True,
        help_text='The value of the attribute as it needs to be displayed to '
                  'the end users'
    )
    name = models.TextField(
        null=True,
        help_text='A name which uniquely identifies the attribute. Required '
                  'when selling or editing.'
    )
    value = models.TextField(
        null=True,
        help_text='The string value of the attribute. When listing, the valid'
                  ' values for the attribute can be determined using the '
                  '“Retrieve attributes for a category” API. Use “false” or '
                  '“true” for boolean attributes. Required when selling or '
                  'editing.'
    )

    class Meta:

        unique_together = (
            (
                'display_name',
                'display_value',
                'name',
                'value',
            ),
        )


class Branding(models.Model):

    background_color = models.TextField(
        null=True,
        help_text='Banner outline/stroke colour, tick the checkbox before '
                  'saving to apply the new colour'
    )
    disable_banner = models.NullBooleanField(
        null=True,
        help_text='Disable the agent branding regardless of Super Feature '
                  'status'
    )
    large_banner_url = models.TextField(
        null=True,
        help_text='The url of a larger version of the logo'
    )
    large_square_logo = models.TextField(
        null=True,
        help_text='A large square branding image with dimensions of 480×480.'
    )
    large_wide_logo = models.TextField(
        null=True,
        help_text='A large rectangular branding image with dimensions of '
                  '480×200.'
    )
    office_location = models.TextField(
        null=True,
        help_text='The name of the office location'
    )
    stroke_color = models.TextField(
        null=True,
        help_text='Banner text colour, tick the checkbox before saving to '
                  'apply the new colour'
    )
    text_color = models.TextField(
        null=True,
        help_text='Banner background colour, tick the checkbox before saving '
                  'to apply the new colour'
    )

    class Meta:

        unique_together = (
            (
                'background_color',
                'disable_banner',
                'large_banner_url',
                'large_square_logo',
                'large_wide_logo',
                'office_location',
                'stroke_color',
                'text_color',
            ),
        )


class BroadbandTechnology(models.Model):

    availability = models.TextField(
        null=True,
        help_text='The availability of the broadband technology.'
    )
    completion = models.TextField(
        null=True,
        help_text='The estimated completion date of planned or underway '
                  'connections.'
    )
    max_down = models.FloatField(
        null=True,
        help_text='The maxiumum download speed (in megabits per second).'
    )
    max_up = models.FloatField(
        null=True,
        help_text='The maximum upload speed (in megabits per second).'
    )
    min_down = models.FloatField(
        null=True,
        help_text='The minimum download speed (in megabits per second).'
    )
    min_up = models.FloatField(
        null=True,
        help_text='The minimup upload speed (in megabits per second).'
    )
    name = models.TextField(
        help_text='The technology name.'
    )

    def __repr__(self):
        return ("BroadbandTechnology({!r}, down={}-{},"
                " up={}-{}").format(
            self.name, self.min_down, self.max_down, self.min_up, self.max_up
        )

    class Meta:

        unique_together = (
            (
                'availability',
                'completion',
                'max_down',
                'max_up',
                'min_down',
                'min_up',
                'name',
            ),
        )


class EmbeddedContent(models.Model):

    matterport_key = models.TextField(
        null=True,
        help_text='The Matterport video key for the listing’s InsideView '
                  'content.'
    )
    you_tube_video_key = models.TextField(
        null=True,
        help_text='The YouTube video key for the listing.'
    )

    class Meta:

        unique_together = (
            (
                'matterport_key',
                'you_tube_video_key',
            ),
        )


class FlatmateInformation(models.Model):

    current_flatmates = models.TextField(
        null=True,
        help_text='A description of the current flatmates.'
    )
    flatmates = models.IntegerField(
        help_text='The number of current flatmates.'
    )

    class Meta:

        unique_together = (
            (
                'current_flatmates',
                'flatmates',
            ),
        )


class GeographicLocation(models.Model):

    accuracy = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Address'),
            (3, 'Street'),
            (2, 'Suburb'),
        ),
        null=True,
        help_text='The accuracy of the geographic location (address, street '
                  'or suburb).'
    )
    latitude = models.FloatField(
        null=True,
        help_text='The latitude of the location, in degrees (WGS84).'
    )
    longitude = models.FloatField(
        null=True,
        help_text='The longitude of the location, in degrees (WGS84).'
    )

    def __repr__(self):
        return ("GeographicLocation(longitude={:0.7f},"
                " latitude={:0.7f}, accuracy={!r})").format(
            self.longitude, self.latitude, self.accuracy
        )

    class Meta:

        unique_together = (
            (
                'accuracy',
                'latitude',
                'longitude',
            ),
        )


class ListingType(enum.Enum):

    PROPERTY = enum.auto()
    FLATMATE = enum.auto()


class Listing(models.Model):

    listing_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the listing.',
    )
    listing_type = EnumIntegerField(
        ListingType,
        help_text='Type of listing(property, flatmate, etc.)',
    )
    address = models.TextField(
        null=True,
        help_text='The address to display.'
    )
    agency_reference = models.TextField(
        null=True,
        help_text='The reference to the agency.'
    )
    amenities = models.TextField(
        null=True,
        help_text='A list of the amenities in the area.'
    )
    as_at = models.DateTimeField(
        help_text='The date and time the response was generated on the '
                  'server.'
    )
    available_from = models.TextField(
        null=True,
        help_text='The date the property is available from.'
    )
    bathrooms = models.IntegerField(
        null=True,
        help_text='The number of bedrooms in the property.'
    )
    bedrooms = models.IntegerField(
        null=True,
        help_text='The number of bathrooms in the property.'
    )
    best_contact_time = models.TextField(
        null=True,
        help_text='The best time to contact the seller.'
    )
    body = models.TextField(
        null=True,
        help_text='The text used as the body of the item.'
    )
    end_date = models.DateTimeField(
        null=True,
        help_text='The date the listing will end.'
    )
    ideal_tenant = models.TextField(
        null=True,
        help_text='A description of the ideal tenant (are they tidy, a '
                  'professional couple, etc).'
    )
    max_tenants = models.IntegerField(
        null=True,
        help_text='The maximum number of tenents.'
    )
    parking = models.TextField(
        null=True,
        help_text='Information on the availability of parking.'
    )
    pets_okay = models.IntegerField(
        choices=(
            (0, 'NotSpecified'),
            (1, 'No'),
            (2, 'Yes'),
            (3, 'Negotiable'),
        ),
        null=True,
        help_text='Indicates whether pets are allowed by the landlord. This '
                  'information is available for flatmates wanted and '
                  'residential to rent listings.'
    )
    property_id = models.TextField(
        null=True,
        help_text='The property ID. This is different from the listing ID.'
    )
    property_type = models.TextField(
        null=True,
        help_text='The type of property. Currently valid values are: '
                  '“Apartment”, “Bare land”, “Car Park”, “Development site”, '
                  '“Dwelling”, “Hotel/Leisure”, “House”, “Industrial”, '
                  '“Lifestyle block”, “Office”, “Retail”, “Section”, '
                  '“Townhouse”, “Unit”, “Villa”.'
    )
    rent_per_week = models.FloatField(
        null=True,
        help_text='The rent payable per week, in NZD.'
    )
    smokers_okay = models.IntegerField(
        choices=(
            (0, 'NotSpecified'),
            (1, 'No'),
            (2, 'Yes'),
        ),
        null=True,
        help_text='Indicates whether smokers are allowed by the landlord. '
                  'This information is available for flatmates wanted and '
                  'residential to rent listings.'
    )
    start_date = models.DateTimeField(
        null=True,
        help_text='The date the listing was created.'
    )
    title = models.TextField(
        null=True,
        help_text='The listing title.'
    )
    whiteware = models.TextField(
        null=True,
        help_text='A description of what is included in the rent (if '
                  'furnished).'
    )

    agency = models.ForeignKey(
        'Agency',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='listed_item_detail_reverse_agency',
        help_text='The agency details if this is a job or property listing.'
    )
    attributes = models.ManyToManyField(
        'Attribute',
        related_name='listed_item_detail_reverse_attributes',
        help_text='The attributes for the item that are intended to be '
                  'displayed on the UI.'
    )
    broadband_technologies = models.ManyToManyField(
        'BroadbandTechnology',
        related_name='listed_item_detail_reverse_broadband_technologies',
        help_text='A list of broadband technology availability for property '
                  'listings.'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
    )
    embedded_content = models.ForeignKey(
        'EmbeddedContent',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text='The content keys that are embedded in the listing page '
                  '(e.g. YouTube Video Key).'
    )
    flatmate_information = models.ForeignKey(
        'FlatmateInformation',
        null=True,
        on_delete=models.CASCADE,
    )
    geographic_location = models.ForeignKey(
        'GeographicLocation',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        help_text='The geographic location (latitude and longitude) of a '
                  'property.'
    )
    member = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        help_text='The seller of the listing.'
    )
    photo = models.ForeignKey(
        'Photo',
        null=True,
        related_name='+',
        on_delete=models.DO_NOTHING,
        help_text='A collection of photos for the listing.'
    )
    photos = models.ManyToManyField(
        'Photo',
        related_name='listings',
        help_text='A collection of photos for the listing.'
    )
    suburb = models.ForeignKey(
        'Suburb',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='listings',
        help_text='The suburb where this item is located.'
    )

    def __repr__(self):
        return (
            '{}('
            '\n    listing_id={:d},'
            '\n    listing_type={!r},'
            '\n    address={!r},'
            '\n    agency_reference={!r},'
            '\n    available_from={!r},'
            '\n    bathrooms={!r},'
            '\n    bedrooms={!r},'
            '\n    end_date={!r},'
            '\n    max_tenants={!r},'
            '\n    pets_okay={!r},'
            '\n    property_id={!r},'
            '\n    property_type={!r},'
            '\n    rent_per_week={!r},'
            '\n    smokers_okay={!r},'
            '\n    start_date={!r},'
            '\n    title={!r},'
            '\n    agency={!r},'
            '\n    attributes={!r},'
            '\n    broadband_technologies={!r},'
            '\n    category={!r},'
            '\n    geographic_location={!r},'
            '\n    member={!r},'
            '\n    photo={!r},'
            '\n    photos={!r},'
            '\n    suburb={!r},'
            '\n)').format(
                self.__class__.__qualname__,
                self.listing_id,
                self.listing_type,
                self.address,
                self.agency_reference,
                self.available_from,
                self.bathrooms,
                self.bedrooms,
                self.end_date,
                self.max_tenants,
                self.pets_okay,
                self.property_id,
                self.property_type,
                self.rent_per_week,
                self.smokers_okay,
                self.start_date,
                self.title,
                self.agency,
                self.attributes,
                self.broadband_technologies,
                self.category,
                self.geographic_location,
                self.member,
                self.photo,
                self.photos,
                self.suburb,
        )


class Photo(models.Model):

    photo_id = models.IntegerField(
        primary_key=True,
        help_text=''
    )
    full_size = models.TextField(
        null=True,
        help_text='The URL for the full sized photo (scaled down to fit '
                  '670×502).'
    )
    gallery = models.TextField(
        null=True,
        help_text='The URL for the gallery sized photo (scaled down to fit '
                  '233×176).'
    )
    large = models.TextField(
        null=True,
        help_text='The URL for the large sized photo (scaled down to fit '
                  '352×264).'
    )
    list = models.TextField(
        null=True,
        help_text='The URL for the list view sized photo (scaled down to fit '
                  '160×120).'
    )
    medium = models.TextField(
        null=True,
        help_text='The URL for the medium sized photo (scaled down to fit '
                  '175×175).'
    )
    original_height = models.IntegerField(
        null=True,
        help_text='The original height of the photo.'
    )
    original_width = models.IntegerField(
        null=True,
        help_text='The original width of the photo.'
    )
    plus_size = models.TextField(
        null=True,
        help_text='The URL for the plus sized photo (scaled down to fit).'
    )
    thumbnail = models.TextField(
        null=True,
        help_text='The URL for the thumbnail sized photo (always 85×64, with '
                  'white borders).'
    )

    def __repr__(self):
        return (
            '{}('
            '\n    photo_id={:d},'
            '\n    original_height={!r},'
            '\n    original_width={!r},'
            '\n    full_size={!r},'
            '\n)').format(
                self.__class__.__qualname__,
                self.photo_id,
                self.original_height,
                self.original_width,
                self.full_size,
        )
