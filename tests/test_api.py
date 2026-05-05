from unittest.mock import patch, Mock
import pytest
import requests
from ilf import ERROR_MESSAGES, ExitCode
from ilf.api import InPostFetcher,Locker
fetcher = InPostFetcher()
MOCK_RESPONSE = {
    "items": [
        {
            "name": "PIS1",
            "status": "Operating",
            "location_247":"true",
            "opening_hours": "24/7",
            "easy_access_zone": "true",
            "location_description": "Obok domu z różowym dachem",
            "location_description_1": None,
            "location_description_2": None,
            "address": {
                "line1": "ul. Kasztanowa 47b",
                "line2": "32-064 Pisary"
            },
            "address_details": {
                "city": "Pisary",
                "post_code": "32-064",
                "street": "Władysława Broniewskiego",
                "building_number": "1",
                "flat_number": 'null'
            }
        }
    ]
}

@patch("ilf.api.requests.get")
#when the function runs, find get_lockers and replace it with a dummy object
def test_get_lockers(mock_get_lockers):
    #pass the dummy object into the function as mock_get_lockers
    mock_get_lockers.return_value.status_code = 200
    #guarantee that the dummy object reports 200
    mock_get_lockers.return_value.json.return_value = MOCK_RESPONSE
    #When the code calls get_lockers dont connect to the internet, but
    #just go with MOCK_RESPONSE
    #initialize an instance of the InPostFetcher class
    result = fetcher.get_operating_lockers("Pisary")
    #act - call the real function and give it the MOCK_RESPONSE
    assert len(result) == 1
    #assert that the length of the result is 1
    assert isinstance(result[0], Locker)
    #assert that the object returned by the function is
    #an instance of the class Locker

    mock_get_lockers.assert_called_once_with(
        fetcher.BASE_URL,
        params = {
            "city": "Pisary",
            'status': InPostFetcher.statuses,
            'page': 1,
            'per_page': 1000
        }
    )
    #check whether the actual api.py built the dictionary with the string "Pisary",
    #before sending it to BASE_URL
@patch("ilf.api.requests.get")
def test_api_server_down(mock_get):
    """
    Test whether the program responds correctly when the server request returns code 500
    :param mock_get:
    :return:
    """
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        fetcher.get_operating_lockers("Kraków")

@patch("ilf.api.requests.get")
def test_api_malformed_response(mock_get):
    """Test whether the program responds correctly when the server request returns unexpected json response"""
    # Setup the mock to return weird JSON without the 'items' list
    mock_response = Mock()
    mock_response.json.return_value = {
        "weird_unexpected_key": "hello",
        "total_pages": 1
    }
    mock_get.return_value = mock_response

    lockers = fetcher.get_operating_lockers(city="Kraków")
    assert lockers == []
    assert len(lockers) == 0
