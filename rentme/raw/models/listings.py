import types

from django.db import models
import multidict

from .base import RawModel


class Address(RawModel):

    swagger_types = types.MappingProxyType({
        'address1': 'str',
        'address2': 'str',
        'city': 'str',
        'country': 'str',
        'name': 'str',
        'phone_number': 'str',
        'postcode': 'str',
        'suburb': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('address1', 'Address1'),
        ('address2', 'Address2'),
        ('city', 'City'),
        ('country', 'Country'),
        ('name', 'Name'),
        ('phone_number', 'PhoneNumber'),
        ('postcode', 'Postcode'),
        ('suburb', 'Suburb'),
    ]))

    address1 = models.TextField(
        null=True,
        help_text='The first line of the address.'
    )
    address2 = models.TextField(
        null=True,
        help_text='The second line of the address (optional).'
    )
    city = models.TextField(
        null=True,
        help_text='The city.'
    )
    country = models.TextField(
        null=True,
        help_text='The country (currently restricted to “New Zealand” or '
                  '“Australia”).'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the person whom the item is being delivered '
                  'to.'
    )
    phone_number = models.TextField(
        null=True,
        help_text='The contact phone number (optional).'
    )
    postcode = models.TextField(
        null=True,
        help_text='The postcode (optional).'
    )
    suburb = models.TextField(
        null=True,
        help_text='The suburb (optional).'
    )

    class Meta:

        unique_together = (
            (
                'address1',
                'address2',
                'city',
                'country',
                'name',
                'phone_number',
                'postcode',
                'suburb',
            ),
        )


class Agency(RawModel):

    swagger_types = types.MappingProxyType({
        'address': 'str',
        'agents': 'list[Agent]',
        'branding': 'Branding',
        'city': 'str',
        'e_mail': 'str',
        'fax_number': 'str',
        'id': 'int',
        'is_job_agency': 'bool',
        'is_licensed_property_agency': 'bool',
        'is_real_estate_agency': 'bool',
        'logo': 'str',
        'logo2': 'str',
        'name': 'str',
        'phone_number': 'str',
        'suburb': 'str',
        'website': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('address', 'Address'),
        ('agents', 'Agents'),
        ('branding', 'Branding'),
        ('city', 'City'),
        ('e_mail', 'EMail'),
        ('fax_number', 'FaxNumber'),
        ('id', 'Id'),
        ('is_job_agency', 'IsJobAgency'),
        ('is_licensed_property_agency', 'IsLicensedPropertyAgency'),
        ('is_real_estate_agency', 'IsRealEstateAgency'),
        ('logo', 'Logo'),
        ('logo2', 'Logo2'),
        ('name', 'Name'),
        ('phone_number', 'PhoneNumber'),
        ('suburb', 'Suburb'),
        ('website', 'Website'),
    ]))

    address = models.TextField(
        null=True,
        help_text='The address of the company HQ.'
    )
    agents = models.ManyToManyField(
        'Agent',
        related_name='agency_reverse_agents',
        help_text='The contact details of contacts within the agency.'
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

    class Meta:

        unique_together = (
            (
                'id',
            ),
        )


class Agent(RawModel):

    swagger_types = types.MappingProxyType({
        'e_mail': 'str',
        'fax_number': 'str',
        'full_name': 'str',
        'home_phone_number': 'str',
        'mobile_phone_number': 'str',
        'office_phone_number': 'str',
        'photo': 'str',
        'position': 'str',
        'url_slug': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('e_mail', 'EMail'),
        ('fax_number', 'FaxNumber'),
        ('full_name', 'FullName'),
        ('home_phone_number', 'HomePhoneNumber'),
        ('mobile_phone_number', 'MobilePhoneNumber'),
        ('office_phone_number', 'OfficePhoneNumber'),
        ('photo', 'Photo'),
        ('position', 'Position'),
        ('url_slug', 'UrlSlug'),
    ]))

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


class Attribute(RawModel):

    swagger_types = types.MappingProxyType({
        'display_name': 'str',
        'display_value': 'str',
        'is_required_for_sell': 'bool',
        'name': 'str',
        'options': 'list[AttributeOption]',
        'range': 'AttributeRange',
        'type': 'int',
        'value': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('display_name', 'DisplayName'),
        ('display_value', 'DisplayValue'),
        ('is_required_for_sell', 'IsRequiredForSell'),
        ('name', 'Name'),
        ('options', 'Options'),
        ('range', 'Range'),
        ('type', 'Type'),
        ('value', 'Value'),
    ]))

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
    is_required_for_sell = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the attribute must be present when '
                  'selling an item.'
    )
    name = models.TextField(
        null=True,
        help_text='A name which uniquely identifies the attribute. Required '
                  'when selling or editing.'
    )
    options = models.ManyToManyField(
        'AttributeOption',
        related_name='attribute_reverse_options',
        help_text='A list of options, if the attribute is restricted to a '
                  'fixed set of values. Not required when selling or editing.'
    )
    range = models.ForeignKey(
        'AttributeRange',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='attribute_reverse_range',
        help_text='The allowed range of the attribute. Only applies to '
                  'numeric attributes. Not required when selling or editing.'
    )
    type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Boolean'),
            (2, 'Integer'),
            (3, 'Decimal'),
            (4, 'String'),
            (5, 'DateTime'),
        ),
        null=True,
        help_text='The type of the attribute, which determines the range of '
                  'acceptable values. Not required when selling or editing.'
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
                'is_required_for_sell',
                'name',
                'range',
                'type',
                'value',
            ),
        )


class AttributeOption(RawModel):

    swagger_types = types.MappingProxyType({
        'count': 'int',
        'display': 'str',
        'value': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('count', 'Count'),
        ('display', 'Display'),
        ('value', 'Value'),
    ]))

    count = models.IntegerField(
        null=True,
        help_text='How many child elements are available.'
    )
    display = models.TextField(
        null=True,
        help_text='What should be displayed for this value (often the same).'
    )
    value = models.TextField(
        null=True,
        help_text='The value of the item as a string.'
    )

    class Meta:

        unique_together = (
            (
                'count',
                'display',
                'value',
            ),
        )


class AttributeRange(RawModel):

    swagger_types = types.MappingProxyType({
        'lower': 'str',
        'upper': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('lower', 'Lower'),
        ('upper', 'Upper'),
    ]))

    lower = models.TextField(
        null=True,
        help_text='The lowest allowed value of the attribute.'
    )
    upper = models.TextField(
        null=True,
        help_text='The highest allowed value of the attribute.'
    )

    class Meta:

        unique_together = (
            (
                'lower',
                'upper',
            ),
        )


class Bid(RawModel):

    swagger_types = types.MappingProxyType({
        'account': 'str',
        'bid_amount': 'float',
        'bid_date': 'datetime',
        'bidder': 'Member',
        'is_buy_now': 'bool',
        'is_by_mobile': 'bool',
        'is_by_proxy': 'bool',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('account', 'Account'),
        ('bid_amount', 'BidAmount'),
        ('bid_date', 'BidDate'),
        ('bidder', 'Bidder'),
        ('is_buy_now', 'IsBuyNow'),
        ('is_by_mobile', 'IsByMobile'),
        ('is_by_proxy', 'IsByProxy'),
    ]))

    account = models.TextField(
        null=True,
        help_text='The account the bid came from.'
    )
    bid_amount = models.FloatField(
        null=True,
        help_text='The amount of money the bid represents, in NZD.'
    )
    bid_date = models.DateTimeField(
        null=True,
        help_text='The date and time the bid was placed.'
    )
    bidder = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='bid_reverse_bidder',
        help_text='The member who placed the bid.'
    )
    is_buy_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the bid was a Buy Now bid.'
    )
    is_by_mobile = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the bid came from a mobile phone.'
    )
    is_by_proxy = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the bid was by proxy.'
    )

    class Meta:

        unique_together = (
            (
                'account',
                'bid_amount',
                'bid_date',
                'bidder',
                'is_buy_now',
                'is_by_mobile',
                'is_by_proxy',
            ),
        )


class BidCollection(RawModel):

    swagger_types = types.MappingProxyType({
        'list': 'list[Bid]',
        'page': 'int',
        'page_size': 'int',
        'total_count': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('list', 'List'),
        ('page', 'Page'),
        ('page_size', 'PageSize'),
        ('total_count', 'TotalCount'),
    ]))

    list = models.ManyToManyField(
        'Bid',
        related_name='bid_collection_reverse_list',
        help_text='A list of the results in the current page.'
    )
    page = models.IntegerField(
        null=True,
        help_text='The index of the current page of results (starts at 1).'
    )
    page_size = models.IntegerField(
        null=True,
        help_text='The number of results in the current page.'
    )
    total_count = models.IntegerField(
        null=True,
        help_text='The total number of results in the collection. Can be '
                  'larger than the number of returned results.'
    )

    class Meta:

        unique_together = (
            (
                'page',
                'page_size',
                'total_count',
            ),
        )


class Branding(RawModel):

    swagger_types = types.MappingProxyType({
        'background_color': 'str',
        'disable_banner': 'bool',
        'large_banner_url': 'str',
        'large_square_logo': 'str',
        'large_wide_logo': 'str',
        'office_location': 'str',
        'stroke_color': 'str',
        'text_color': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('background_color', 'BackgroundColor'),
        ('disable_banner', 'DisableBanner'),
        ('large_banner_url', 'LargeBannerURL'),
        ('large_square_logo', 'LargeSquareLogo'),
        ('large_wide_logo', 'LargeWideLogo'),
        ('office_location', 'OfficeLocation'),
        ('stroke_color', 'StrokeColor'),
        ('text_color', 'TextColor'),
    ]))

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


class BroadbandTechnology(RawModel):

    swagger_types = types.MappingProxyType({
        'availability': 'str',
        'completion': 'str',
        'max_down': 'float',
        'max_up': 'float',
        'min_down': 'float',
        'min_up': 'float',
        'name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('availability', 'Availability'),
        ('completion', 'Completion'),
        ('max_down', 'MaxDown'),
        ('max_up', 'MaxUp'),
        ('min_down', 'MinDown'),
        ('min_up', 'MinUp'),
        ('name', 'Name'),
    ]))

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
        null=True,
        help_text='The technology name.'
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


