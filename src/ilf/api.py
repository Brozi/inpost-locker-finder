import requests
BASE_URL = 'https://api-global-points.easypack24.net/v1/points'
#define the base url as a variable - gives the possibility
#to change it later

def get_lockers(city:str) -> list:
    """
    Return the list of all lockers for a given city
    :param city: A string containg the city name
    :return: a list containing all lockers assigned to the city
    """
    params = {
        'city': city
    }
    #define the parameters of the api call
    response = requests.get(BASE_URL, params=params)
    #assign the reply from the api to the variable 'response'
    response.raise_for_status()
    #stop the program when the response in ['404', '500'] and raise exception
    data = response.json()
    #convert the json string into a python dict
    return data.get('items', [])
    #return everything inside the 'items' key from the data dict.
    #If the 'items' key missing/empty, return empty list