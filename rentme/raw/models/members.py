import types

from django.db import models
import multidict

from .base import RawModel


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
        related_name='member_profile',
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


class Store(models.Model):

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


__all__ = (
    'LargeBannerImage',
    'Member',
    'MemberProfile',
    'Store',
    'StorePromotion',
)
