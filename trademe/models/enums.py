import enum


@enum.unique
class AreaOfBusiness(enum.Enum):
    All = 0
    Marketplace = 1
    Property = 2
    Motors = 3
    Jobs = 4
    Services = 5
