from api.base.manager import APIManagerBase
from api.trademe import catalogue, detail, search


class RootManager(APIManagerBase):

    class Endpoints:
        catalogue = catalogue.Manager
        detail = detail.Manager
        search = search.Manager
