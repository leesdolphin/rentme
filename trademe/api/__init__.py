from . import catalogue  # noqa
from . import base


class RootManager(base.APIManagerBase):

    class Endpoints:
        catalogue = catalogue.Manager
