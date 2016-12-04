from django.db import models
from trademe.models.enums import AreaOfBusiness

from ._utils import EnumIntegerField
from .registry import model_registry


@model_registry.register_django_model
class Category(models.Model):

    number = models.TextField(primary_key=True)
    name = models.TextField()
    path = models.TextField()
    is_restricted = models.BooleanField(default=False)
    has_legal_notice = models.BooleanField(default=False)
    has_classifieds = models.BooleanField(default=False)
    area_of_business = EnumIntegerField(enum=AreaOfBusiness, null=True)
    parent = models.ForeignKey('self', related_name='subcategories', null=True)


@model_registry.register_django_model
class Locality(models.Model):

    locality_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model
class District(models.Model):

    locality = models.ForeignKey(Locality, related_name='districts')
    district_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model
class Suburb(models.Model):

    district = models.ForeignKey(District, related_name='suburbs')
    suburb_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    adjacent_suburbs = models.ManyToManyField('self')


@model_registry.register_django_model
class MembershipLocality(models.Model):

    locality_id = models.IntegerField(primary_key=True)
    name = models.TextField()


@model_registry.register_django_model
class MembershipDistrict(models.Model):

    locality = models.ForeignKey(MembershipLocality, related_name='districts')
    district_id = models.IntegerField(primary_key=True)
    name = models.TextField()
