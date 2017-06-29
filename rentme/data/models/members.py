from django.db import models


class Member(models.Model):

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
