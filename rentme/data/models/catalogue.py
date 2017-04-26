from django.db import models
from trademe.models.enums import AreaOfBusiness

from ._utils import default_debug_methods, EnumIntegerField
from .registry import model_registry


@model_registry.register_django_model
@default_debug_methods
class Category(models.Model):

    class Meta:
        ordering = ['number']

    number = models.TextField(primary_key=True)
    name = models.TextField()
    path = models.TextField()
    is_restricted = models.BooleanField(default=False)
    has_legal_notice = models.BooleanField(default=False)
    has_classifieds = models.BooleanField(default=False)
    area_of_business = EnumIntegerField(enum=AreaOfBusiness, null=True)
    parent = models.ForeignKey('self', related_name='subcategories', null=True)


@model_registry.register_django_model
@default_debug_methods
class Locality(models.Model):

    class Meta:
        ordering = ['name']

    locality_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model
@default_debug_methods
class District(models.Model):

    class Meta:
        ordering = ['name']

    locality = models.ForeignKey(Locality, related_name='districts')
    district_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model(delayed_fks=['adjacent_suburbs'])
@default_debug_methods
class Suburb(models.Model):

    class Meta:
        ordering = ['name']

    district = models.ForeignKey(District, related_name='suburbs')
    suburb_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    adjacent_suburbs = models.ManyToManyField('self')


@model_registry.register_django_model
@default_debug_methods
class MembershipLocality(models.Model):

    class Meta:
        ordering = ['name']

    locality_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model
@default_debug_methods
class MembershipDistrict(models.Model):

    class Meta:
        ordering = ['name']

    locality = models.ForeignKey(MembershipLocality, related_name='districts')
    district_id = models.IntegerField(primary_key=True)
    name = models.TextField()
