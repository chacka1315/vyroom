from enum import Enum


class UserType(str, Enum):
    person = "person"
    agency = "agency"


class ListingType(str, Enum):
    rent = "rent"
    sale = "sale"


class PropertyType(str, Enum):
    apartment = "apartment"
    house = "house"
    land = "land"
    building = "building"


class PropertySubType(str, Enum):
    office = "office"
    shop = "shop"
    warehouse = "warehouse"
    restaurant = "restaurant"


class PropertyUse(str, Enum):
    residential = "residential"
    commercial = "commercial"


class ListingStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    sold = "sold"
    rented = "rented"