class Charity(RawModel):

    swagger_types = types.MappingProxyType({
        'charity_type': 'int',
        'description': 'str',
        'image_source': 'str',
        'tagline': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('charity_type', 'CharityType'),
        ('description', 'Description'),
        ('image_source', 'ImageSource'),
        ('tagline', 'Tagline'),
    ]))

    charity_type = models.IntegerField(
        choices=(
            (1, 'ForestAndBird'),
            (2, 'Plunket'),
        ),
        null=True,
        help_text='The unique identifier of the charity.'
    )
    description = models.TextField(
        null=True,
        help_text='The name of the charity e.g. “Plunket”, “Kiwis for kiwi”.'
    )
    image_source = models.TextField(
        null=True,
        help_text='The url source location for this charity’s brand image.'
    )
    tagline = models.TextField(
        null=True,
        help_text='A short description of what the charity does.'
    )

    class Meta:

        unique_together = (
            (
                'charity_type',
                'description',
                'image_source',
                'tagline',
            ),
        )


class ContactDetails(RawModel):

    swagger_types = types.MappingProxyType({
        'best_contact_time': 'str',
        'contact_name': 'str',
        'mobile_phone_number': 'str',
        'phone_number': 'str',
        'website': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('best_contact_time', 'BestContactTime'),
        ('contact_name', 'ContactName'),
        ('mobile_phone_number', 'MobilePhoneNumber'),
        ('phone_number', 'PhoneNumber'),
        ('website', 'Website'),
    ]))

    best_contact_time = models.TextField(
        null=True,
        help_text='The best time to contact the seller.'
    )
    contact_name = models.TextField(
        null=True,
        help_text='The name of the service provider.'
    )
    mobile_phone_number = models.TextField(
        null=True,
        help_text='The seller’s mobile phone number.'
    )
    phone_number = models.TextField(
        null=True,
        help_text='The seller’s contact phone number (landline).'
    )
    website = models.TextField(
        null=True,
        help_text='The service provider’s website.'
    )

    class Meta:

        unique_together = (
            (
                'best_contact_time',
                'contact_name',
                'mobile_phone_number',
                'phone_number',
                'website',
            ),
        )


class CurrentShippingPromotion(RawModel):

    swagger_types = types.MappingProxyType({
        'threshold': 'int',
        'threshold_type': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('threshold', 'Threshold'),
        ('threshold_type', 'ThresholdType'),
    ]))

    threshold = models.IntegerField(
        null=True,
        help_text='The threshold a buyer needs to reach to qualify for this '
                  'promotional shipping offer.'
    )
    threshold_type = models.IntegerField(
        choices=(
            (1, 'Price'),
            (2, 'Item'),
        ),
        null=True,
        help_text='The type of threshold.'
    )

    class Meta:

        unique_together = (
            (
                'threshold',
                'threshold_type',
            ),
        )


class Dealer(RawModel):

    swagger_types = types.MappingProxyType({
        'e_mail': 'str',
        'fax_number': 'str',
        'full_name': 'str',
        'home_phone_number': 'str',
        'mobile_phone_number': 'str',
        'office_phone_number': 'str',
        'position': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('e_mail', 'EMail'),
        ('fax_number', 'FaxNumber'),
        ('full_name', 'FullName'),
        ('home_phone_number', 'HomePhoneNumber'),
        ('mobile_phone_number', 'MobilePhoneNumber'),
        ('office_phone_number', 'OfficePhoneNumber'),
        ('position', 'Position'),
    ]))

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
    position = models.TextField(
        null=True,
        help_text='Get the position of a contact'
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
                'position',
            ),
        )


class Dealership(RawModel):

    swagger_types = types.MappingProxyType({
        'about_us': 'str',
        'address': 'str',
        'branding': 'Branding',
        'city': 'str',
        'dealers': 'list[Dealer]',
        'e_mail': 'str',
        'fax_number': 'str',
        'id': 'int',
        'listing_counts': 'DealershipListingCounts',
        'logo': 'str',
        'logo2': 'str',
        'name': 'str',
        'phone_number': 'str',
        'phone_numbers': 'list[DealershipPhoneNumbers]',
        'showroom': 'DealerShowroom',
        'suburb': 'str',
        'website': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('about_us', 'AboutUs'),
        ('address', 'Address'),
        ('branding', 'Branding'),
        ('city', 'City'),
        ('dealers', 'Dealers'),
        ('e_mail', 'EMail'),
        ('fax_number', 'FaxNumber'),
        ('id', 'Id'),
        ('listing_counts', 'ListingCounts'),
        ('logo', 'Logo'),
        ('logo2', 'Logo2'),
        ('name', 'Name'),
        ('phone_number', 'PhoneNumber'),
        ('phone_numbers', 'PhoneNumbers'),
        ('showroom', 'Showroom'),
        ('suburb', 'Suburb'),
        ('website', 'Website'),
    ]))

    about_us = models.TextField(
        null=True,
        help_text='Description of the Dealership'
    )
    address = models.TextField(
        null=True,
        help_text='The address of the company HQ.'
    )
    branding = models.ForeignKey(
        'Branding',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='dealership_reverse_branding',
        help_text='The branding object for the company.'
    )
    city = models.TextField(
        null=True,
        help_text='The city where the company HQ is located.'
    )
    dealers = models.ManyToManyField(
        'Dealer',
        related_name='dealership_reverse_dealers',
        help_text='Gets the contact details of contacts within the dealership'
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
    listing_counts = models.ForeignKey(
        'DealershipListingCounts',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='dealership_reverse_listing_counts',
        help_text='Count of listings of dealership'
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
    phone_numbers = models.ManyToManyField(
        'DealershipPhoneNumbers',
        related_name='dealership_reverse_phone_numbers',
        help_text='Array of up to two phone numbers which can be used to '
                  'reach the dealership'
    )
    showroom = models.ForeignKey(
        'DealerShowroom',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='dealership_reverse_showroom',
        help_text='The show room of the Dealership'
    )
    suburb = models.TextField(
        null=True,
        help_text='The suburb where the company HQ is located.'
    )
    website = models.TextField(
        null=True,
        help_text='The URL of the company website.'
    )

    class Meta:

        unique_together = (
            (
                'id',
            ),
        )


class DealershipListingCounts(RawModel):

    swagger_types = types.MappingProxyType({
        'bikes': 'int',
        'boats': 'int',
        'cars': 'int',
        'total': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('bikes', 'Bikes'),
        ('boats', 'Boats'),
        ('cars', 'Cars'),
        ('total', 'Total'),
    ]))

    bikes = models.IntegerField(
        null=True,
        help_text='Count of motorbike listings'
    )
    boats = models.IntegerField(
        null=True,
        help_text='Count of motorboat listings'
    )
    cars = models.IntegerField(
        null=True,
        help_text='Count of car listings'
    )
    total = models.IntegerField(
        null=True,
        help_text='Total of listings'
    )

    class Meta:

        unique_together = (
            (
                'bikes',
                'boats',
                'cars',
                'total',
            ),
        )


class DealershipPhoneNumbers(RawModel):

    expect_single_value = 'value'
    swagger_types = types.MappingProxyType({
        'value': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('value', 'value'),
    ]))

    value = models.TextField(
        null=True,
    )

    class Meta:

        unique_together = (
            (
                'value',
            ),
        )


class DealerShowroom(RawModel):

    swagger_types = types.MappingProxyType({
        'background_colour': 'str',
        'banner': 'str',
        'id': 'int',
        'logo': 'str',
        'url': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('background_colour', 'BackgroundColour'),
        ('banner', 'Banner'),
        ('id', 'Id'),
        ('logo', 'Logo'),
        ('url', 'Url'),
    ]))

    background_colour = models.TextField(
        null=True,
        help_text='Background colour of the Showroom banner / logo'
    )
    banner = models.TextField(
        null=True,
        help_text='Banner of the Showroom'
    )
    id = models.IntegerField(
        primary_key=True,
        help_text='ID of the Showroom'
    )
    logo = models.TextField(
        null=True,
        help_text='Logo of the Showroom'
    )
    url = models.TextField(
        null=True,
        help_text='Url of the Showroom'
    )

    class Meta:

        unique_together = (
            (
                'id',
            ),
        )


class EmbeddedContent(RawModel):

    swagger_types = types.MappingProxyType({
        'matterport_key': 'str',
        'you_tube_video_key': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('matterport_key', 'MatterportKey'),
        ('you_tube_video_key', 'YouTubeVideoKey'),
    ]))

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


class FixedPriceOfferDetails(RawModel):

    swagger_types = types.MappingProxyType({
        'offer_expiry_date': 'datetime',
        'offer_price': 'float',
        'quantity': 'int',
        'recipients': 'list[FixedPriceOfferRecipient]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('offer_expiry_date', 'OfferExpiryDate'),
        ('offer_price', 'OfferPrice'),
        ('quantity', 'Quantity'),
        ('recipients', 'Recipients'),
    ]))

    offer_expiry_date = models.DateTimeField(
        null=True,
        help_text='The date and time the fixed price offer expires.'
    )
    offer_price = models.FloatField(
        null=True,
        help_text='The offer price of the item on offer. For offers with more'
                  ' than one available item, this is the price per item. The '
                  'price for shipping is not included.'
    )
    quantity = models.IntegerField(
        null=True,
        help_text='The number of items that are available. Buyers are able to'
                  ' purchase one or more of this item until the stock runs '
                  'out or the offer ends.'
    )
    recipients = models.ManyToManyField(
        'FixedPriceOfferRecipient',
        related_name='fixed_price_offer_details_reverse_recipients',
        help_text='A list of recipients for the offer. Only available if you '
                  'are the seller.'
    )

    class Meta:

        unique_together = (
            (
                'offer_expiry_date',
                'offer_price',
                'quantity',
            ),
        )


class FixedPriceOfferRecipient(RawModel):

    swagger_types = types.MappingProxyType({
        'decision': 'int',
        'member': 'Member',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('decision', 'Decision'),
        ('member', 'Member'),
    ]))

    decision = models.IntegerField(
        choices=(
            (0, 'NoDecision'),
            (1, 'Declined'),
            (2, 'Accepted'),
        ),
        null=True,
        help_text='The response of the member to the offer.'
    )
    member = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='fixed_price_offer_recipient_reverse_member',
        help_text='Member details for the recipient of the offer.'
    )

    class Meta:

        unique_together = (
            (
                'decision',
                'member',
            ),
        )


