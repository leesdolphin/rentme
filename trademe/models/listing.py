from .registry import model_registry
from .enums import GeographicLocationAccuracy

Listing = model_registry.register_namedtuple_model(
    'listing.Listing',
    required=[
'allows_pickups',
'as_at',
'attributes',
'bidder_and_watchers',
'body',
'can_add_to_cart',
'category_name',
'category_path',
'category',
'embedded_content',
'end_date',
'geographic_location',
'has_gallery',
'is_bold',
'is_classified',
'is_featured',
'is_highlighted',
'listing_id',
'listing_length',
'member',
'note_date',
'open_homes',
'payment_options',
'photo_id',
'photos',
'price_display',
'region_id',
'region',
'reserve_state',
'shipping_options',
'start_date',
'start_price',
'suburb_id',
'suburb',
'title',
'view_count',
],
    defaults=dict(broadband_technologies=(), contact_details=None),
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
    defaults=dict(original_width=-1, original_height=-1),
)

Photo = model_registry.register_namedtuple_model(
    'listing.Photo',
    required=['thumbnail', 'list', 'medium', 'gallery', 'large', 'full_size', 'plus_size', 'photo_id'],
    defaults=dict(original_width=-1, original_height=-1),
)


def photo__str(self):
    return '%s(photo_id=%r, original_width=%r, original_height=%r)' \
            % (self.__class__.__name__, self.photo_id,
               self.original_width, self.original_height)


Photo.__str__ = photo__str
Photo.__repr__ = photo__str
del photo__str
