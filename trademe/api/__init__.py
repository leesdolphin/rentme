from . import base
from . import catalogue, listing, search


class RootManager(base.APIManagerBase):

    class Endpoints:
        catalogue = catalogue.Manager
        listing = listing.Manager
        search = search.Manager
