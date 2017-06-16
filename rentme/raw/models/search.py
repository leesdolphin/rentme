import types

from django.db import models
import multidict

from .base import RawModel


class Flatmate(RawModel):

    swagger_types = types.MappingProxyType({
        'address': 'str',
        'adjacent_suburb_ids': 'list[FlatmateAdjacentSuburbIds]',
        'adjacent_suburb_names': 'list[FlatmateAdjacentSuburbNames]',
        'agency': 'Agency',
        'agency_reference': 'str',
        'amenities': 'str',
        'area': 'int',
        'area_range_max': 'int',
        'as_at': 'datetime',
        'available_from': 'str',
        'bathrooms': 'int',
        'bedrooms': 'int',
        'best_contact_time': 'str',
        'bid_count': 'int',
        'branding': 'Branding',
        'buy_now_price': 'float',
        'category': 'str',
        'category_path': 'str',
        'current_flatmates': 'str',
        'district': 'str',
        'district_id': 'int',
        'end_date': 'datetime',
        'flatmates': 'int',
        'geographic_location': 'GeographicLocation',
        'has_buy_now': 'bool',
        'has_embedded_video': 'bool',
        'has_free_shipping': 'bool',
        'has_gallery': 'bool',
        'has_home_page_feature': 'bool',
        'has_pay_now': 'bool',
        'has_reserve': 'bool',
        'ideal_tenant': 'str',
        'is_bold': 'bool',
        'is_boosted': 'bool',
        'is_buy_now_only': 'bool',
        'is_classified': 'bool',
        'is_clearance': 'bool',
        'is_featured': 'bool',
        'is_highlighted': 'bool',
        'is_new': 'bool',
        'is_on_watch_list': 'bool',
        'is_reserve_met': 'bool',
        'is_super_featured': 'bool',
        'land_area': 'int',
        'listing_group': 'str',
        'listing_id': 'int',
        'max_bid_amount': 'float',
        'max_tenants': 'int',
        'note_date': 'datetime',
        'open_homes': 'list[OpenHome]',
        'parking': 'str',
        'percentage_off': 'int',
        'pets_okay': 'int',
        'photo_urls': 'list[FlatmatePhotoUrls]',
        'picture_href': 'str',
        'positive_review_count': 'int',
        'price_display': 'str',
        'promotion_id': 'int',
        'property_id': 'str',
        'property_type': 'str',
        'rateable_value': 'int',
        'region': 'str',
        'region_id': 'int',
        'remaining_gallery_plus_relists': 'int',
        'rent_per_week': 'float',
        'reserve_state': 'int',
        'short_description': 'str',
        'smokers_okay': 'int',
        'start_date': 'datetime',
        'start_price': 'float',
        'subtitle': 'str',
        'suburb': 'str',
        'suburb_id': 'int',
        'title': 'str',
        'total_review_count': 'int',
        'variant_definition_summary': 'VariantDefinitionSummary',
        'viewing_instructions': 'str',
        'was_price': 'float',
        'whiteware': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('address', 'Address'),
        ('adjacent_suburb_ids', 'AdjacentSuburbIds'),
        ('adjacent_suburb_names', 'AdjacentSuburbNames'),
        ('agency', 'Agency'),
        ('agency_reference', 'AgencyReference'),
        ('amenities', 'Amenities'),
        ('area', 'Area'),
        ('area_range_max', 'AreaRangeMax'),
        ('as_at', 'AsAt'),
        ('available_from', 'AvailableFrom'),
        ('bathrooms', 'Bathrooms'),
        ('bedrooms', 'Bedrooms'),
        ('best_contact_time', 'BestContactTime'),
        ('bid_count', 'BidCount'),
        ('branding', 'Branding'),
        ('buy_now_price', 'BuyNowPrice'),
        ('category', 'Category'),
        ('category_path', 'CategoryPath'),
        ('current_flatmates', 'CurrentFlatmates'),
        ('district', 'District'),
        ('district_id', 'DistrictId'),
        ('end_date', 'EndDate'),
        ('flatmates', 'Flatmates'),
        ('geographic_location', 'GeographicLocation'),
        ('has_buy_now', 'HasBuyNow'),
        ('has_embedded_video', 'HasEmbeddedVideo'),
        ('has_free_shipping', 'HasFreeShipping'),
        ('has_gallery', 'HasGallery'),
        ('has_home_page_feature', 'HasHomePageFeature'),
        ('has_pay_now', 'HasPayNow'),
        ('has_reserve', 'HasReserve'),
        ('ideal_tenant', 'IdealTenant'),
        ('is_bold', 'IsBold'),
        ('is_boosted', 'IsBoosted'),
        ('is_buy_now_only', 'IsBuyNowOnly'),
        ('is_classified', 'IsClassified'),
        ('is_clearance', 'IsClearance'),
        ('is_featured', 'IsFeatured'),
        ('is_highlighted', 'IsHighlighted'),
        ('is_new', 'IsNew'),
        ('is_on_watch_list', 'IsOnWatchList'),
        ('is_reserve_met', 'IsReserveMet'),
        ('is_super_featured', 'IsSuperFeatured'),
        ('land_area', 'LandArea'),
        ('listing_group', 'ListingGroup'),
        ('listing_id', 'ListingId'),
        ('max_bid_amount', 'MaxBidAmount'),
        ('max_tenants', 'MaxTenants'),
        ('note_date', 'NoteDate'),
        ('open_homes', 'OpenHomes'),
        ('parking', 'Parking'),
        ('percentage_off', 'PercentageOff'),
        ('pets_okay', 'PetsOkay'),
        ('photo_urls', 'PhotoUrls'),
        ('picture_href', 'PictureHref'),
        ('positive_review_count', 'PositiveReviewCount'),
        ('price_display', 'PriceDisplay'),
        ('promotion_id', 'PromotionId'),
        ('property_id', 'PropertyId'),
        ('property_type', 'PropertyType'),
        ('rateable_value', 'RateableValue'),
        ('region', 'Region'),
        ('region_id', 'RegionId'),
        ('remaining_gallery_plus_relists', 'RemainingGalleryPlusRelists'),
        ('rent_per_week', 'RentPerWeek'),
        ('reserve_state', 'ReserveState'),
        ('short_description', 'ShortDescription'),
        ('smokers_okay', 'SmokersOkay'),
        ('start_date', 'StartDate'),
        ('start_price', 'StartPrice'),
        ('subtitle', 'Subtitle'),
        ('suburb', 'Suburb'),
        ('suburb_id', 'SuburbId'),
        ('title', 'Title'),
        ('total_review_count', 'TotalReviewCount'),
        ('variant_definition_summary', 'VariantDefinitionSummary'),
        ('viewing_instructions', 'ViewingInstructions'),
        ('was_price', 'WasPrice'),
        ('whiteware', 'Whiteware'),
    ]))

    address = models.TextField(
        null=True,
        help_text='The address to display.'
    )
    adjacent_suburb_ids = models.ManyToManyField(
        'FlatmateAdjacentSuburbIds',
        related_name='flatmate_reverse_adjacent_suburb_ids',
        help_text='The IDs of any adjacent suburbs.'
    )
    adjacent_suburb_names = models.ManyToManyField(
        'FlatmateAdjacentSuburbNames',
        related_name='flatmate_reverse_adjacent_suburb_names',
        help_text='The names of any adjacent suburbs.'
    )
    agency = models.ForeignKey(
        'Agency',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='flatmate_reverse_agency',
        help_text='Details of the agency this property was listed by.'
    )
    agency_reference = models.TextField(
        null=True,
        help_text='The reference to the agency.'
    )
    amenities = models.TextField(
        null=True,
        help_text='A list of the amenities in the area.'
    )
    area = models.IntegerField(
        null=True,
        help_text='The area of the house, in square metres.'
    )
    area_range_max = models.IntegerField(
        null=True,
        help_text='The maximum area of the house, in square metres.'
    )
    as_at = models.DateTimeField(
        null=True,
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
    bid_count = models.IntegerField(
        null=True,
        help_text='The number of bids on the item.'
    )
    branding = models.ForeignKey(
        'Branding',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='flatmate_reverse_branding',
        help_text='A list of branding images associated with this listing.'
    )
    buy_now_price = models.FloatField(
        null=True,
        help_text='The Buy Now price.'
    )
    category = models.TextField(
        null=True,
        help_text='The listing category.'
    )
    category_path = models.TextField(
        null=True,
        help_text='The category path.'
    )
    current_flatmates = models.TextField(
        null=True,
        help_text='A description of the current flatmates.'
    )
    district = models.TextField(
        null=True,
        help_text='The name of the district the property is located in.'
    )
    district_id = models.IntegerField(
        null=True,
        help_text='The ID of the district where this property is located.'
    )
    end_date = models.DateTimeField(
        null=True,
        help_text='The date the listing will end.'
    )
    flatmates = models.IntegerField(
        null=True,
        help_text='The number of current flatmates.'
    )
    geographic_location = models.ForeignKey(
        'GeographicLocation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='flatmate_reverse_geographic_location',
        help_text='The geographic location (latitude and longitude) of a '
                  'property.'
    )
    has_buy_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Buy Now.'
    )
    has_embedded_video = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing has an embedded video'
    )
    has_free_shipping = models.NullBooleanField(
        null=True,
        help_text='Indicates if the listing offers free shipping as an option'
    )
    has_gallery = models.NullBooleanField(
        null=True,
        help_text='Is this a gallery listing?'
    )
    has_home_page_feature = models.NullBooleanField(
        null=True,
        help_text='Is this a homepage feature listing?'
    )
    has_pay_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Pay Now.'
    )
    has_reserve = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has a reserve.'
    )
    ideal_tenant = models.TextField(
        null=True,
        help_text='A description of the ideal tenant (are they tidy, a '
                  'professional couple, etc).'
    )
    is_bold = models.NullBooleanField(
        null=True,
        help_text='Is this a bold listing?'
    )
    is_boosted = models.NullBooleanField(
        null=True,
        help_text='If the listing has been boosted or not'
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
    is_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a featured listing?'
    )
    is_highlighted = models.NullBooleanField(
        null=True,
        help_text='Is this a highlighted listing?'
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
    is_reserve_met = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item’s reserve has been met.'
    )
    is_super_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a super featured listing?'
    )
    land_area = models.IntegerField(
        null=True,
        help_text='The area of the land, in square metres.'
    )
    listing_group = models.TextField(
        null=True,
        help_text='The listing group.'
    )
    listing_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the listing.'
    )
    max_bid_amount = models.FloatField(
        null=True,
        help_text='The current leading bid amount.'
    )
    max_tenants = models.IntegerField(
        null=True,
        help_text='The maximum number of tenents.'
    )
    note_date = models.DateTimeField(
        null=True,
        help_text='The date of the note on an item.'
    )
    open_homes = models.ManyToManyField(
        'OpenHome',
        related_name='flatmate_reverse_open_homes',
        help_text='A collection of open home times for this listing. Only '
                  'applies to open home listings.'
    )
    parking = models.TextField(
        null=True,
        help_text='Information on the availability of parking.'
    )
    percentage_off = models.IntegerField(
        null=True,
        help_text='The percentage that a product has been discounted. This '
                  'has been rounded for display purposes. This field will '
                  'only be populated if IsClearance is true .'
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
    photo_urls = models.ManyToManyField(
        'FlatmatePhotoUrls',
        related_name='flatmate_reverse_photo_urls',
        help_text='A collection of photo urls for the listing'
    )
    picture_href = models.TextField(
        null=True,
        help_text='The URL of the primary photo for the listing (if the '
                  'listing has a photo). By default you’ll get a thumbnail-'
                  'sized photo, but you can control the size of the photo '
                  'using the photo_size parameter.'
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
    promotion_id = models.IntegerField(
        null=True,
        help_text='The ID of the promotion applied to this listing.'
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
    rateable_value = models.IntegerField(
        null=True,
        help_text='The rateable value of the property.'
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
    rent_per_week = models.FloatField(
        null=True,
        help_text='The rent payable per week, in NZD.'
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
    short_description = models.TextField(
        null=True,
        help_text='Short description of a listing. This is Jobs and Services '
                  'specfic.'
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
    start_price = models.FloatField(
        null=True,
        help_text='The start price.'
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
    title = models.TextField(
        null=True,
        help_text='The listing title.'
    )
    total_review_count = models.IntegerField(
        null=True,
        help_text='The total number of user-submitted reviews. Currently only'
                  ' applies to services listings.'
    )
    variant_definition_summary = models.ForeignKey(
        'VariantDefinitionSummary',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='flatmate_reverse_variant_definition_summary',
        help_text='A summary of the variant information.'
    )
    viewing_instructions = models.TextField(
        null=True,
        help_text='Instructions on how to view the property.'
    )
    was_price = models.FloatField(
        null=True,
        help_text='The usual price that a product is sold at, or the price '
                  'before it was marked down. This is always more than the '
                  'Buy Now price. This field will only be populated if '
                  'IsClearance is true .'
    )
    whiteware = models.TextField(
        null=True,
        help_text='A description of what is included in the rent (if '
                  'furnished).'
    )

    class Meta:

        unique_together = (
            (
                'listing_id',
            ),
        )


class FlatmateAdjacentSuburbIds(RawModel):

    expect_single_value = 'value'
    swagger_types = types.MappingProxyType({
        'value': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('value', 'value'),
    ]))

    value = models.IntegerField(
        null=True,
    )

    class Meta:

        unique_together = (
            (
                'value',
            ),
        )


class FlatmateAdjacentSuburbNames(RawModel):

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


class FlatmatePhotoUrls(RawModel):

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


class Flatmates(RawModel):

    swagger_types = types.MappingProxyType({
        'did_you_mean': 'str',
        'favourite_id': 'int',
        'favourite_type': 'int',
        'found_categories': 'list[FoundCategory]',
        'list': 'list[Flatmate]',
        'member_profile': 'MemberProfile',
        'page': 'int',
        'page_size': 'int',
        'parameters': 'list[SearchParameter]',
        'sort_orders': 'list[AttributeOption]',
        'super_features': 'list[Flatmate]',
        'total_count': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('did_you_mean', 'DidYouMean'),
        ('favourite_id', 'FavouriteId'),
        ('favourite_type', 'FavouriteType'),
        ('found_categories', 'FoundCategories'),
        ('list', 'List'),
        ('member_profile', 'MemberProfile'),
        ('page', 'Page'),
        ('page_size', 'PageSize'),
        ('parameters', 'Parameters'),
        ('sort_orders', 'SortOrders'),
        ('super_features', 'SuperFeatures'),
        ('total_count', 'TotalCount'),
    ]))

    did_you_mean = models.TextField(
        null=True,
        help_text='The suggestion string, if the search produced no results '
                  'and there is a popular search term that is lexigraphically'
                  ' close to the search string.'
    )
    favourite_id = models.IntegerField(
        null=True,
        help_text='The ID of a favourite search that corresponds to the '
                  'current search, if the call is authenticated and the '
                  'authenticated member has a favourite search that matches.'
    )
    favourite_type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Category'),
            (3, 'Search'),
            (4, 'AttributeSearch'),
            (6, 'Seller'),
        ),
        null=True,
        help_text='The type of favourite (e.g. “Category”, “Search”, '
                  '“Seller”) that the FavouriteId property refers to. Only '
                  'applicable for searches that match one of the '
                  'authenticated user’s favourites.'
    )
    found_categories = models.ManyToManyField(
        'FoundCategory',
        related_name='flatmates_reverse_found_categories',
        help_text='A collection of suggested categories and the number of '
                  'search results in each category.'
    )
    list = models.ManyToManyField(
        'Flatmate',
        related_name='flatmates_reverse_list',
        help_text='A list of the results in the current page.'
    )
    member_profile = models.ForeignKey(
        'MemberProfile',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='flatmates_reverse_member_profile',
        help_text='Details of the member that is being filtered on. Not '
                  'returned unless member_listing is non-zero and '
                  'return_metadata is true.'
    )
    page = models.IntegerField(
        null=True,
        help_text='The index of the current page of results (starts at 1).'
    )
    page_size = models.IntegerField(
        null=True,
        help_text='The number of results in the current page.'
    )
    parameters = models.ManyToManyField(
        'SearchParameter',
        related_name='flatmates_reverse_parameters',
        help_text='A list of search parameters which are applicable to the '
                  'searched category. Not returned unless return_metadata is '
                  'true.'
    )
    sort_orders = models.ManyToManyField(
        'AttributeOption',
        related_name='flatmates_reverse_sort_orders',
        help_text='A list of sort orders which are applicable to the searched'
                  ' category. Not returned unless return_metadata is true.'
    )
    super_features = models.ManyToManyField(
        'Flatmate',
        related_name='flatmates_reverse_super_features',
        help_text='A randomised collection of super features matching the '
                  'current search'
    )
    total_count = models.IntegerField(
        null=True,
        help_text='The total number of results in the collection. Can be '
                  'larger than the number of returned results.'
    )

    class Meta:

        unique_together = (
            (
                'did_you_mean',
                'favourite_id',
                'favourite_type',
                'member_profile',
                'page',
                'page_size',
                'total_count',
            ),
        )


class FoundCategory(RawModel):

    swagger_types = types.MappingProxyType({
        'category': 'str',
        'category_id': 'int',
        'count': 'int',
        'is_restricted': 'bool',
        'name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('category', 'Category'),
        ('category_id', 'CategoryId'),
        ('count', 'Count'),
        ('is_restricted', 'IsRestricted'),
        ('name', 'Name'),
    ]))

    category = models.TextField(
        null=True,
        help_text='The category identifier string in the form nnnn- (e.g. '
                  '“0344-3357-6420-“).'
    )
    category_id = models.IntegerField(
        null=True,
        help_text='The category id (e.g. 6420).'
    )
    count = models.IntegerField(
        null=True,
        help_text='The number of results that were found in this category.'
    )
    is_restricted = models.NullBooleanField(
        null=True,
        help_text='True if the category is restricted. All R18 categories are'
                  ' restricted by default.'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the category (e.g. “Blackberry”).'
    )

    class Meta:

        unique_together = (
            (
                'category',
                'category_id',
                'count',
                'is_restricted',
                'name',
            ),
        )


class MemberProfile(RawModel):

    swagger_types = types.MappingProxyType({
        'biography': 'str',
        'date_removed': 'datetime',
        'favourite_id': 'int',
        'first_name': 'str',
        'is_enabled': 'bool',
        'member': 'Member',
        'occupation': 'str',
        'photo': 'str',
        'quote': 'str',
        'store': 'Store',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('biography', 'Biography'),
        ('date_removed', 'DateRemoved'),
        ('favourite_id', 'FavouriteId'),
        ('first_name', 'FirstName'),
        ('is_enabled', 'IsEnabled'),
        ('member', 'Member'),
        ('occupation', 'Occupation'),
        ('photo', 'Photo'),
        ('quote', 'Quote'),
        ('store', 'Store'),
    ]))

    biography = models.TextField(
        null=True,
        help_text='The member’s bio.'
    )
    date_removed = models.DateTimeField(
        null=True,
        help_text='The date the member was disabled (assuming it has been '
                  'disabled).'
    )
    favourite_id = models.IntegerField(
        null=True,
        help_text='The ID of a favourite seller, if the call is authenticated'
                  ' and this member is a favourite seller for the '
                  'authenticated caller.'
    )
    first_name = models.TextField(
        null=True,
        help_text='The first name of the member.'
    )
    is_enabled = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the member account is enabled.'
    )
    member = models.ForeignKey(
        'Member',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='member_profile_reverse_member',
        help_text='Basic information about the member.'
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
    store = models.ForeignKey(
        'Store',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='member_profile_reverse_store',
        help_text='Store details, if the seller has been set up as a Trade Me'
                  ' store.'
    )

    class Meta:

        unique_together = (
            (
                'biography',
                'date_removed',
                'favourite_id',
                'first_name',
                'is_enabled',
                'member',
                'occupation',
                'photo',
                'quote',
                'store',
            ),
        )


class Properties(RawModel):

    swagger_types = types.MappingProxyType({
        'did_you_mean': 'str',
        'favourite_id': 'int',
        'favourite_type': 'int',
        'found_categories': 'list[FoundCategory]',
        'list': 'list[Property]',
        'member_profile': 'MemberProfile',
        'page': 'int',
        'page_size': 'int',
        'parameters': 'list[SearchParameter]',
        'sort_orders': 'list[AttributeOption]',
        'super_features': 'list[Property]',
        'total_count': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('did_you_mean', 'DidYouMean'),
        ('favourite_id', 'FavouriteId'),
        ('favourite_type', 'FavouriteType'),
        ('found_categories', 'FoundCategories'),
        ('list', 'List'),
        ('member_profile', 'MemberProfile'),
        ('page', 'Page'),
        ('page_size', 'PageSize'),
        ('parameters', 'Parameters'),
        ('sort_orders', 'SortOrders'),
        ('super_features', 'SuperFeatures'),
        ('total_count', 'TotalCount'),
    ]))

    did_you_mean = models.TextField(
        null=True,
        help_text='The suggestion string, if the search produced no results '
                  'and there is a popular search term that is lexigraphically'
                  ' close to the search string.'
    )
    favourite_id = models.IntegerField(
        null=True,
        help_text='The ID of a favourite search that corresponds to the '
                  'current search, if the call is authenticated and the '
                  'authenticated member has a favourite search that matches.'
    )
    favourite_type = models.IntegerField(
        choices=(
            (0, 'None'),
            (1, 'Category'),
            (3, 'Search'),
            (4, 'AttributeSearch'),
            (6, 'Seller'),
        ),
        null=True,
        help_text='The type of favourite (e.g. “Category”, “Search”, '
                  '“Seller”) that the FavouriteId property refers to. Only '
                  'applicable for searches that match one of the '
                  'authenticated user’s favourites.'
    )
    found_categories = models.ManyToManyField(
        'FoundCategory',
        related_name='properties_reverse_found_categories',
        help_text='A collection of suggested categories and the number of '
                  'search results in each category.'
    )
    list = models.ManyToManyField(
        'Property',
        related_name='properties_reverse_list',
        help_text='A list of the results in the current page.'
    )
    member_profile = models.ForeignKey(
        'MemberProfile',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='properties_reverse_member_profile',
        help_text='Details of the member that is being filtered on. Not '
                  'returned unless member_listing is non-zero and '
                  'return_metadata is true.'
    )
    page = models.IntegerField(
        null=True,
        help_text='The index of the current page of results (starts at 1).'
    )
    page_size = models.IntegerField(
        null=True,
        help_text='The number of results in the current page.'
    )
    parameters = models.ManyToManyField(
        'SearchParameter',
        related_name='properties_reverse_parameters',
        help_text='A list of search parameters which are applicable to the '
                  'searched category. Not returned unless return_metadata is '
                  'true.'
    )
    sort_orders = models.ManyToManyField(
        'AttributeOption',
        related_name='properties_reverse_sort_orders',
        help_text='A list of sort orders which are applicable to the searched'
                  ' category. Not returned unless return_metadata is true.'
    )
    super_features = models.ManyToManyField(
        'Property',
        related_name='properties_reverse_super_features',
        help_text='A randomised collection of super features matching the '
                  'current search'
    )
    total_count = models.IntegerField(
        null=True,
        help_text='The total number of results in the collection. Can be '
                  'larger than the number of returned results.'
    )

    class Meta:

        unique_together = (
            (
                'did_you_mean',
                'favourite_id',
                'favourite_type',
                'member_profile',
                'page',
                'page_size',
                'total_count',
            ),
        )


