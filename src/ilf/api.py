from dataclasses import dataclass
import requests
#define the base url as a variable - gives the possibility
#to change it later

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

class InPostFetcher:
    """Handles communication with inpost api, and the data extraction from
    the api response"""
    BASE_URL = 'https://api-global-points.easypack24.net/v1/points'

    def get_lockers(self, city:str) -> list[Locker]:
        """
        Return the list of all lockers for a given city
        :param city: A string containg the city name
        :return: a list containing all lockers assigned to the city
        """
        params = {
            'city': city,
            'status': 'Operating'
        }
        #define the parameters of the api call
        response = requests.get(self.BASE_URL, params=params)
        #assign the reply from the api to the variable 'response'
        response.raise_for_status()
        #stop the program when the response in ['404', '500'] and raise exception
        data = response.json()
        #convert the json string into a python dict
        points = data.get('items', [])
        #return everything inside the 'items' key from the data dict.
        #If the 'items' key missing/empty, return empty list
        return [
            Locker(
                name=point['name'],
                status=point['status'],
                location_247=point['location_247'],
                opening_hours=point['opening_hours'],
                easy_access_zone=point['easy_access_zone'],
                location_description=point['location_description'],
                location_description_1=point['location_description_1'],
                location_description_2=point['location_description_2'],
                address_line1=point.get('address', {})['line1'],
                address_line2=point.get('address', {})['line2'],
                address_details_city=point.get('address_details', {})['city'],
                address_details_post_code=point.get('address_details', {})['post_code'],
            )
            for point in points
        ]