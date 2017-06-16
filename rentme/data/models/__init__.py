from rentme.raw.loader import ModuleDiscoverer, MutliDiscoverer
from . import catalogue


def create_discoverer():
    return MutliDiscoverer(
        ModuleDiscoverer(catalogue),
    )