class GeographicLocation(RawModel):

    swagger_types = types.MappingProxyType({
        'accuracy': 'int',
        'easting': 'int',
        'latitude': 'float',
        'longitude': 'float',
        'northing': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('accuracy', 'Accuracy'),
        ('easting', 'Easting'),
        ('latitude', 'Latitude'),
        ('longitude', 'Longitude'),
        ('northing', 'Northing'),
    ]))

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
    easting = models.IntegerField(
        null=True,
        help_text='The easting of the location, in metres (NZTM).'
    )
    latitude = models.FloatField(
        null=True,
        help_text='The latitude of the location, in degrees (WGS84).'
    )
    longitude = models.FloatField(
        null=True,
        help_text='The longitude of the location, in degrees (WGS84).'
    )
    northing = models.IntegerField(
        null=True,
        help_text='The northing of the location, in metres (NZTM).'
    )

    class Meta:

        unique_together = (
            (
                'accuracy',
                'easting',
                'latitude',
                'longitude',
                'northing',
            ),
        )


class LargeBannerImage(RawModel):

    swagger_types = types.MappingProxyType({
        'large': 'str',
        'medium': 'str',
        'small': 'str',
        'x_large': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('large', 'Large'),
        ('medium', 'Medium'),
        ('small', 'Small'),
        ('x_large', 'XLarge'),
    ]))

    large = models.TextField(
        null=True,
        help_text='The URL of the promotional image in large size 1024×576.'
    )
    medium = models.TextField(
        null=True,
        help_text='The URL of the promotional image in medium size 768×432.'
    )
    small = models.TextField(
        null=True,
        help_text='The URL of the promotional image in small size 320×180'
    )
    x_large = models.TextField(
        null=True,
        help_text='The URL of the promotional image in extra large size '
                  '1440×810.'
    )

    class Meta:

        unique_together = (
            (
                'large',
                'medium',
                'small',
                'x_large',
            ),
        )


