from .registry import model_registry


SearchResults = model_registry.register_namedtuple_model(
    'search.SearchResults',
    required=['page', 'page_size', 'total_count', 'list'],
    lists=['list'],
)
