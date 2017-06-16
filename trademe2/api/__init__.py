from . import base
from . import catalogue, detail, search


class RootManager(base.APIManagerBase):

    class Endpoints:
        catalogue = catalogue.Manager
        detail = detail.Manager
        search = search.Manager