class ListedItemDetail(RawModel):

    swagger_types = types.MappingProxyType({
        'agency': 'Agency',
        'allows_pickups': 'int',
        'as_at': 'datetime',
        'attributes': 'list[Attribute]',
        'authenticated_members_only': 'bool',
        'available_to_buy': 'str',
        'bid_count': 'int',
        'bidder_and_watchers': 'int',
        'bids': 'BidCollection',
        'body': 'str',
        'branding': 'Branding',
        'broadband_technologies': 'list[BroadbandTechnology]',
        'buy_now_price': 'float',
        'can_add_to_cart': 'bool',
        'can_offer': 'bool',
        'can_relist': 'bool',
        'can_use_pay_now_instant': 'bool',
        'cart_item_id': 'int',
        'category': 'str',
        'category_name': 'str',
        'category_path': 'str',
        'closed_offer': 'FixedPriceOfferDetails',
        'contact_count': 'int',
        'contact_details': 'ContactDetails',
        'current_auto_bid': 'float',
        'current_shipping_promotion': 'CurrentShippingPromotion',
        'dealership': 'Dealership',
        'donation_recipient': 'Charity',
        'embedded_content': 'EmbeddedContent',
        'end_date': 'datetime',
        'external_reference_id': 'str',
        'firearms_license_required_to_buy': 'bool',
        'formatted_start_date': 'str',
        'geographic_location': 'GeographicLocation',
        'has_buy_now': 'bool',
        'has_contact_details': 'bool',
        'has_gallery': 'bool',
        'has_home_page_feature': 'bool',
        'has_multiple': 'bool',
        'has_pay_now': 'bool',
        'has_reserve': 'bool',
        'hidden_attributes': 'list[Attribute]',
        'is_bold': 'bool',
        'is_buy_now_only': 'bool',
        'is_classified': 'bool',
        'is_clearance': 'bool',
        'is_eligible_for_bidding': 'bool',
        'is_eligible_for_buy_now': 'bool',
        'is_eligible_for_buyer_protection': 'bool',
        'is_featured': 'bool',
        'is_flat_shipping_charge': 'bool',
        'is_highlighted': 'bool',
        'is_in_cart': 'bool',
        'is_in_trade_protected': 'bool',
        'is_leading': 'bool',
        'is_new': 'bool',
        'is_on_watch_list': 'bool',
        'is_or_near_offer': 'bool',
        'is_outbid': 'bool',
        'is_reserve_met': 'bool',
        'is_super_featured': 'bool',
        'listing_id': 'int',
        'max_bid_amount': 'float',
        'member': 'Member',
        'member_profile': 'SimpleMemberProfile',
        'member_request_information': 'MemberRequestInformation',
        'minimum_next_bid_amount': 'float',
        'motor_web_basic_report': 'MotorWebBasicReport',
        'note_date': 'datetime',
        'number_of_payments': 'int',
        'offer_status': 'int',
        'open_homes': 'list[OpenHome]',
        'over18_declaration_required_to_buy': 'bool',
        'payment_amount': 'float',
        'payment_interval': 'str',
        'payment_method_fee': 'float',
        'payment_options': 'str',
        'pending_offer': 'FixedPriceOfferDetails',
        'percentage_off': 'int',
        'photo_id': 'int',
        'photos': 'list[Photo]',
        'positive_review_count': 'int',
        'price_display': 'str',
        'quantity': 'int',
        'questions': 'Questions',
        'refund_collection': 'list[RefundDetails]',
        'region': 'str',
        'region_id': 'int',
        'relisted_item_id': 'int',
        'remaining_gallery_plus_relists': 'int',
        'reserve_price': 'float',
        'reserve_state': 'int',
        'sales': 'list[Sale]',
        'send_payment_instructions': 'bool',
        'shipping_options': 'list[ShippingOption]',
        'sku': 'str',
        'sponsor_links': 'list[SponsorLink]',
        'start_date': 'datetime',
        'start_price': 'float',
        'store': 'Store',
        'subtitle': 'str',
        'suburb': 'str',
        'suburb_id': 'int',
        'super_feature_end_date': 'datetime',
        'supports_questions_and_answers': 'bool',
        'title': 'str',
        'total_review_count': 'int',
        'unanswered_question_count': 'int',
        'variant_definition': 'VariantDefinition',
        'view_count': 'int',
        'was_price': 'float',
        'withdrawn_by_seller': 'bool',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('agency', 'Agency'),
        ('allows_pickups', 'AllowsPickups'),
        ('as_at', 'AsAt'),
        ('attributes', 'Attributes'),
        ('authenticated_members_only', 'AuthenticatedMembersOnly'),
        ('available_to_buy', 'AvailableToBuy'),
        ('bid_count', 'BidCount'),
        ('bidder_and_watchers', 'BidderAndWatchers'),
        ('bids', 'Bids'),
        ('body', 'Body'),
        ('branding', 'Branding'),
        ('broadband_technologies', 'BroadbandTechnologies'),
        ('buy_now_price', 'BuyNowPrice'),
        ('can_add_to_cart', 'CanAddToCart'),
        ('can_offer', 'CanOffer'),
        ('can_relist', 'CanRelist'),
        ('can_use_pay_now_instant', 'CanUsePayNowInstant'),
        ('cart_item_id', 'CartItemId'),
        ('category', 'Category'),
        ('category_name', 'CategoryName'),
        ('category_path', 'CategoryPath'),
        ('closed_offer', 'ClosedOffer'),
        ('contact_count', 'ContactCount'),
        ('contact_details', 'ContactDetails'),
        ('current_auto_bid', 'CurrentAutoBid'),
        ('current_shipping_promotion', 'CurrentShippingPromotion'),
        ('dealership', 'Dealership'),
        ('donation_recipient', 'DonationRecipient'),
        ('embedded_content', 'EmbeddedContent'),
        ('end_date', 'EndDate'),
        ('external_reference_id', 'ExternalReferenceId'),
        ('firearms_license_required_to_buy', 'FirearmsLicenseRequiredToBuy'),
        ('formatted_start_date', 'FormattedStartDate'),
        ('geographic_location', 'GeographicLocation'),
        ('has_buy_now', 'HasBuyNow'),
        ('has_contact_details', 'HasContactDetails'),
        ('has_gallery', 'HasGallery'),
        ('has_home_page_feature', 'HasHomePageFeature'),
        ('has_multiple', 'HasMultiple'),
        ('has_pay_now', 'HasPayNow'),
        ('has_reserve', 'HasReserve'),
        ('hidden_attributes', 'HiddenAttributes'),
        ('is_bold', 'IsBold'),
        ('is_buy_now_only', 'IsBuyNowOnly'),
        ('is_classified', 'IsClassified'),
        ('is_clearance', 'IsClearance'),
        ('is_eligible_for_bidding', 'IsEligibleForBidding'),
        ('is_eligible_for_buy_now', 'IsEligibleForBuyNow'),
        ('is_eligible_for_buyer_protection', 'IsEligibleForBuyerProtection'),
        ('is_featured', 'IsFeatured'),
        ('is_flat_shipping_charge', 'IsFlatShippingCharge'),
        ('is_highlighted', 'IsHighlighted'),
        ('is_in_cart', 'IsInCart'),
        ('is_in_trade_protected', 'IsInTradeProtected'),
        ('is_leading', 'IsLeading'),
        ('is_new', 'IsNew'),
        ('is_on_watch_list', 'IsOnWatchList'),
        ('is_or_near_offer', 'IsOrNearOffer'),
        ('is_outbid', 'IsOutbid'),
        ('is_reserve_met', 'IsReserveMet'),
        ('is_super_featured', 'IsSuperFeatured'),
        ('listing_id', 'ListingId'),
        ('max_bid_amount', 'MaxBidAmount'),
        ('member', 'Member'),
        ('member_profile', 'MemberProfile'),
        ('member_request_information', 'MemberRequestInformation'),
        ('minimum_next_bid_amount', 'MinimumNextBidAmount'),
        ('motor_web_basic_report', 'MotorWebBasicReport'),
        ('note_date', 'NoteDate'),
        ('number_of_payments', 'NumberOfPayments'),
        ('offer_status', 'OfferStatus'),
        ('open_homes', 'OpenHomes'),
        ('over18_declaration_required_to_buy', 'Over18DeclarationRequiredToBuy'),
        ('payment_amount', 'PaymentAmount'),
        ('payment_interval', 'PaymentInterval'),
        ('payment_method_fee', 'PaymentMethodFee'),
        ('payment_options', 'PaymentOptions'),
        ('pending_offer', 'PendingOffer'),
        ('percentage_off', 'PercentageOff'),
        ('photo_id', 'PhotoId'),
        ('photos', 'Photos'),
        ('positive_review_count', 'PositiveReviewCount'),
        ('price_display', 'PriceDisplay'),
        ('quantity', 'Quantity'),
        ('questions', 'Questions'),
        ('refund_collection', 'RefundCollection'),
        ('region', 'Region'),
        ('region_id', 'RegionId'),
        ('relisted_item_id', 'RelistedItemId'),
        ('remaining_gallery_plus_relists', 'RemainingGalleryPlusRelists'),
        ('reserve_price', 'ReservePrice'),
        ('reserve_state', 'ReserveState'),
        ('sku', 'SKU'),
        ('sales', 'Sales'),
        ('send_payment_instructions', 'SendPaymentInstructions'),
        ('shipping_options', 'ShippingOptions'),
        ('sponsor_links', 'SponsorLinks'),
        ('start_date', 'StartDate'),
        ('start_price', 'StartPrice'),
        ('store', 'Store'),
        ('subtitle', 'Subtitle'),
        ('suburb', 'Suburb'),
        ('suburb_id', 'SuburbId'),
        ('super_feature_end_date', 'SuperFeatureEndDate'),
        ('supports_questions_and_answers', 'SupportsQuestionsAndAnswers'),
        ('title', 'Title'),
        ('total_review_count', 'TotalReviewCount'),
        ('unanswered_question_count', 'UnansweredQuestionCount'),
        ('variant_definition', 'VariantDefinition'),
        ('view_count', 'ViewCount'),
        ('was_price', 'WasPrice'),
        ('withdrawn_by_seller', 'WithdrawnBySeller'),
    ]))

    agency = models.ForeignKey(
        'Agency',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_agency',
        help_text='The agency details if this is a job or property listing.'
    )
    allows_pickups = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Allow'),
            (2, 'Demand'),
            (3, 'Forbid'),
        ),
        null=True,
        help_text='Indicates whether the seller allows pickup.'
    )
    as_at = models.DateTimeField(
        null=True,
        help_text='The date and time the response was generated on the '
                  'server.'
    )
    attributes = models.ManyToManyField(
        'Attribute',
        related_name='listed_item_detail_reverse_attributes',
        help_text='The attributes for the item that are intended to be '
                  'displayed on the UI.'
    )
    authenticated_members_only = models.NullBooleanField(
        null=True,
        help_text='Indicates whether bidding on this auction is restricted to'
                  ' authenticated members. Note that there are many '
                  'restrictions on non-authenticated users. For more '
                  'information, see the help article on becoming '
                  'authenticated .'
    )
    available_to_buy = models.TextField(
        null=True,
        help_text='The amount of listings available for purchase. If greater '
                  'than 10, 10+ will be displayed.'
    )
    bid_count = models.IntegerField(
        null=True,
        help_text='The number of bids on the item.'
    )
    bidder_and_watchers = models.IntegerField(
        null=True,
        help_text='The number of bidders and watcher for this listing.'
    )
    bids = models.ForeignKey(
        'BidCollection',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_bids',
        help_text='A list of the last 10 bids for the listing.'
    )
    body = models.TextField(
        null=True,
        help_text='The text used as the body of the item.'
    )
    branding = models.ForeignKey(
        'Branding',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_branding',
        help_text='A list of branding images associated with this listing.'
    )
    broadband_technologies = models.ManyToManyField(
        'BroadbandTechnology',
        related_name='listed_item_detail_reverse_broadband_technologies',
        help_text='A list of broadband technology availability for property '
                  'listings.'
    )
    buy_now_price = models.FloatField(
        null=True,
        help_text='The Buy Now price.'
    )
    can_add_to_cart = models.NullBooleanField(
        null=True,
        help_text='Indicates if the item can be added to members cart.'
    )
    can_offer = models.NullBooleanField(
        null=True,
        help_text='Indicates whether a fixed price offer can be created for '
                  'the listing. You can use this flag to hide the FPO button '
                  'in your UI or to avoid a useless FPO API call. Note that '
                  'if this flag is true it does not guarantee that a '
                  'subsequent FPO operation will succeed.'
    )
    can_relist = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing can be relisted using the '
                  'relist or relist with edits API. You can use this flag to '
                  'hide the relist button in your UI or to avoid a useless '
                  'relist API call. Note that if this flag is true it does '
                  'not guarantee that a subsequent relist operation will '
                  'succeed.'
    )
    can_use_pay_now_instant = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the PayNowInstant is available for this '
                  'listing.'
    )
    cart_item_id = models.IntegerField(
        null=True,
        help_text='the cartItemId if the item is already in the members cart.'
    )
    category = models.TextField(
        null=True,
        help_text='The listing category.'
    )
    category_name = models.TextField(
        null=True,
        help_text='The display name of the category.'
    )
    category_path = models.TextField(
        null=True,
        help_text='The category path.'
    )
    closed_offer = models.ForeignKey(
        'FixedPriceOfferDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_closed_offer',
        help_text='Contains details of a fixed price offer that was made, but'
                  ' is no longer available, either because it was accepted, '
                  'it expired or all recipients declined the offer. Only '
                  'available if you are the seller or a recipient of the '
                  'offer.'
    )
    contact_count = models.IntegerField(
        null=True,
        help_text='The number of contacts received for this listing, either '
                  'emails, applications, or clicks-to-apply. Only available '
                  'if you are the seller.'
    )
    contact_details = models.ForeignKey(
        'ContactDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_contact_details',
        help_text='The contact details for a personal listing.'
    )
    current_auto_bid = models.FloatField(
        null=True,
        help_text='If you are the bidder then the highest AutoBid value is '
                  'returned'
    )
    current_shipping_promotion = models.ForeignKey(
        'CurrentShippingPromotion',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_current_shipping_promotion',
        help_text='A list of shipping promotions that are currently active '
                  'for this listing'
    )
    dealership = models.ForeignKey(
        'Dealership',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_dealership',
        help_text='The dealership details if this is a car dealer listing.'
    )
    donation_recipient = models.ForeignKey(
        'Charity',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_donation_recipient',
        help_text='Indicates the seller will round up their success fees to '
                  'the nearest dollar and donate the difference to the '
                  'selected charity.'
    )
    embedded_content = models.ForeignKey(
        'EmbeddedContent',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_embedded_content',
        help_text='The content keys that are embedded in the listing page '
                  '(e.g. YouTube Video Key).'
    )
    end_date = models.DateTimeField(
        null=True,
        help_text='The date the listing will end.'
    )
    external_reference_id = models.TextField(
        null=True,
        help_text='The external reference ID, if one exists. Only available '
                  'to the seller of a listing.'
    )
    firearms_license_required_to_buy = models.NullBooleanField(
        null=True,
        help_text='Indicates whether a buyer is required to enter their '
                  'firearms license number. Applies to firearms listings '
                  '(e.g. Sports > Hunting & shooting > Rifles).'
    )
    formatted_start_date = models.TextField(
        null=True,
        help_text='Listing start date, displayed as a string. Currently '
                  'applies to Motors Classified listings only.'
    )
    geographic_location = models.ForeignKey(
        'GeographicLocation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_geographic_location',
        help_text='The geographic location (latitude and longitude) of a '
                  'property.'
    )
    has_buy_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Buy Now.'
    )
    has_contact_details = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing has contact details'
    )
    has_gallery = models.NullBooleanField(
        null=True,
        help_text='Is this a gallery listing?'
    )
    has_home_page_feature = models.NullBooleanField(
        null=True,
        help_text='Is this a homepage feature listing?'
    )
    has_multiple = models.NullBooleanField(
        null=True,
        help_text='Indicates whether there is more than one item available. '
                  'Only applicable for Buy Now Only listings.'
    )
    has_pay_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Pay Now.'
    )
    has_reserve = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has a reserve.'
    )
    hidden_attributes = models.ManyToManyField(
        'Attribute',
        related_name='listed_item_detail_reverse_hidden_attributes',
        help_text='The attributes for the item that are not intended to be '
                  'displayed on the UI.'
    )
    is_bold = models.NullBooleanField(
        null=True,
        help_text='Is this a bold listing?'
    )
    is_buy_now_only = models.NullBooleanField(
        null=True,
        help_text='Indicates whether or not this is a Buy Now Only listing.'
    )
    is_classified = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item is a classified.'
    )
    is_clearance = models.NullBooleanField(
        null=True,
        help_text='This indicates that the listing is a clearance item. '
                  'Clearance listings include listings with was/now pricing '
                  'and general clearance stock.'
    )
    is_eligible_for_bidding = models.NullBooleanField(
        null=True,
        help_text='Indicates whether afterpay is an eligible payment method '
                  'for Buy Now'
    )
    is_eligible_for_buy_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether afterpay is an eligible payment method '
                  'for Buy Now'
    )
    is_eligible_for_buyer_protection = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing is eligible for buyer '
                  'protection'
    )
    is_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a featured listing?'
    )
    is_flat_shipping_charge = models.NullBooleanField(
        null=True,
        help_text='Indicates whether one flat shipping fee will be charged if'
                  ' more than one of this item is purchased. Only applicable '
                  'for Buy Now Only listings.'
    )
    is_highlighted = models.NullBooleanField(
        null=True,
        help_text='Is this a highlighted listing?'
    )
    is_in_cart = models.NullBooleanField(
        null=True,
        help_text='Indicates if the item is also in the members cart.'
    )
    is_in_trade_protected = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing is protected by the Consumer'
                  ' Guarantees Act'
    )
    is_leading = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the authenticated user is leading the '
                  'bidding.'
    )
    is_new = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item is marked as new.'
    )
    is_on_watch_list = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item is on the authenticated '
                  'member’s watchlist.'
    )
    is_or_near_offer = models.NullBooleanField(
        null=True,
        help_text='Indicates whether a near offer is accepted.'
    )
    is_outbid = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the authenticated user has been outbid. '
                  'This will be false if the authenticated user has not made '
                  'any bids.'
    )
    is_reserve_met = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item’s reserve has been met.'
    )
    is_super_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a super featured listing?'
    )
    listing_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the listing.'
    )
    max_bid_amount = models.FloatField(
        null=True,
        help_text='The current leading bid amount.'
    )
    member = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_member',
        help_text='The seller of the listing.'
    )
    member_profile = models.ForeignKey(
        'SimpleMemberProfile',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_member_profile',
        help_text='This listing member’s public profile information.'
    )
    member_request_information = models.ForeignKey(
        'MemberRequestInformation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_member_request_information',
        help_text='Provides information relating to the member regarding '
                  'their ability to request a relist or offer and the status '
                  'of any request.'
    )
    minimum_next_bid_amount = models.FloatField(
        null=True,
        help_text='The smallest amount that will be accepted for the next '
                  'bid. Only applicable to auctions which allow bidding (i.e.'
                  ' not classifieds and not Buy Now Only auctions). You must '
                  'still check for the “bid too small” error when using this '
                  'value, as someone may make a bid after you have checked '
                  'this value but before you have finished placing your bid.'
    )
    motor_web_basic_report = models.ForeignKey(
        'MotorWebBasicReport',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_motor_web_basic_report',
        help_text='MotorWeb basic report for car listings if purchased by the'
                  ' seller.'
    )
    note_date = models.DateTimeField(
        null=True,
        help_text='The date of the note on an item.'
    )
    number_of_payments = models.IntegerField(
        null=True,
        help_text='Indicates the number of payments'
    )
    offer_status = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Active'),
            (2, 'Withdrawn'),
            (3, 'Expired'),
            (4, 'Declined'),
            (5, 'Accepted'),
        ),
        null=True,
        help_text='The status of the fixed price offer for this listing (if '
                  'there is one). Only available if you are the seller or a '
                  'recipient of the offer.'
    )
    open_homes = models.ManyToManyField(
        'OpenHome',
        related_name='listed_item_detail_reverse_open_homes',
        help_text='A collection of open home times for this listing. Only '
                  'applies to open home listings.'
    )
    over18_declaration_required_to_buy = models.NullBooleanField(
        null=True,
        help_text='Indicates whether a buyer is required to confirm that they'
                  ' are over 18. Applies to wine listings (e.g. Home & living'
                  ' > Wine > Red > Pinot noir).'
    )
    payment_amount = models.FloatField(
        null=True,
        help_text='The total amount of this payment'
    )
    payment_interval = models.TextField(
        null=True,
        help_text='Indicates the payment interval, eg. Fortnightly'
    )
    payment_method_fee = models.FloatField(
        null=True,
        help_text='The fee amount paid as part of this payment'
    )
    payment_options = models.TextField(
        null=True,
        help_text='A comma-separated list of the available payment options '
                  'e.g. “NZ Bank Deposit, Cash, Pay Now”.'
    )
    pending_offer = models.ForeignKey(
        'FixedPriceOfferDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_pending_offer',
        help_text='Contains details of a fixed price offer that is pending '
                  'for this auction. Only available if you are the seller or '
                  'a recipient of the offer.'
    )
    percentage_off = models.IntegerField(
        null=True,
        help_text='The percentage that a product has been discounted. This '
                  'has been rounded for display purposes. This field will '
                  'only be populated if IsClearance is true .'
    )
    photo_id = models.IntegerField(
        null=True,
        help_text='The ID of the primary photo for the listing (if the '
                  'listing has a photo).'
    )
    photos = models.ManyToManyField(
        'Photo',
        related_name='listed_item_detail_reverse_photos',
        help_text='A collection of photos for the listing.'
    )
    positive_review_count = models.IntegerField(
        null=True,
        help_text='The number of user-submitted reviews which are positive '
                  '(i.e. the user selected the thumbs up graphic when '
                  'submitting a review). Currently only applies to services '
                  'listings.'
    )
    price_display = models.TextField(
        null=True,
        help_text='The price, in a format suitable for displaying to the '
                  'user. Some categories may have special pricing rules, e.g.'
                  ' properties may have “Price by negotiation”.'
    )
    quantity = models.IntegerField(
        null=True,
        help_text='The total quantity available of the item. Only applicable '
                  'for Buy Now Only listings. When retrieving won items this '
                  'value represents the number sold, not the total quantity. '
                  'When retrieving sold items, this value is not present (use'
                  ' QuantitySold instead). When retrieving listing details, '
                  'this value is only present if you are the seller.'
    )
    questions = models.ForeignKey(
        'Questions',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_questions',
        help_text='A list of questions and answers for the listing.'
    )
    refund_collection = models.ManyToManyField(
        'RefundDetails',
        related_name='listed_item_detail_reverse_refund_collection',
        help_text='A collection of refunds that have been made against this '
                  'payment'
    )
    region = models.TextField(
        null=True,
        help_text='The name of the region where this item is located.'
    )
    region_id = models.IntegerField(
        null=True,
        help_text='The ID of the region where this item is located. In the '
                  'general search, listing details and watchlist APIs this is'
                  ' the ID of the seller’s region (using the two-tier '
                  'region/suburb system), which means it might be '
                  'inconsistent with the region name. In the property search '
                  'API this is the ID of the property region, using the '
                  'three-tier region/district/suburb system. This field '
                  'cannot cope with the two main geographical classification '
                  'systems. Except for the property search API, it should not'
                  ' be used.'
    )
    relisted_item_id = models.IntegerField(
        null=True,
        help_text='The ID of the new listing if this listing was relisted.'
    )
    remaining_gallery_plus_relists = models.IntegerField(
        null=True,
        help_text='The number of times the item can be relisted and get the '
                  'gallery promotion for free. This value is only present if '
                  'you are the seller and the listing had the gallery '
                  'promotion applied due to the gallery plus promotion. Note '
                  'that for this field, a value of zero is not the same as if'
                  ' the field is missing (a value of zero means gallery plus '
                  'is in effect whereas if the field is missing it means that'
                  ' you are not the seller or gallery plus is not in effect).'
    )
    reserve_price = models.FloatField(
        null=True,
        help_text='The reserve price for the auction. This is available in '
                  'the sold/unsold items APIs and, if you are the seller, the'
                  ' listing details API.'
    )
    reserve_state = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Met'),
            (2, 'NotMet'),
            (3, 'NotApplicable'),
        ),
        null=True,
        help_text='The flag to display on an item.'
    )
    sku = models.TextField(
        null=True,
        help_text='SKU or Stock Keeping Unit. Used to uniquely identify an '
                  'auction’s product line.'
    )
    sales = models.ManyToManyField(
        'Sale',
        related_name='listed_item_detail_reverse_sales',
        help_text='Contains sales information for the listing. A “sale” in '
                  'this context can via Buy Now, a fixed price offer or a '
                  'winning bid. If you are the seller of this listing, this '
                  'field contains information on all sales. If you are the '
                  'buyer, then it contains information about your purchases '
                  'only.'
    )
    send_payment_instructions = models.NullBooleanField(
        null=True,
        help_text='Indicates whether payment instructions are automatically '
                  'sent to buyers. This value is only present if you are the '
                  'seller.'
    )
    shipping_options = models.ManyToManyField(
        'ShippingOption',
        related_name='listed_item_detail_reverse_shipping_options',
        help_text='A list of shipping options.'
    )
    sponsor_links = models.ManyToManyField(
        'SponsorLink',
        related_name='listed_item_detail_reverse_sponsor_links',
        help_text='A collection of sponsored links for the listing.'
    )
    start_date = models.DateTimeField(
        null=True,
        help_text='The date the listing was created.'
    )
    start_price = models.FloatField(
        null=True,
        help_text='The start price.'
    )
    store = models.ForeignKey(
        'Store',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_store',
        help_text='The store details, if the seller has a Trade Me store.'
    )
    subtitle = models.TextField(
        null=True,
        help_text='The subtitle, if present.'
    )
    suburb = models.TextField(
        null=True,
        help_text='The name of the suburb where this item is located.'
    )
    suburb_id = models.IntegerField(
        null=True,
        help_text='The ID of the suburb where this item is located. Only '
                  'populated by the property search API, which means it uses '
                  'the three-tier region/district/suburb system.'
    )
    super_feature_end_date = models.DateTimeField(
        null=True,
        help_text='End date of a super feature for a listing.'
    )
    supports_questions_and_answers = models.NullBooleanField(
        null=True,
        help_text='Indicates if questions and answers can be shown on the '
                  'listing'
    )
    title = models.TextField(
        null=True,
        help_text='The listing title.'
    )
    total_review_count = models.IntegerField(
        null=True,
        help_text='The total number of user-submitted reviews. Currently only'
                  ' applies to services listings.'
    )
    unanswered_question_count = models.IntegerField(
        null=True,
        help_text='The number of unanswered questions for this listing.'
    )
    variant_definition = models.ForeignKey(
        'VariantDefinition',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='listed_item_detail_reverse_variant_definition',
        help_text='The variants.'
    )
    view_count = models.IntegerField(
        null=True,
        help_text='The number of times the listing has been viewed.'
    )
    was_price = models.FloatField(
        null=True,
        help_text='The usual price that a product is sold at, or the price '
                  'before it was marked down. This is always more than the '
                  'Buy Now price. This field will only be populated if '
                  'IsClearance is true .'
    )
    withdrawn_by_seller = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing was withdrawn by the seller.'
    )

    class Meta:

        unique_together = (
            (
                'listing_id',
            ),
        )


