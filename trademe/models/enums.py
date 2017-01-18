import enum


def named_enum(name, item):
    if isinstance(item, str):
        item = item.split(' ')
    item = map(str.strip, item)
    return enum.Enum(name, dict(zip(item, item)), module=__name__)


@enum.unique
class AreaOfBusiness(enum.Enum):
    All = 0
    Marketplace = 1
    Property = 2
    Motors = 3
    Jobs = 4
    Services = 5


SearchSortOrder = named_enum('SearchSortOrder',
                             'Default FeaturedFirst SuperGridFeaturedFirst '
                             'TitleAsc ExpiryAsc ExpiryDesc PriceAsc PriceDesc '
                             'BidsMost BuyNowAsc BuyNowDesc ReviewsDesc '
                             'HighestSalary LowestSalary LowestKilometres '
                             'HighestKilometres NewestVehicle OldestVehicle '
                             'BestMatch LargestDiscount')
PhotoSize = named_enum('PhotoSize',
                       'Thumbnail List Medium Gallery Large FullSize')
PropertyType = named_enum('PropertyType', 'Apartment CarPark House Townhouse Unit')
AllowsPickups = enum.Enum('AllowsPickups', 'None Allow Demand Forbid', start=0)
GeographicLocationAccuracy = enum.Enum('GeographicLocationAccuracy',
                                       'None Address Suburb Street', start=0)
