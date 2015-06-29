import rentme_web.models as models
import trademe.api as api


def load_trademe_locality_information():
    session = api.API()
    api.get_localities()