class Member(RawModel):

    swagger_types = types.MappingProxyType({
        'date_address_verified': 'datetime',
        'date_joined': 'datetime',
        'email': 'str',
        'feedback_count': 'int',
        'import_charges_may_apply': 'bool',
        'is_address_verified': 'bool',
        'is_authenticated': 'bool',
        'is_dealer': 'bool',
        'is_in_trade': 'bool',
        'is_top_seller': 'bool',
        'member_id': 'int',
        'nickname': 'str',
        'photo': 'str',
        'region': 'str',
        'suburb': 'str',
        'unique_negative': 'int',
        'unique_positive': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('date_address_verified', 'DateAddressVerified'),
        ('date_joined', 'DateJoined'),
        ('email', 'Email'),
        ('feedback_count', 'FeedbackCount'),
        ('import_charges_may_apply', 'ImportChargesMayApply'),
        ('is_address_verified', 'IsAddressVerified'),
        ('is_authenticated', 'IsAuthenticated'),
        ('is_dealer', 'IsDealer'),
        ('is_in_trade', 'IsInTrade'),
        ('is_top_seller', 'IsTopSeller'),
        ('member_id', 'MemberId'),
        ('nickname', 'Nickname'),
        ('photo', 'Photo'),
        ('region', 'Region'),
        ('suburb', 'Suburb'),
        ('unique_negative', 'UniqueNegative'),
        ('unique_positive', 'UniquePositive'),
    ]))

    date_address_verified = models.DateTimeField(
        null=True,
        help_text='The date the member was address verified.'
    )
    date_joined = models.DateTimeField(
        null=True,
        help_text='The date the member joined.'
    )
    email = models.TextField(
        null=True,
        help_text='The member’s email address.'
    )
    feedback_count = models.IntegerField(
        null=True,
        help_text='The member’s total feedback (UniquePositive minus '
                  'UniqueNegative).'
    )
    import_charges_may_apply = models.NullBooleanField(
        null=True,
        help_text='Indicates that the trader is an international seller, and '
                  'therefore customs import charges may apply.'
    )
    is_address_verified = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member has been address verified.'
    )
    is_authenticated = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member is authenticated.'
    )
    is_dealer = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member is a car dealer.'
    )
    is_in_trade = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member is a professional trader.'
    )
    is_top_seller = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member is currently a Top Seller'
    )
    member_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the member. This may be 0 , if we determine it '
                  'is necessary to protect the member’s privacy.'
    )
    nickname = models.TextField(
        null=True,
        help_text='The nickname of the member. Some characters may be '
                  'changed, if we determine it is necessary to protect the '
                  'member’s privacy.'
    )
    photo = models.TextField(
        null=True,
        help_text='The profile photo URL of the member'
    )
    region = models.TextField(
        null=True,
        help_text='The name of the member’s region.'
    )
    suburb = models.TextField(
        null=True,
        help_text='The name of the member’s suburb.'
    )
    unique_negative = models.IntegerField(
        null=True,
        help_text='The number of distinct members who have placed negative '
                  'feedback against this member.'
    )
    unique_positive = models.IntegerField(
        null=True,
        help_text='The number of distinct members who have placed positive '
                  'feedback against this member.'
    )

    class Meta:

        unique_together = (
            (
                'member_id',
            ),
        )


