import types

from django.db import models
import multidict
from trademe.models.enums import AreaOfBusiness

from rentme.data.models._utils import EnumIntegerField


class Category(models.Model):

    swagger_types = types.MappingProxyType({
        'area_of_business': 'int',
        'can_be_second_category': 'bool',
        'can_have_second_category': 'bool',
        'count': 'int',
        'has_classifieds': 'bool',
        'has_legal_notice': 'bool',
        'is_restricted': 'bool',
        'name': 'str',
        'number': 'str',
        'path': 'str',
        'subcategories': 'list[Category]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('area_of_business', 'AreaOfBusiness'),
        ('can_be_second_category', 'CanBeSecondCategory'),
        ('can_have_second_category', 'CanHaveSecondCategory'),
        ('count', 'Count'),
        ('has_classifieds', 'HasClassifieds'),
        ('has_legal_notice', 'HasLegalNotice'),
        ('is_restricted', 'IsRestricted'),
        ('name', 'Name'),
        ('number', 'Number'),
        ('path', 'Path'),
        ('subcategories', 'Subcategories'),
    ]))

    area_of_business = EnumIntegerField(
        enum=AreaOfBusiness,
        help_text='Area of business this category is related to',
        null=True,
    )
    can_be_second_category = models.NullBooleanField(
        help_text='Indicates whether this category can be selected as a '
                  'second category.',
        null=True,
    )
    can_have_second_category = models.NullBooleanField(
        help_text='Indicates whether this category can be paired with a '
                  'second category.',
        null=True,
    )
    count = models.IntegerField(
        help_text='The number of items for sale in this category.',
        null=True,
    )
    has_classifieds = models.NullBooleanField(
        help_text='Indicates whether classifieds are allowed in this '
                  'category.',
        null=True,
    )
    has_legal_notice = models.NullBooleanField(
        help_text='Indicates whether the category has legal requirements. You'
                  ' should ask the user to accept the legal notice before '
                  'listing in this category. There is an API to get the text '
                  'of the legal notice.',
        null=True,
    )
    is_restricted = models.NullBooleanField(
        help_text='Indicates whether the category is restricted to adults '
                  'only (i.e. the category is R18).',
        null=True,
    )
    name = models.TextField(
        help_text='The name of the category.',
        null=True,
    )
    number = models.TextField(
        primary_key=True,
        help_text='A unique identifier for the category e.g. '
                  '“0004-0369-6076-“. We plan to change this to a numeric '
                  'identifier (e.g. “6076”) so you should ensure you can cope'
                  ' with both formats.',
    )
    path = models.TextField(
        help_text='The full URL path of this category e.g. “/Home-'
                  'living/Beds-bedroom-furniture/Bedside-tables”.',
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        null=True,
        on_delete=models.CASCADE,
        help_text='The list of subcategories belonging to this category.',
    )

    class Meta:
        ordering = ['number']


class Locality(models.Model):

    swagger_types = types.MappingProxyType({
        'districts': 'list[District]',
        'locality_id': 'int',
        'name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('districts', 'Districts'),
        ('locality_id', 'LocalityId'),
        ('name', 'Name'),
    ]))

    locality_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the region.',
    )
    name = models.TextField(
        help_text='The name of the region.',
        null=True,
    )

    class Meta:
        ordering = ['name']


class District(models.Model):

    locality = models.ForeignKey(
        'Locality',
        related_name='districts',
        help_text='The list of districts that belong to this region.',
    )

    swagger_types = types.MappingProxyType({
        'district_id': 'int',
        'name': 'str',
        'suburbs': 'list[Suburb]',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('district_id', 'DistrictId'),
        ('name', 'Name'),
        ('suburbs', 'Suburbs'),
    ]))

    district_id = models.IntegerField(
        help_text='The ID of the district.',
        primary_key=True,
    )
    name = models.TextField(
        help_text='The name of the district.',
        null=True,
    )

    class Meta:
        ordering = ['name']


class SuburbAdjacentSuburbs(models.Model):

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


class Suburb(models.Model):

    district = models.ForeignKey(
        'District',
        related_name='suburbs',
        help_text='The list of suburbs that belong to this district.',
    )
    adjacent_suburbs = models.ManyToManyField(
        'self',
    )

    swagger_types = types.MappingProxyType({
        'adjacent_suburbs_ids': 'list[SuburbAdjacentSuburbs]',
        'name': 'str',
        'suburb_id': 'int',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('adjacent_suburbs_ids', 'AdjacentSuburbs'),
        ('name', 'Name'),
        ('suburb_id', 'SuburbId'),
    ]))

    adjacent_suburbs_ids = models.ManyToManyField(
        'SuburbAdjacentSuburbs',
        related_name='suburb_reverse_adjacent_suburbs',
        help_text='A list containing the IDs of the suburbs adjacent to this '
                  'suburb.',
    )
    name = models.TextField(
        help_text='The name of the suburb.',
        null=True,
    )
    suburb_id = models.IntegerField(
        help_text='The ID of the suburb.',
        primary_key=True,
    )

    class Meta:

        ordering = ['name']


class MembershipLocality(models.Model):

    swagger_types = types.MappingProxyType({
        'districts': 'list[MembershipDistrict]',
        'locality_id': 'int',
        'name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('districts', 'Districts'),
        ('locality_id', 'LocalityId'),
        ('name', 'Name'),
    ]))

    locality_id = models.IntegerField(
        primary_key=True,
        help_text='The ID of the region.',
    )
    name = models.TextField(
        help_text='The name of the region.',
        null=True,
    )

    class Meta:
        ordering = ['name']


class MembershipDistrict(models.Model):

    locality = models.ForeignKey(
        'MembershipLocality',
        related_name='districts',
        help_text='The list of districts that belong to this region.',
    )

    swagger_types = types.MappingProxyType({
        'district_id': 'int',
        'name': 'str',
    })
    attribute_map = multidict.MultiDictProxy(multidict.MultiDict([
        ('district_id', 'DistrictId'),
        ('name', 'Name'),
    ]))
    district_id = models.IntegerField(
        help_text='The ID of the district.',
        primary_key=True,
    )
    name = models.TextField(
        help_text='The name of the district.',
        null=True,
    )

    class Meta:
        ordering = ['name']
