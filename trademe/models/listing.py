from .enums import GeographicLocationAccuracy
from .registry import model_registry

Listing = model_registry.register_namedtuple_model(
    'listing.Listing',
    required=[
        'allows_pickups', 'as_at', 'attributes', 'body', 'can_add_to_cart',
        'category', 'end_date', 'geographic_location', 'is_classified',
        'is_featured', 'listing_id', 'member', 'note_date', 'photos',
        'price_display', 'start_date', 'suburb_id', 'suburb_name', 'title',
        'view_count',
    ],
    defaults=dict(broadband_technologies=(),
                  bidder_and_watchers=0, viewing_tracker_supported=False,
                  agency=None, is_super_featured=False, super_feature_end_date=None,
                  is_highlighted=False, is_bold=False, has_gallery=False, photo_id=None),
    lists=['photos', 'attributes', 'broadband_technologies'],
)

Attributes = model_registry.register_namedtuple_model(
    'listing.Attributes',
    required=['name', 'value', 'display_name'],
)

BroadbandTechnology = model_registry.register_namedtuple_model(
    'listing.BroadbandTechnology',
    required=['completion', 'name', 'availability'],
    defaults=dict(min_down=0, max_down=0, min_up=0, max_up=0),
)

GeographicLocation = model_registry.register_namedtuple_model(
    'listing.GeographicLocation',
    required=['accuracy', 'easting', 'latitude', 'longitude', 'northing'],
    enums=dict(accuracy=GeographicLocationAccuracy),
)

Member = model_registry.register_namedtuple_model(
    'listing.Member',
    required=['unique_positive', 'date_joined', 'is_authenticated', 'member_id',
              'nickname', 'unique_negative', 'feedback_count', 'region',
              'suburb', 'is_address_verified', 'date_address_verified', 'photo'],
              defaults=dict(original_width=-1, original_height=-1, is_in_trade=False, occupation=None, biography=None, quote=None),
)

Photo = model_registry.register_namedtuple_model(
    'listing.Photo',
    required=['thumbnail', 'list', 'medium', 'gallery', 'large', 'full_size', 'plus_size', 'photo_id'],
    defaults=dict(original_width=-1, original_height=-1),
)

Agency = model_registry.register_namedtuple_model(
    'listing.Agency',
    required=[
        'branding_large_banner_url', 'id',
        'is_real_estate_agency', 'branding_background_color', 'name',
        'branding_stroke_color', 'branding_office_location',
        'branding_text_color'
    ],
    defaults=dict(logo=None, logo2=None, website=None, fax_number=None,
                  is_licensed_property_agency=True, phone_number=None,
                  branding_disable_banner=False),
    lists=['agents']
)

AgencyAgent = model_registry.register_namedtuple_model(
    'listing.AgencyAgent',
    required=['full_name'],
    defaults=dict(mobile_phone_number=None, office_phone_number=None,
                  photo=None, url_slug=None)
)


ViewingTime = model_registry.register_namedtuple_model(
    'listing.ViewingTime',
    required=['viewing_id', 'viewing_time'],
)

def photo__str(self):
    return '%s(photo_id=%r, original_width=%r, original_height=%r)' \
            % (self.__class__.__name__, self.photo_id,
               self.original_width, self.original_height)


Photo.__str__ = photo__str
Photo.__repr__ = photo__str
del photo__str
