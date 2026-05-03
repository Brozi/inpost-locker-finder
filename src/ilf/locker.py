from dataclasses import dataclass
@dataclass
class Locker:
    """Represents a single parcel locker"""
    name: str
    status: str
    location_247: bool
    opening_hours: str
    easy_access_zone: bool
    location_description: str
    location_description_1: str
    location_description_2: str
    address_line1: str
    address_line2: str
    address_details_city: str
    address_details_post_code: str