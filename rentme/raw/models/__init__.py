from rentme.raw.loader import Deserializer, ModuleDiscoverer, MutliDiscoverer
from . import catalogue, listings


def create_deserialiser():
    return Deserializer(MutliDiscoverer(
        ModuleDiscoverer(catalogue),
        ModuleDiscoverer(listings),
    ))
