from dataclasses import dataclass
@dataclass
class Locker:
    """Represents a single parcel locker. The attributes represent all
    fields that the program is going to use.
    """
    name: str
    status: str
    location_247: bool
    opening_hours: str
    easy_access_zone: bool
    location_description: str
    address: str
    address_details_city: str
    address_details_post_code: str

    @classmethod
    def from_api_dict(cls, point: dict) -> "Locker":
        """Takes a raw data (dict) from the api and returns a Locker object, while
        cleaning any None or missing values.
        :param cls: the Locker class
        :param point: A single point from the api response
        :return: a Locker object with cleaned data
        """
        desc_1 = point.get('location_description', {})
        desc_2 = point.get('location_description_1', {})
        desc_3 = point.get('location_description_2', {})

        raw_desc = [desc_1, desc_2, desc_3]

        cleaned_desc = ", ".join(filter(None, raw_desc))

        address_1 = point.get('address', {})['line1']
        address_2 = point.get('address', {})['line2']

        address_combined = f"{address_1}, {address_2}"

        opening_hours = point.get('opening_hours', {})
        location_247 = point.get('location_247', False)

        opening_hours_dict = point.get('opening_hours_extended', {}).get(
            'customer', {})

        #for key in opening_hours_dict.keys():


        if not opening_hours:
            if location_247:
                opening_hours = "24/7"



        return cls(
            name=point['name'],
            status=point['status'],
            location_247=point['location_247'],
            opening_hours=opening_hours,
            easy_access_zone=point['easy_access_zone'],
            location_description=cleaned_desc,
            address=address_combined,
            address_details_city=point.get('address_details', {})['city'],
            address_details_post_code=point.get('address_details', {})['post_code'],
        )