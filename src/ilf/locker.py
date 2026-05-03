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

        return cls(
            name=point['name'],
            status=point['status'],
            location_247=point['location_247'],
            opening_hours=cls._parse_schedule(point),
            easy_access_zone=point['easy_access_zone'],
            location_description=cls._clean_description(point),
            address=cls._combine_address(point),
            address_details_city=point.get('address_details', {})['city'],
            address_details_post_code=point.get('address_details', {})['post_code'],
        )


    @staticmethod
    def _clean_description(point:dict) -> str:
        """
        Helper function to clean the description of the point
        :param: point: a dict containing data about a single point
        :return: a cleaned description: concated into one string and rid of any nulls
        """
        desc_1 = point.get('location_description', {})
        desc_2 = point.get('location_description_1', {})
        desc_3 = point.get('location_description_2', {})

        raw_desc = [desc_1, desc_2, desc_3]

        cleaned_desc = ", ".join(filter(None, raw_desc))

        return cleaned_desc

    @staticmethod
    def _combine_address(point:dict) -> str:
        """
        Helper function to combine the address of the point
        :param: point: a dict containing data about a single point
        :return: address_combined: address string combined from line 1 and line 2
        """
        address_1 = point.get('address', {})['line1']
        address_2 = point.get('address', {})['line2']

        address_combined = f"{address_1}, {address_2}"

        return address_combined

    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """Converts minutes from midnight (e.g., 650) to HH:MM format (e.g.,09:00"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"


    @staticmethod
    def _parse_schedule(point:dict) -> str:
        """
        Helper function to parse the schedule data when opening_hours isn't accurate
        :param: point: a dict containing data about a single point
        :return:
        """
        opening_hours = point.get('opening_hours', {})
        location_247 = point.get('location_247', False)

        if not opening_hours:
            if location_247:
                opening_hours = "24/7"
            else:

                hours_ext = point.get('opening_hours_extended', {})
                customer_hours = hours_ext.get('customer', {})

                def get_hours(day:str) -> str:
                    shifts = customer_hours.get(day, [])
                    if not shifts:
                        return "Closed"

                    start = Locker._minutes_to_time(shifts[0].get('start', 0))
                    end = Locker._minutes_to_time(shifts[0].get('end', 0))
                    return f"{start}-{end}"

                weekday_hours = get_hours('monday')
                weekend_hours = get_hours('saturday')

                opening_hours = f"MON-FRI: {weekday_hours}\nSAT-SUN: {weekend_hours}"

        return opening_hours