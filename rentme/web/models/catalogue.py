import enum

from django.db import models

from ._utils import EnumIntegerField


class Category(models.Model):

    name = models.TextField()
    number = models.TextField(primary_key=True)
    path = models.TextField()
    is_restricted = models.BooleanField()
    has_legal_notice = models.BooleanField()
    has_classifieds = models.BooleanField()
    area_of_business = EnumIntegerField(enum=AreaOfBusiness)

    subcatagories = models.ForeignKey('self', related_name='parent')


class Locality(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class District(models.Model):

    locality = models.ForeignKey(Locality, related_name='districts')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class Suburb(models.Model):

    district = models.ForeignKey(District, related_name='suburbs')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    adjacent_suburbs = models.ManyToManyField('self')


class MembershipLocality(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField()


class MembershipDistrict(models.Model):

    locality = models.ForeignKey(Locality, related_name='districts')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
