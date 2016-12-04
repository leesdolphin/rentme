from .registry import model_registry


Category = model_registry.register_namedtuple_model(
    'catalogue.Category',
    required=['number', 'path', 'name'],
    defaults=dict(area_of_business=None, has_classifieds=False,
                  subcategories=None, has_legal_notice=False,
                  is_restricted=False),
    lists=['subcategories'],
)

Locality = model_registry.register_namedtuple_model(
    'catalogue.Locality',
    required=['locality_id', 'name'],
    defaults=dict(districts=None),
    lists=['districts'],
)
District = model_registry.register_namedtuple_model(
    'catalogue.District',
    required=['district_id', 'name'],
    defaults=dict(suburbs=None),
    lists=['suburbs'],
)
Suburb = model_registry.register_namedtuple_model(
    'catalogue.Suburb',
    required=['suburb_id', 'name'],
    defaults=dict(adjacent_suburbs=None),
    lists=['adjacent_suburbs'],
)

MembershipLocality = model_registry.register_namedtuple_model(
    'catalogue.MembershipLocality',
    required=['locality_id', 'name'],
    defaults=dict(districts=None),
    lists=['districts'],
)
MembershipDistrict = model_registry.register_namedtuple_model(
    'catalogue.MembershipDistrict',
    required=['district_id', 'name'],
)