class Property(RawModel):

    swagger_types = types.MappingProxyType({
        'address': 'str',
        'adjacent_suburb_ids': 'list[PropertyAdjacentSuburbIds]',
        'adjacent_suburb_names': 'list[PropertyAdjacentSuburbNames]',
        'agency': 'Agency',
        'agency_reference': 'str',
        'amenities': 'str',
        'area': 'int',
        'area_range_max': 'int',
        'as_at': 'datetime',
        'available_from': 'str',
        'bathrooms': 'int',
        'bedrooms': 'int',
        'best_contact_time': 'str',
        'bid_count': 'int',
        'branding': 'Branding',
        'buy_now_price': 'float',
        'category': 'str',
        'category_path': 'str',
        'district': 'str',
        'district_id': 'int',
        'end_date': 'datetime',
        'geographic_location': 'GeographicLocation',
        'has_buy_now': 'bool',
        'has_embedded_video': 'bool',
        'has_free_shipping': 'bool',
        'has_gallery': 'bool',
        'has_home_page_feature': 'bool',
        'has_pay_now': 'bool',
        'has_reserve': 'bool',
        'ideal_tenant': 'str',
        'is_bold': 'bool',
        'is_boosted': 'bool',
        'is_buy_now_only': 'bool',
        'is_classified': 'bool',
        'is_clearance': 'bool',
        'is_featured': 'bool',
        'is_highlighted': 'bool',
        'is_new': 'bool',
        'is_on_watch_list': 'bool',
        'is_reserve_met': 'bool',
        'is_super_featured': 'bool',
        'land_area': 'int',
        'listing_group': 'str',
        'listing_id': 'int',
        'max_bid_amount': 'float',
        'max_tenants': 'int',
        'note_date': 'datetime',
        'open_homes': 'list[OpenHome]',
        'parking': 'str',
        'percentage_off': 'int',
        'pets_okay': 'int',
        'photo_urls': 'list[PropertyPhotoUrls]',
        'picture_href': 'str',
        'positive_review_count': 'int',
        'price_display': 'str',
        'promotion_id': 'int',
        'property_id': 'str',
        'property_type': 'str',
        'rateable_value': 'int',
        'region': 'str',
        'region_id': 'int',
        'remaining_gallery_plus_relists': 'int',
        'rent_per_week': 'float',
        'reserve_state': 'int',
        'short_description': 'str',
        'smokers_okay': 'int',
        'start_date': 'datetime',
        'start_price': 'float',
        'subtitle': 'str',
        'suburb': 'str',
        'suburb_id': 'int',
        'title': 'str',
        'total_review_count': 'int',
        'variant_definition_summary': 'VariantDefinitionSummary',
        'viewing_instructions': 'str',
        'was_price': 'float',
        'whiteware': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('address', 'Address'),
        ('adjacent_suburb_ids', 'AdjacentSuburbIds'),
        ('adjacent_suburb_names', 'AdjacentSuburbNames'),
        ('agency', 'Agency'),
        ('agency_reference', 'AgencyReference'),
        ('amenities', 'Amenities'),
        ('area', 'Area'),
        ('area_range_max', 'AreaRangeMax'),
        ('as_at', 'AsAt'),
        ('available_from', 'AvailableFrom'),
        ('bathrooms', 'Bathrooms'),
        ('bedrooms', 'Bedrooms'),
        ('best_contact_time', 'BestContactTime'),
        ('bid_count', 'BidCount'),
        ('branding', 'Branding'),
        ('buy_now_price', 'BuyNowPrice'),
        ('category', 'Category'),
        ('category_path', 'CategoryPath'),
        ('district', 'District'),
        ('district_id', 'DistrictId'),
        ('end_date', 'EndDate'),
        ('geographic_location', 'GeographicLocation'),
        ('has_buy_now', 'HasBuyNow'),
        ('has_embedded_video', 'HasEmbeddedVideo'),
        ('has_free_shipping', 'HasFreeShipping'),
        ('has_gallery', 'HasGallery'),
        ('has_home_page_feature', 'HasHomePageFeature'),
        ('has_pay_now', 'HasPayNow'),
        ('has_reserve', 'HasReserve'),
        ('ideal_tenant', 'IdealTenant'),
        ('is_bold', 'IsBold'),
        ('is_boosted', 'IsBoosted'),
        ('is_buy_now_only', 'IsBuyNowOnly'),
        ('is_classified', 'IsClassified'),
        ('is_clearance', 'IsClearance'),
        ('is_featured', 'IsFeatured'),
        ('is_highlighted', 'IsHighlighted'),
        ('is_new', 'IsNew'),
        ('is_on_watch_list', 'IsOnWatchList'),
        ('is_reserve_met', 'IsReserveMet'),
        ('is_super_featured', 'IsSuperFeatured'),
        ('land_area', 'LandArea'),
        ('listing_group', 'ListingGroup'),
        ('listing_id', 'ListingId'),
        ('max_bid_amount', 'MaxBidAmount'),
        ('max_tenants', 'MaxTenants'),
        ('note_date', 'NoteDate'),
        ('open_homes', 'OpenHomes'),
        ('parking', 'Parking'),
        ('percentage_off', 'PercentageOff'),
        ('pets_okay', 'PetsOkay'),
        ('photo_urls', 'PhotoUrls'),
        ('picture_href', 'PictureHref'),
        ('positive_review_count', 'PositiveReviewCount'),
        ('price_display', 'PriceDisplay'),
        ('promotion_id', 'PromotionId'),
        ('property_id', 'PropertyId'),
        ('property_type', 'PropertyType'),
        ('rateable_value', 'RateableValue'),
        ('region', 'Region'),
        ('region_id', 'RegionId'),
        ('remaining_gallery_plus_relists', 'RemainingGalleryPlusRelists'),
        ('rent_per_week', 'RentPerWeek'),
        ('reserve_state', 'ReserveState'),
        ('short_description', 'ShortDescription'),
        ('smokers_okay', 'SmokersOkay'),
        ('start_date', 'StartDate'),
        ('start_price', 'StartPrice'),
        ('subtitle', 'Subtitle'),
        ('suburb', 'Suburb'),
        ('suburb_id', 'SuburbId'),
        ('title', 'Title'),
        ('total_review_count', 'TotalReviewCount'),
        ('variant_definition_summary', 'VariantDefinitionSummary'),
        ('viewing_instructions', 'ViewingInstructions'),
        ('was_price', 'WasPrice'),
        ('whiteware', 'Whiteware'),
    ]))

    address = models.TextField(
        null=True,
        help_text='The address to display.'
    )
    adjacent_suburb_ids = models.ManyToManyField(
        'PropertyAdjacentSuburbIds',
        related_name='property_reverse_adjacent_suburb_ids',
        help_text='The IDs of any adjacent suburbs.'
    )
    adjacent_suburb_names = models.ManyToManyField(
        'PropertyAdjacentSuburbNames',
        related_name='property_reverse_adjacent_suburb_names',
        help_text='The names of any adjacent suburbs.'
    )
    agency = models.ForeignKey(
        'Agency',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='property_reverse_agency',
        help_text='Details of the agency this property was listed by.'
    )
    agency_reference = models.TextField(
        null=True,
        help_text='The reference to the agency.'
    )
    amenities = models.TextField(
        null=True,
        help_text='A list of the amenities in the area.'
    )
    area = models.IntegerField(
        null=True,
        help_text='The area of the house, in square metres.'
    )
    area_range_max = models.IntegerField(
        null=True,
        help_text='The maximum area of the house, in square metres.'
    )
    as_at = models.DateTimeField(
        null=True,
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
    bid_count = models.IntegerField(
        null=True,
        help_text='The number of bids on the item.'
    )
    branding = models.ForeignKey(
        'Branding',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='property_reverse_branding',
        help_text='A list of branding images associated with this listing.'
    )
    buy_now_price = models.FloatField(
        null=True,
        help_text='The Buy Now price.'
    )
    category = models.TextField(
        null=True,
        help_text='The listing category.'
    )
    category_path = models.TextField(
        null=True,
        help_text='The category path.'
    )
    district = models.TextField(
        null=True,
        help_text='The name of the district the property is located in.'
    )
    district_id = models.IntegerField(
        null=True,
        help_text='The ID of the district where this property is located.'
    )
    end_date = models.DateTimeField(
        null=True,
        help_text='The date the listing will end.'
    )
    geographic_location = models.ForeignKey(
        'GeographicLocation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='property_reverse_geographic_location',
        help_text='The geographic location (latitude and longitude) of a '
                  'property.'
    )
    has_buy_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Buy Now.'
    )
    has_embedded_video = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the listing has an embedded video'
    )
    has_free_shipping = models.NullBooleanField(
        null=True,
        help_text='Indicates if the listing offers free shipping as an option'
    )
    has_gallery = models.NullBooleanField(
        null=True,
        help_text='Is this a gallery listing?'
    )
    has_home_page_feature = models.NullBooleanField(
        null=True,
        help_text='Is this a homepage feature listing?'
    )
    has_pay_now = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has Pay Now.'
    )
    has_reserve = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item has a reserve.'
    )
    ideal_tenant = models.TextField(
        null=True,
        help_text='A description of the ideal tenant (are they tidy, a '
                  'professional couple, etc).'
    )
    is_bold = models.NullBooleanField(
        null=True,
        help_text='Is this a bold listing?'
    )
    is_boosted = models.NullBooleanField(
        null=True,
        help_text='If the listing has been boosted or not'
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
    is_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a featured listing?'
    )
    is_highlighted = models.NullBooleanField(
        null=True,
        help_text='Is this a highlighted listing?'
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
    is_reserve_met = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the item’s reserve has been met.'
    )
    is_super_featured = models.NullBooleanField(
        null=True,
        help_text='Is this a super featured listing?'
    )
    land_area = models.IntegerField(
        null=True,
        help_text='The area of the land, in square metres.'
    )
    listing_group = models.TextField(
        null=True,
        help_text='The listing group.'
    )
    listing_id = models.IntegerField(
        null=True,
        help_text='The ID of the listing.'
    )
    max_bid_amount = models.FloatField(
        null=True,
        help_text='The current leading bid amount.'
    )
    max_tenants = models.IntegerField(
        null=True,
        help_text='The maximum number of tenents.'
    )
    note_date = models.DateTimeField(
        null=True,
        help_text='The date of the note on an item.'
    )
    open_homes = models.ManyToManyField(
        'OpenHome',
        related_name='property_reverse_open_homes',
        help_text='A collection of open home times for this listing. Only '
                  'applies to open home listings.'
    )
    parking = models.TextField(
        null=True,
        help_text='Information on the availability of parking.'
    )
    percentage_off = models.IntegerField(
        null=True,
        help_text='The percentage that a product has been discounted. This '
                  'has been rounded for display purposes. This field will '
                  'only be populated if IsClearance is true .'
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
    photo_urls = models.ManyToManyField(
        'PropertyPhotoUrls',
        related_name='property_reverse_photo_urls',
        help_text='A collection of photo urls for the listing'
    )
    picture_href = models.TextField(
        null=True,
        help_text='The URL of the primary photo for the listing (if the '
                  'listing has a photo). By default you’ll get a thumbnail-'
                  'sized photo, but you can control the size of the photo '
                  'using the photo_size parameter.'
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
    promotion_id = models.IntegerField(
        null=True,
        help_text='The ID of the promotion applied to this listing.'
    )
    property_id = models.TextField(
        primary_key=True,
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
    rateable_value = models.IntegerField(
        null=True,
        help_text='The rateable value of the property.'
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
    rent_per_week = models.FloatField(
        null=True,
        help_text='The rent payable per week, in NZD.'
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
    short_description = models.TextField(
        null=True,
        help_text='Short description of a listing. This is Jobs and Services '
                  'specfic.'
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
    start_price = models.FloatField(
        null=True,
        help_text='The start price.'
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
    title = models.TextField(
        null=True,
        help_text='The listing title.'
    )
    total_review_count = models.IntegerField(
        null=True,
        help_text='The total number of user-submitted reviews. Currently only'
                  ' applies to services listings.'
    )
    variant_definition_summary = models.ForeignKey(
        'VariantDefinitionSummary',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='property_reverse_variant_definition_summary',
        help_text='A summary of the variant information.'
    )
    viewing_instructions = models.TextField(
        null=True,
        help_text='Instructions on how to view the property.'
    )
    was_price = models.FloatField(
        null=True,
        help_text='The usual price that a product is sold at, or the price '
                  'before it was marked down. This is always more than the '
                  'Buy Now price. This field will only be populated if '
                  'IsClearance is true .'
    )
    whiteware = models.TextField(
        null=True,
        help_text='A description of what is included in the rent (if '
                  'furnished).'
    )

    class Meta:

        unique_together = (
            (
                'property_id',
            ),
        )


class PropertyAdjacentSuburbIds(RawModel):

    expect_single_value = 'value'
    swagger_types = types.MappingProxyType({
        'value': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('value', 'value'),
    ]))

    value = models.IntegerField(
        null=True,
    )

    class Meta:

        unique_together = (
            (
                'value',
            ),
        )


class PropertyAdjacentSuburbNames(RawModel):

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


class PropertyPhotoUrls(RawModel):

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


class SearchParameter(RawModel):

    swagger_types = types.MappingProxyType({
        'allows_multiple_values': 'bool',
        'dependent_on': 'str',
        'dependent_parameter': 'SearchParameter',
        'display_name': 'str',
        'external_options_key': 'str',
        'lower_bound_name': 'str',
        'mutual_exclusion_group': 'str',
        'name': 'str',
        'options': 'list[AttributeOption]',
        'type': 'int',
        'upper_bound_name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('allows_multiple_values', 'AllowsMultipleValues'),
        ('dependent_on', 'DependentOn'),
        ('dependent_parameter', 'DependentParameter'),
        ('display_name', 'DisplayName'),
        ('external_options_key', 'ExternalOptionsKey'),
        ('lower_bound_name', 'LowerBoundName'),
        ('mutual_exclusion_group', 'MutualExclusionGroup'),
        ('name', 'Name'),
        ('options', 'Options'),
        ('type', 'Type'),
        ('upper_bound_name', 'UpperBoundName'),
    ]))

    allows_multiple_values = models.NullBooleanField(
        null=True,
        help_text='Indicates the user is allowed to select multiple values. '
                  'Each value should be comma-separated. Currently applies '
                  'only to String parameters.'
    )
    dependent_on = models.TextField(
        null=True,
        help_text='If present, the Name (not the DisplayName) of another '
                  'parameter. If the user is filtering by that other '
                  'parameter, then this filter becomes available for use. The'
                  ' parameter that is referenced will be a single-valued '
                  '(non-ranged).'
    )
    dependent_parameter = models.ForeignKey(
        'SearchParameter',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='search_parameter_reverse_dependent_parameter',
        help_text='Dependent parameter to display cascading structure'
    )
    display_name = models.TextField(
        null=True,
        help_text='The name of the search parameter, in a form suitable for '
                  'displaying to the user.'
    )
    external_options_key = models.TextField(
        null=True,
        help_text='If present, indicates that the list of options is not '
                  'immediately available, but can be retrieved from the '
                  'SearchOptions API endpoint. The value is the key that '
                  'should be passed to the SearchOptions API. Either the list'
                  ' of options is really long, or the list is dependent on '
                  'the value of another parameter (see the DependentOn '
                  'field).'
    )
    lower_bound_name = models.TextField(
        null=True,
        help_text='If the parameter is a ranged parameter, this is the name '
                  'of the parameter to use to specify the lower bound.'
    )
    mutual_exclusion_group = models.TextField(
        null=True,
        help_text='If present, indicates this parameter is part of a group of'
                  ' parameters which are all mutually exclusive. The group '
                  'name can be used as a heading name.'
    )
    name = models.TextField(
        null=True,
        help_text='The name of the search parameter.'
    )
    options = models.ManyToManyField(
        'AttributeOption',
        related_name='search_parameter_reverse_options',
        help_text='A list of options to display to the user.'
    )
    type = models.IntegerField(
        choices=(
            (0, 'Boolean'),
            (1, 'Numeric'),
            (2, 'String'),
            (3, 'PropertyRegionId'),
            (4, 'PropertyDistrictId'),
            (5, 'PropertySuburbId'),
            (6, 'Location'),
        ),
        null=True,
        help_text='Indicates the type of the parameter value.'
    )
    upper_bound_name = models.TextField(
        null=True,
        help_text='If the parameter is a ranged parameter, this is the name '
                  'of the parameter to use to specify the upper bound.'
    )

    class Meta:

        unique_together = (
            (
                'allows_multiple_values',
                'dependent_on',
                'dependent_parameter',
                'display_name',
                'external_options_key',
                'lower_bound_name',
                'mutual_exclusion_group',
                'name',
                'type',
                'upper_bound_name',
            ),
        )


class VariantDefinitionSummary(RawModel):

    swagger_types = types.MappingProxyType({
        'all_discounted': 'bool',
        'all_on_clearance': 'bool',
        'discount_percent': 'int',
        'discount_percent_high': 'int',
        'discount_percent_low': 'int',
        'has_discount_percent_range': 'bool',
        'has_price_range': 'bool',
        'price': 'float',
        'price_high': 'float',
        'price_low': 'float',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('all_discounted', 'AllDiscounted'),
        ('all_on_clearance', 'AllOnClearance'),
        ('discount_percent', 'DiscountPercent'),
        ('discount_percent_high', 'DiscountPercentHigh'),
        ('discount_percent_low', 'DiscountPercentLow'),
        ('has_discount_percent_range', 'HasDiscountPercentRange'),
        ('has_price_range', 'HasPriceRange'),
        ('price', 'Price'),
        ('price_high', 'PriceHigh'),
        ('price_low', 'PriceLow'),
    ]))

    all_discounted = models.NullBooleanField(
        null=True,
        help_text='Whether or not the variants are all discounted.'
    )
    all_on_clearance = models.NullBooleanField(
        null=True,
        help_text='Whether or not the variants are all on clearance.'
    )
    discount_percent = models.IntegerField(
        null=True,
        help_text='The discount percentage of all the variants, if they are '
                  'all the same.'
    )
    discount_percent_high = models.IntegerField(
        null=True,
        help_text='The highest discount percentage of all the variants, if '
                  'there is a discount percentage range.'
    )
    discount_percent_low = models.IntegerField(
        null=True,
        help_text='The lowest discount percentage of all the variants, if '
                  'there is a discount percentage range.'
    )
    has_discount_percent_range = models.NullBooleanField(
        null=True,
        help_text='Whether or not the variants have a single discount '
                  'percentage or a discount percentage range.'
    )
    has_price_range = models.NullBooleanField(
        null=True,
        help_text='Whether or not the variants have a single price or a price'
                  ' range.'
    )
    price = models.FloatField(
        null=True,
        help_text='The price of all the variants, if they are all the same.'
    )
    price_high = models.FloatField(
        null=True,
        help_text='The highest price of all the variants, if there is a price'
                  ' range.'
    )
    price_low = models.FloatField(
        null=True,
        help_text='The lowest price of all the variants, if there is a price '
                  'range.'
    )

    class Meta:

        unique_together = (
            (
                'all_discounted',
                'all_on_clearance',
                'discount_percent',
                'discount_percent_high',
                'discount_percent_low',
                'has_discount_percent_range',
                'has_price_range',
                'price',
                'price_high',
                'price_low',
            ),
        )


__all__ = (
    'FlatmateAdjacentSuburbIds',
    'FlatmateAdjacentSuburbNames',
    'FlatmatePhotoUrls',
    'Flatmate',
    'Flatmates',
    'FoundCategory',
    'MemberProfile',
    'Properties',
    'PropertyAdjacentSuburbIds',
    'PropertyAdjacentSuburbNames',
    'PropertyPhotoUrls',
    'Property',
    'SearchParameter',
    'VariantDefinitionSummary',
)