class MemberRequestInformation(RawModel):

    swagger_types = types.MappingProxyType({
        'request_offer_status': 'int',
        'request_relist_status': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('request_offer_status', 'RequestOfferStatus'),
        ('request_relist_status', 'RequestRelistStatus'),
    ]))

    request_offer_status = models.IntegerField(
        choices=(
            (0, 'MemberCanRequest'),
            (1, 'SoldAlready'),
            (2, 'MemberIsBlacklisted'),
            (3, 'RequestAlreadyMade'),
            (4, 'OfferAlreadyMade'),
            (5, 'RelistedAlready'),
            (6, 'MemberIsNotAValidOfferee'),
        ),
        null=True,
        help_text='Indicates whether the member can request an offer and the '
                  'status of any request.'
    )
    request_relist_status = models.IntegerField(
        choices=(
            (0, 'MemberCanRequest'),
            (1, 'SoldAlready'),
            (2, 'MemberIsBlacklisted'),
            (3, 'RequestAlreadyMade'),
            (4, 'OfferAlreadyMade'),
            (5, 'RelistedAlready'),
            (6, 'MemberIsNotAValidOfferee'),
        ),
        null=True,
        help_text='Indicates whether the member can request a relist and the '
                  'status of any request.'
    )

    class Meta:

        unique_together = (
            (
                'request_offer_status',
                'request_relist_status',
            ),
        )


class MotorWebBasicReport(RawModel):

    swagger_types = types.MappingProxyType({
        'damaged': 'str',
        'generated_at': 'datetime',
        'money_owing': 'str',
        'partial_report_url': 'str',
        'rego_or_vin': 'str',
        'reported_stolen': 'str',
        'title': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('damaged', 'Damaged'),
        ('generated_at', 'GeneratedAt'),
        ('money_owing', 'MoneyOwing'),
        ('partial_report_url', 'PartialReportUrl'),
        ('rego_or_vin', 'RegoOrVin'),
        ('reported_stolen', 'ReportedStolen'),
        ('title', 'Title'),
    ]))

    damaged = models.TextField(
        null=True,
        help_text='Returns “YES” if the car was reported to be damaged during'
                  ' the import. Returns “NO” if the car was not reported to '
                  'be damaged during the import. Returns “N/A” if value '
                  'cannot be reliably read from the database.'
    )
    generated_at = models.DateTimeField(
        null=True,
        help_text='Returns the time stamp of the date and time when report '
                  'has been generated.'
    )
    money_owing = models.TextField(
        null=True,
        help_text='Returns “YES” if a person or company has registered a '
                  'security against the vehicle indicating they have a '
                  'financial interest in the vehicle Returns “NO” if a person'
                  ' or company has not registered a security against the '
                  'vehicle indicating they have a financial interest in the '
                  'vehicle. Returns “N/A” if value cannot be reliably read '
                  'from the database.'
    )
    partial_report_url = models.TextField(
        null=True,
        help_text='Returns the URL to the partial MotorWebReport'
    )
    rego_or_vin = models.TextField(
        null=True,
        help_text='Returns the registration or VIN number which has been used'
                  ' to purchase the Motor Web Basic Report.'
    )
    reported_stolen = models.TextField(
        null=True,
        help_text='Returns “YES” if the car was reported to be stolen. '
                  'Returns “NO” if the car was not reported to be stolen. '
                  'Returns “N/A” if value cannot be reliably read from the '
                  'database.'
    )
    title = models.TextField(
        null=True,
        help_text='Returns the vehicle title'
    )

    class Meta:

        unique_together = (
            (
                'damaged',
                'generated_at',
                'money_owing',
                'partial_report_url',
                'rego_or_vin',
                'reported_stolen',
                'title',
            ),
        )


class OpenHome(RawModel):

    swagger_types = types.MappingProxyType({
        'end': 'datetime',
        'start': 'datetime',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('end', 'End'),
        ('start', 'Start'),
    ]))

    end = models.DateTimeField(
        null=True,
        help_text='The date and time the open home is no longer open for '
                  'viewing. Must be the same day as Start .'
    )
    start = models.DateTimeField(
        null=True,
        help_text='The date and time the open home is open for viewing. The '
                  'date must be in the future and it must be less than 56 '
                  'days from the current date. Specify dates in the UTC time '
                  'zone.'
    )

    class Meta:

        unique_together = (
            (
                'end',
                'start',
            ),
        )


class Option(RawModel):

    swagger_types = types.MappingProxyType({
        'name': 'str',
        'value': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('name', 'Name'),
        ('value', 'Value'),
    ]))

    name = models.TextField(
        null=True,
        help_text='The name used to identify the group of option values, e.g.'
                  ' “size” or “colour”. This name must match an entry in the '
                  'option set collection.'
    )
    value = models.TextField(
        null=True,
        help_text='The choice that this variant has for the option, e.g. '
                  '“red”, “blue”. This name must match an entry in the option'
                  ' set.'
    )

    class Meta:

        unique_together = (
            (
                'name',
                'value',
            ),
        )


class OptionSet(RawModel):

    swagger_types = types.MappingProxyType({
        'name': 'str',
        'values': 'list[OptionSetValues]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('name', 'Name'),
        ('values', 'Values'),
    ]))

    name = models.TextField(
        null=True,
        help_text='The name used to identify the group of option values, e.g.'
                  ' “size” or “colour”.'
    )
    values = models.ManyToManyField(
        'OptionSetValues',
        related_name='option_set_reverse_values',
        help_text='The choices available for this option set, e.g. “red”, '
                  '“blue”. The sequence in which values are supplied is '
                  'reflected in the sequence of user-interface elements on '
                  'listings.'
    )

    class Meta:

        unique_together = (
            (
                'name',
            ),
        )


class OptionSetValues(RawModel):

    expect_single_value = 'value'
    swagger_types = types.MappingProxyType({
        'value': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('value', 'value'),
    ]))

    value = models.TextField(
        null=True,
    )

    class Meta:

        unique_together = (
            (
                'value',
            ),
        )


class Photo(RawModel):

    swagger_types = types.MappingProxyType({
        'photo_id': 'int',
        'value': 'PhotoUrl',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('photo_id', 'Key'),
        ('photo_id', 'PhotoId'),
        ('value', 'Value'),
    ]))

    photo_id = models.IntegerField(
        primary_key=True,
        help_text=''
    )
    value = models.ForeignKey(
        'PhotoUrl',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='photo_reverse_value',
        help_text=''
    )

    class Meta:

        unique_together = (
            (
                'photo_id',
            ),
        )


class PhotoUrl(RawModel):

    swagger_types = types.MappingProxyType({
        'full_size': 'str',
        'gallery': 'str',
        'large': 'str',
        'list': 'str',
        'medium': 'str',
        'original_height': 'int',
        'original_width': 'int',
        'photo_id': 'int',
        'plus_size': 'str',
        'thumbnail': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('full_size', 'FullSize'),
        ('gallery', 'Gallery'),
        ('large', 'Large'),
        ('list', 'List'),
        ('medium', 'Medium'),
        ('original_height', 'OriginalHeight'),
        ('original_width', 'OriginalWidth'),
        ('photo_id', 'PhotoId'),
        ('plus_size', 'PlusSize'),
        ('thumbnail', 'Thumbnail'),
    ]))

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
    photo_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the photo.'
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

    class Meta:

        unique_together = (
            (
                'photo_id',
            ),
        )


class Question(RawModel):

    swagger_types = types.MappingProxyType({
        'answer': 'str',
        'answer_date': 'datetime',
        'asking_member': 'Member',
        'comment': 'str',
        'comment_date': 'datetime',
        'is_seller_comment': 'bool',
        'listing_id': 'int',
        'listing_question_id': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('answer', 'Answer'),
        ('answer_date', 'AnswerDate'),
        ('asking_member', 'AskingMember'),
        ('comment', 'Comment'),
        ('comment_date', 'CommentDate'),
        ('is_seller_comment', 'IsSellerComment'),
        ('listing_id', 'ListingId'),
        ('listing_question_id', 'ListingQuestionId'),
    ]))

    answer = models.TextField(
        null=True,
        help_text='The answer given to the question by the owner of the '
                  'listing.'
    )
    answer_date = models.DateTimeField(
        null=True,
        help_text='The date the question was answered.'
    )
    asking_member = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='question_reverse_asking_member',
        help_text='The member details for the member asking the question.'
    )
    comment = models.TextField(
        null=True,
        help_text='The text of the question.'
    )
    comment_date = models.DateTimeField(
        null=True,
        help_text='The date and time the question was asked.'
    )
    is_seller_comment = models.NullBooleanField(
        null=True,
        help_text='Indicates whether this is a comment from the seller rather'
                  ' than a question.'
    )
    listing_id = models.IntegerField(
        null=True,
        help_text='The ID of the listing this question belongs to.'
    )
    listing_question_id = models.IntegerField(
        null=True,
        help_text='The question ID.'
    )

    class Meta:

        unique_together = (
            (
                'answer',
                'answer_date',
                'asking_member',
                'comment',
                'comment_date',
                'is_seller_comment',
                'listing_id',
                'listing_question_id',
            ),
        )


