from django.db import models

from rentme.raw.loader import ModuleDiscoverer, MutliDiscoverer
from . import catalogue
from . import listings, members  # noqa: F401


def create_discoverer():
    return MutliDiscoverer(
        ModuleDiscoverer(catalogue),
    )
