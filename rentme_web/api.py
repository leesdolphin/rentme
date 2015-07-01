import rentme_web.models as models
import trademe.api as api
from requests.structures import CaseInsensitiveDict

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
    params = CaseInsensitiveDict(kwargs)
    params.setdefault('page', 1)
    params.setdefault('rows', 200)
    rows = params['rows'] = int(params['rows'])
    print("Params:", params)
    session = api.API()
    more_pages = True
    while more_pages:
        rentals = session.get_rental_touch(params)
        for listing_data in rentals['List']:
            ## This loads preliminary data. It is sufficient to display; but
            ##  full data should be loaded before displaying individual listing.
            try:
                listing = models.TradeMeListing.objects.get(
                    id=listing_data["ListingId"])
            except models.TradeMeListing.DoesNotExist:
                listing = models.TradeMeListing(id=listing_data["ListingId"])
            listing.title = listing_data["Title"]
            listing.category = listing_data["Category"]
            listing.start_date = _d(listing_data["StartDate"])
            listing.end_date = _d(listing_data["EndDate"])
            listing.generated_at = _d(listing_data["AsAt"])
            listing.agency =



        params['page'] = rentals["Page"] + 1
        more_pages = (rentals["PageSize"] >= rows)
    return rentals






