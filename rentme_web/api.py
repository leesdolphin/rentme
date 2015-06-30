import rentme_web.models as models
import trademe.api as api


def load_trademe_locality_information():
    session = api.API()
    adj_suburbs = {}
    ## Array
    localities = session.get_localities()
    for locality in localities:
        l_name = locality["Name"]
        l_id = locality["LocalityId"]
        l, _ = models.TradeMeLocality.objects.get_or_create(id=l_id,
                                                            name=l_name)
        print(l)
        for districts in locality["Districts"]:
            d_name = districts["Name"]
            d_id = districts["DistrictId"]
            d, _ = models.TradeMeDistrict.objects.get_or_create(id=d_id,
                                                                name=d_name,
                                                                locality=l)
            for suburb in districts["Suburbs"]:
                s_name = suburb["Name"]
                s_id = suburb["SuburbId"]
                s, _ = models.TradeMeSuburb.objects.get_or_create(id=s_id,
                                                                  name=s_name,
                                                                  district=d)
                adj_suburbs[s] = suburb.get("AdjacentSuburbs", [])
    ## All suburbs added, now handle adjacency.
    for suburb, adj_list in adj_suburbs.items():
        suburb.adjacent_suburbs = models.TradeMeSuburb.objects\
                                        .filter(id__in=adj_list).all()
    return localities

def load_rentals(**kwargs):
    ## TODO create suburbs string
    session = api.API()
    rentals = session.get_rental_touch(kwargs)
    return rentals