class Questions(RawModel):

    swagger_types = types.MappingProxyType({
        'list': 'list[Question]',
        'page': 'int',
        'page_size': 'int',
        'total_count': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('list', 'List'),
        ('page', 'Page'),
        ('page_size', 'PageSize'),
        ('total_count', 'TotalCount'),
    ]))

    list = models.ManyToManyField(
        'Question',
        related_name='questions_reverse_list',
        help_text='A list of the results in the current page.'
    )
    page = models.IntegerField(
        null=True,
        help_text='The index of the current page of results (starts at 1).'
    )
    page_size = models.IntegerField(
        null=True,
        help_text='The number of results in the current page.'
    )
    total_count = models.IntegerField(
        null=True,
        help_text='The total number of results in the collection. Can be '
                  'larger than the number of returned results.'
    )

    class Meta:

        unique_together = (
            (
                'page',
                'page_size',
                'total_count',
            ),
        )


class RefundDetails(RawModel):

    swagger_types = types.MappingProxyType({
        'amount': 'float',
        'destination': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('amount', 'Amount'),
        ('destination', 'Destination'),
    ]))

    amount = models.FloatField(
        null=True,
        help_text='The amount refunded'
    )
    destination = models.TextField(
        null=True,
        help_text='The destination the refund was sent to.'
    )

    class Meta:

        unique_together = (
            (
                'amount',
                'destination',
            ),
        )


class Sale(RawModel):

    swagger_types = types.MappingProxyType({
        'buyer': 'Member',
        'credit_card_last_four_digits': 'str',
        'credit_card_payment_date': 'datetime',
        'credit_card_type': 'str',
        'delivery_address': 'Address',
        'delivery_details_sent': 'bool',
        'has_buyer_placed_feedback': 'bool',
        'has_paid_by_credit_card': 'bool',
        'has_seller_placed_feedback': 'bool',
        'is_payment_pending': 'bool',
        'message_from_buyer': 'str',
        'method': 'int',
        'order_id': 'int',
        'payment_instructions': 'str',
        'price': 'float',
        'purchase_id': 'int',
        'quantity_sold': 'int',
        'reference_number': 'str',
        'selected_shipping': 'str',
        'shipping_price': 'float',
        'shipping_type': 'int',
        'sold_date': 'datetime',
        'status': 'int',
        'status_date': 'datetime',
        'subtotal_price': 'float',
        'total_sale_price': 'float',
        'total_shipping_price': 'float',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('buyer', 'Buyer'),
        ('credit_card_last_four_digits', 'CreditCardLastFourDigits'),
        ('credit_card_payment_date', 'CreditCardPaymentDate'),
        ('credit_card_type', 'CreditCardType'),
        ('delivery_address', 'DeliveryAddress'),
        ('delivery_details_sent', 'DeliveryDetailsSent'),
        ('has_buyer_placed_feedback', 'HasBuyerPlacedFeedback'),
        ('has_paid_by_credit_card', 'HasPaidByCreditCard'),
        ('has_seller_placed_feedback', 'HasSellerPlacedFeedback'),
        ('is_payment_pending', 'IsPaymentPending'),
        ('message_from_buyer', 'MessageFromBuyer'),
        ('method', 'Method'),
        ('order_id', 'OrderId'),
        ('payment_instructions', 'PaymentInstructions'),
        ('price', 'Price'),
        ('purchase_id', 'PurchaseId'),
        ('quantity_sold', 'QuantitySold'),
        ('reference_number', 'ReferenceNumber'),
        ('selected_shipping', 'SelectedShipping'),
        ('shipping_price', 'ShippingPrice'),
        ('shipping_type', 'ShippingType'),
        ('sold_date', 'SoldDate'),
        ('status', 'Status'),
        ('status_date', 'StatusDate'),
        ('subtotal_price', 'SubtotalPrice'),
        ('total_sale_price', 'TotalSalePrice'),
        ('total_shipping_price', 'TotalShippingPrice'),
    ]))

    buyer = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='sale_reverse_buyer',
        help_text='The member who bought the item. Not available if you are '
                  'the buyer.'
    )
    credit_card_last_four_digits = models.TextField(
        null=True,
        help_text='The last four digits of the credit card used to pay for '
                  'the item. Only available if Pay Now was used to make the '
                  'purchase and you are logged in as the buyer.'
    )
    credit_card_payment_date = models.DateTimeField(
        null=True,
        help_text='The date and time a payment was made with a credit card '
                  'using Pay Now. Only valid if HasPaidByCreditCard is true .'
    )
    credit_card_type = models.TextField(
        null=True,
        help_text='The type of credit card that was used to pay for the item '
                  '(“Visa”, “MasterCard”, etc). Only available if Pay Now was'
                  ' used to make the purchase and you are logged in as the '
                  'buyer.'
    )
    delivery_address = models.ForeignKey(
        'Address',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='sale_reverse_delivery_address',
        help_text='The delivery address as indicated by the buyer.'
    )
    delivery_details_sent = models.NullBooleanField(
        null=True,
        help_text='Indicates whether delivery details (i.e. the delivery '
                  'address, phone number and message) have been sent to the '
                  'seller. Because all three elements are optional, this can '
                  'be true even if the DeliveryAddress and MessageFromBuyer '
                  'fields are missing.'
    )
    has_buyer_placed_feedback = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the buyer has placed feedback on the '
                  'seller for this sale.'
    )
    has_paid_by_credit_card = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the buyer has purchased the item using '
                  'Pay Now. For high risk payments, the value will be false '
                  'until the payment has been manually approved by the Trade '
                  'Me customer service team.'
    )
    has_seller_placed_feedback = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the seller has placed feedback on the '
                  'buyer for this sale.'
    )
    is_payment_pending = models.NullBooleanField(
        null=True,
        help_text='Indicates whether a Pay Now payment is currently under '
                  'review by the Trade Me customer service team. If this flag'
                  ' is set, you should not send payment reminder notices to '
                  'the buyer. Note: the Trade Me website uses the label '
                  '“Payment Held” for payments in this state.'
    )
    message_from_buyer = models.TextField(
        null=True,
        help_text='The message from the buyer to the seller, if any.'
    )
    method = models.IntegerField(
        choices=(
            (0, 'Auction'),
            (1, 'BuyNow'),
            (2, 'Offer'),
        ),
        null=True,
        help_text='The method by which the sale was made.'
    )
    order_id = models.IntegerField(
        null=True,
        help_text='If the item was purchased via the shopping cart, then this'
                  ' is an ID that uniquely identifies the shopping cart '
                  'transaction. All of the items that were ordered in the '
                  'same cart transaction will have the same ID.'
    )
    payment_instructions = models.TextField(
        null=True,
        help_text='The payment instructions that the seller has sent to the '
                  'buyer, containing information on how to pay. Will be '
                  'absent if the seller has not enabled payment instructions,'
                  ' or if the seller has not yet sent them to the buyer.'
    )
    price = models.FloatField(
        null=True,
        help_text='The price the item was sold for, excluding shipping. If '
                  'the purchase was for multiple items, this is the price of '
                  'a single item.'
    )
    purchase_id = models.IntegerField(
        null=True,
        help_text='A unique identifier for the sale.'
    )
    quantity_sold = models.IntegerField(
        null=True,
        help_text='The quantity sold.'
    )
    reference_number = models.TextField(
        null=True,
        help_text='The reference number that should be used when making a '
                  'deposit into the seller’s bank account.'
    )
    selected_shipping = models.TextField(
        null=True,
        help_text='A description of the selected shipping method (e.g. '
                  '“Nationwide courier”).'
    )
    shipping_price = models.FloatField(
        null=True,
        help_text='The price of shipping.'
    )
    shipping_type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Undecided'),
            (2, 'Pickup'),
            (3, 'Free'),
            (4, 'Custom'),
            (5, 'TradeMe'),
        ),
        null=True,
        help_text='The type of shipping that was selected.'
    )
    sold_date = models.DateTimeField(
        null=True,
        help_text='The date and time the item was sold.'
    )
    status = models.IntegerField(
        choices=(
            (10, 'EmailSent'),
            (20, 'PaymentReceived'),
            (30, 'GoodsShipped'),
            (40, 'SaleCompleted'),
        ),
        null=True,
        help_text='The status of the sale. This can be set by the seller to '
                  'track the status of an order; it is never set by Trade Me.'
                  ' Only available if you are the seller of the listing.'
    )
    status_date = models.DateTimeField(
        null=True,
        help_text='The date the status was last changed. Only available to '
                  'the seller.'
    )
    subtotal_price = models.FloatField(
        null=True,
        help_text='The price for all items, excluding shipping (i.e. equal to'
                  ' SalePrice * QuantitySold).'
    )
    total_sale_price = models.FloatField(
        null=True,
        help_text='The total price for the entire sale, including shipping. '
                  'If the purchase was for multiple items, all items are '
                  'included in this price.'
    )
    total_shipping_price = models.FloatField(
        null=True,
        help_text='The total price for shipping. If flat shipping is not '
                  'enabled, equal to ShippingPrice * QuantitySold.'
    )

    class Meta:

        unique_together = (
            (
                'buyer',
                'credit_card_last_four_digits',
                'credit_card_payment_date',
                'credit_card_type',
                'delivery_address',
                'delivery_details_sent',
                'has_buyer_placed_feedback',
                'has_paid_by_credit_card',
                'has_seller_placed_feedback',
                'is_payment_pending',
                'message_from_buyer',
                'method',
                'order_id',
                'payment_instructions',
                'price',
                'purchase_id',
                'quantity_sold',
                'reference_number',
                'selected_shipping',
                'shipping_price',
                'shipping_type',
                'sold_date',
                'status',
                'status_date',
                'subtotal_price',
                'total_sale_price',
                'total_shipping_price',
            ),
        )


