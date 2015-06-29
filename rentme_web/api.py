import rentme_web.models as models
import trademe.api as api


def load_trademe_locality_information():
    session = api.API()
    ## Array
    localities = session.get_localities()
    for locality in localities:
        l_name = locality["Name"]
        l_id = locality["LocalityId"]
        for districts in locality["Districts"]:
            d_name = districts["Name"]
            d_id = districts["DistrictId"]
            for suburb in districts["Suburbs"]:
                s_name = suburb["Name"]
                s_id = suburb["SuburbId"]
                for adj_suburb_id in districts["AdjacentSuburbs"]:




