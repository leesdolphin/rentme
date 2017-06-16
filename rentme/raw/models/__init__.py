from rentme.raw.loader import Deserializer, ModuleDiscoverer, MutliDiscoverer
from . import base, catalogue, listings, search


def create_deserialiser():
    return Deserializer(MutliDiscoverer(
        ModuleDiscoverer(base),
        ModuleDiscoverer(catalogue),
        ModuleDiscoverer(listings),
        ModuleDiscoverer(search),
    ))
