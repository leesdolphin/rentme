from rentme.raw.loader import ModuleDiscoverer, MutliDiscoverer
from . import base, catalogue, listings, search


def create_discoverer():
    return MutliDiscoverer(
        ModuleDiscoverer(base),
        ModuleDiscoverer(catalogue),
        ModuleDiscoverer(listings),
        ModuleDiscoverer(search),
    )
