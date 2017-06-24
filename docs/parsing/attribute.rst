Attribute Parsing
=================

Ignore:
 - ``price``
 - ``suburb``
 - ``district``
 - ``region``

Generated:
 - ``current_flatmates`` -- Probably an interpolation of ``Flatmate.current_flatmates`` and ``Flatmate.flatmates``
 - ``maximum_tenants`` -- Generated from ``max_tenants``
 - ``rooms`` -- Generated from ``bedrooms``/``bathrooms``/``property_type``
 - ``pets_and_smokers`` -- Generated from ``pets_okay``/``smokers_okay``

Questionable:
 - ``property_id`` -- An incrementing counter starting with ``FIH``. Purpose unknown. Appears to be a replacement for ``agency_reference_#`` for non-agency users.

Useful:
 - ``agency_reference_#`` -
 - ``location`` -- Property Address, or address fragment. Also given in search results as ``address``
 - ``furnishings`` -- Free text(don't try to parse, you'll fail)
 - ``avaliable`` -- Also given in search results as ``available_from``
 - ``ideal_tenants``/``ideal_flatmates`` -- Free text
 - ``parking`` -- Free text
 - ``in_the_area`` -- Free text
 - ``smoke_alarm`` -- ``Yes`` or ``No``



Included in tables
==================
agency_reference
amenities
as_at - Retrevial time.
available_from
bathrooms
bedrooms
best_contact_time
body
current_flatmates
end_date
flatmates
has_contact_details
ideal_tenant
listing_id
max_tenants
parking
pets_okay
property_id
property_type
rent_per_week
smokers_okay
start_date
title
whiteware

FKs
---
broadband_technologies
agency
category
embedded_content
geographic_location
member
member_profile
photo
photos
suburb

Excluded from tables
====================

``adjacent_suburb_ids``, ``adjacent_suburb_names``, ``region``
``district``
``district_id``
``region``
``region_id``
``suburb``

``category_name``, ``category_path`` - Duplicated by ``category``

price_display

``reserve_state`` - When == 3, redundant. Should not be any other value.
``start_price`` - When == 0, redundant.
``allows_pickups`` - Not useful.
``can_add_to_cart`` - False, redundant.
``is_classified``
``note_date`` 1st Jan 1970
``payment_options`` - Empty
``price_display``
``supports_questions_and_answers`` - Always false.

Wut?
====

listing_group