class ShippingOption(RawModel):

    swagger_types = types.MappingProxyType({
        'method': 'str',
        'price': 'float',
        'shipping_id': 'int',
        'type': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('method', 'Method'),
        ('price', 'Price'),
        ('shipping_id', 'ShippingId'),
        ('type', 'Type'),
    ]))

    method = models.TextField(
        null=True,
        help_text='The name of the delivery method (e.g. “NZ Courier”, “Rural'
                  ' Delivery”). Only applicable if ShippingType is Custom.'
    )
    price = models.FloatField(
        null=True,
        help_text='The price of the delivery option. Only applicable if '
                  'ShippingType is Custom. Rounded up to the nearest 2 '
                  'decimal places.'
    )
    shipping_id = models.IntegerField(
        null=True,
        help_text='The ID of the shipping option (used when bidding or for '
                  'Buy Now). Not required when listing an item.'
    )
    type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Undecided'),
            (2, 'Pickup'),
            (3, 'Free'),
            (4, 'Custom'),
            (5, 'TradeMe'),
        ),
        null=True,
        help_text='The type of delivery.'
    )

    class Meta:

        unique_together = (
            (
                'method',
                'price',
                'shipping_id',
                'type',
            ),
        )


class SimpleMemberProfile(RawModel):

    swagger_types = types.MappingProxyType({
        'biography': 'str',
        'occupation': 'str',
        'photo': 'str',
        'quote': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('biography', 'Biography'),
        ('occupation', 'Occupation'),
        ('photo', 'Photo'),
        ('quote', 'Quote'),
    ]))

    biography = models.TextField(
        null=True,
        help_text='The member’s bio.'
    )
    occupation = models.TextField(
        null=True,
        help_text='The occupation of the member.'
    )
    photo = models.TextField(
        null=True,
        help_text='A URL representing the member’s photo.'
    )
    quote = models.TextField(
        null=True,
        help_text='The member’s favourite quote.'
    )

    class Meta:

        unique_together = (
            (
                'biography',
                'occupation',
                'photo',
                'quote',
            ),
        )


class SponsorLink(RawModel):

    swagger_types = types.MappingProxyType({
        'link': 'str',
        'name': 'str',
        'type': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('link', 'Link'),
        ('name', 'Name'),
        ('type', 'Type'),
    ]))

    link = models.TextField(
        null=True,
        help_text='The url to link to'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the sponsor, westpac, GE, TMI etc'
    )
    type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'BusinessPartner'),
            (2, 'Checklist'),
        ),
        null=True,
        help_text='The type of sponsor link, business partner/checklist'
    )

    class Meta:

        unique_together = (
            (
                'link',
                'name',
                'type',
            ),
        )


class Store(RawModel):

    swagger_types = types.MappingProxyType({
        'banner_image_uri': 'str',
        'large_banner_image': 'LargeBannerImage',
        'location': 'str',
        'logo_image_uri': 'str',
        'name': 'str',
        'phone_number': 'str',
        'promotions': 'list[StorePromotion]',
        'short_description': 'str',
        'store_path': 'str',
        'website': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('banner_image_uri', 'BannerImageUri'),
        ('large_banner_image', 'LargeBannerImage'),
        ('location', 'Location'),
        ('logo_image_uri', 'LogoImageUri'),
        ('name', 'Name'),
        ('phone_number', 'PhoneNumber'),
        ('promotions', 'Promotions'),
        ('short_description', 'ShortDescription'),
        ('store_path', 'StorePath'),
        ('website', 'Website'),
    ]))

    banner_image_uri = models.TextField(
        null=True,
        help_text='The URL of a banner image. Stores extra banner images are '
                  '960×120. Store banner images are 633×75. When requesting '
                  'listing details, only stores extra listings have a banner '
                  'image.'
    )
    large_banner_image = models.ForeignKey(
        'LargeBannerImage',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='store_reverse_large_banner_image',
        help_text='The URL’s of a large banner image for each breakpoint, '
                  'small, medium, large, extra large. When requesting listing'
                  ' details, only stores extra listings have a large banner '
                  'image.'
    )
    location = models.TextField(
        null=True,
        help_text='The location for this store'
    )
    logo_image_uri = models.TextField(
        null=True,
        help_text='The URL of a small logo image (180×52).'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the store.'
    )
    phone_number = models.TextField(
        null=True,
        help_text='The phone number for this store'
    )
    promotions = models.ManyToManyField(
        'StorePromotion',
        related_name='store_reverse_promotions',
        help_text='A collection of promotional images. Only applies to stores'
                  ' extra.'
    )
    short_description = models.TextField(
        null=True,
        help_text='A short description of what the store sells. Only returned'
                  ' when browsing the stores list.'
    )
    store_path = models.TextField(
        null=True,
        help_text='A url friendly path for the store, that is unique.'
    )
    website = models.TextField(
        null=True,
        help_text='The website for this store'
    )

    class Meta:

        unique_together = (
            (
                'banner_image_uri',
                'large_banner_image',
                'location',
                'logo_image_uri',
                'name',
                'phone_number',
                'short_description',
                'store_path',
                'website',
            ),
        )


class StorePromotion(RawModel):

    swagger_types = types.MappingProxyType({
        'image_uri': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('image_uri', 'ImageUri'),
    ]))

    image_uri = models.TextField(
        null=True,
        help_text='The URL of the promotional image 760×240.'
    )

    class Meta:

        unique_together = (
            (
                'image_uri',
            ),
        )


class Variant(RawModel):

    swagger_types = types.MappingProxyType({
        'attributes': 'list[Attribute]',
        'is_clearance': 'bool',
        'listing_id': 'int',
        'options': 'list[Option]',
        'photos': 'list[Photo]',
        'price': 'float',
        'quantity': 'int',
        'sku': 'str',
        'was_price': 'float',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('attributes', 'Attributes'),
        ('is_clearance', 'IsClearance'),
        ('listing_id', 'ListingId'),
        ('options', 'Options'),
        ('photos', 'Photos'),
        ('price', 'Price'),
        ('quantity', 'Quantity'),
        ('sku', 'SKU'),
        ('was_price', 'WasPrice'),
    ]))

    attributes = models.ManyToManyField(
        'Attribute',
        related_name='variant_reverse_attributes',
        help_text='A collection of dynamic attrbutes that relate to this '
                  'variant specifically e.g. GTIN or MPC'
    )
    is_clearance = models.NullBooleanField(
        null=True,
        help_text='This indicates that the listing is a clearance item. '
                  'Clearance listings include listings with was/now pricing '
                  'and general clearance stock.'
    )
    listing_id = models.IntegerField(
        null=True,
        help_text='The identifier of the listing that this variant '
                  'represents.'
    )
    options = models.ManyToManyField(
        'Option',
        related_name='variant_reverse_options',
        help_text='The combination of variant options that this variant '
                  'represents.'
    )
    photos = models.ManyToManyField(
        'Photo',
        related_name='variant_reverse_photos',
        help_text='A collection of photo URLs for the listing. Ignored when '
                  'creating or editing a listing.'
    )
    price = models.FloatField(
        null=True,
        help_text='The Buy Now price of the variant. Must be a minimum of '
                  '50c.'
    )
    quantity = models.IntegerField(
        null=True,
        help_text='This is the quantity of items that are available for sale.'
                  ' Can be between 1 and 1000. Note that when editing, the '
                  'value must be less than or equal to 1000 – (quantity '
                  'sold). The quantity sold for a listing can be calculated '
                  'by adding up all the QuantitySold values from the listing '
                  'details response.'
    )
    sku = models.TextField(
        null=True,
        help_text='SKU or Stock Keeping Unit. Used to uniquely identify an '
                  'auction’s product line. Maximum of 50 characters.'
    )
    was_price = models.FloatField(
        null=True,
        help_text='The Was price of the variant. Must be a minimum of 50c.'
    )

    class Meta:

        unique_together = (
            (
                'is_clearance',
                'listing_id',
                'price',
                'quantity',
                'sku',
                'was_price',
            ),
        )


class VariantDefinition(RawModel):

    swagger_types = types.MappingProxyType({
        'option_sets': 'list[OptionSet]',
        'variants': 'list[Variant]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('option_sets', 'OptionSets'),
        ('variants', 'Variants'),
    ]))

    option_sets = models.ManyToManyField(
        'OptionSet',
        related_name='variant_definition_reverse_option_sets',
        help_text='A collection of variant options.'
    )
    variants = models.ManyToManyField(
        'Variant',
        related_name='variant_definition_reverse_variants',
        help_text='A collection of variants.'
    )

    class Meta:

        pass


class ViewingTime(RawModel):

    swagger_types = types.MappingProxyType({
        'viewing_id': 'int',
        'viewing_time': 'datetime',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('viewing_id', 'ViewingId'),
        ('viewing_time', 'ViewingTime'),
    ]))

    viewing_id = models.IntegerField()
    viewing_time = models.DateTimeField()

    class Meta:

        unique_together = (
            'viewing_id',
            'viewing_time',
        )


class ViewingTimes(RawModel):

    swagger_types = types.MappingProxyType({
        'avaliable_viewing_times': 'list[ViewingTime]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('avaliable_viewing_times', 'AvailableViewingTimes'),
    ]))

    avaliable_viewing_times = models.ManyToManyField(
        'ViewingTime',
    )

    class Meta:

        pass


__all__ = (
    'Address',
    'Agency',
    'Agent',
    'Attribute',
    'AttributeOption',
    'AttributeRange',
    'Bid',
    'BidCollection',
    'Branding',
    'BroadbandTechnology',
    'Charity',
    'ContactDetails',
    'CurrentShippingPromotion',
    'Dealer',
    'DealerShowroom',
    'DealershipPhoneNumbers',
    'Dealership',
    'DealershipListingCounts',
    'EmbeddedContent',
    'FixedPriceOfferDetails',
    'FixedPriceOfferRecipient',
    'GeographicLocation',
    'LargeBannerImage',
    'ListedItemDetail',
    'Member',
    'MemberRequestInformation',
    'MotorWebBasicReport',
    'OpenHome',
    'Option',
    'OptionSetValues',
    'OptionSet',
    'Photo',
    'PhotoUrl',
    'Question',
    'Questions',
    'RefundDetails',
    'Sale',
    'ShippingOption',
    'SimpleMemberProfile',
    'SponsorLink',
    'Store',
    'StorePromotion',
    'Variant',
    'VariantDefinition',
    'ViewingTime',
    'ViewingTimes'
)
