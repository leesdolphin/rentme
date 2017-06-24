from rentme.raw.loader import ModuleDiscoverer, MutliDiscoverer
from . import catalogue, listing


def create_discoverer():
    return MutliDiscoverer(
        ModuleDiscoverer(catalogue),
    )
