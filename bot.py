import requests
import os
import re
from pprint import pprint


#
# Calls the darksky api
#
# Global function that calls the specified endpoint
# and passes the specified query. The API key is required and is
# captured from the DARKSKY_API environment variable.
#
# @param String endpoint Valid Darksky API endpoint
# @param String query What to send to the endpoint
# @returns Dict, List or False
#
def darksky_api(endpoint, query=False):
    api_key = os.environ["DARKSKY_API"]

    if query == False:
        raise Exception("You must provide lat and lng")

    url = f"https://api.darksky.net/{endpoint}/{api_key}/{query}"

    r = requests.get(url)

    if r.status_code in [200, 301, 302, 304]:
        return r.json()
    else:
        pprint(r)
        return False


#
# Calls the geocodio api
#
# Global function that calls the specified endpoint
# and passes the specified query. The API key is required and is
# captured from the GEOCODIO_API environment variable.
#
# @param String endpoint Valid Geocodio API endpoint
# @param String query What to send to the endpoint
# @returns Dict, List or False
#
def geocode_api(endpoint, query=False):
    api_key = os.environ["GEOCODIO_API"]

    url = f"https://api.geocod.io/v1.3/{endpoint}?api_key={api_key}"

    if(query != False):
        url += f"&q={query}"

    r = requests.get(url)

    if r.status_code in [200, 301, 302, 304]:
        return r.json()
    else:
        pprint(r)
        return False


#
# Geocodes the provided location to lat, lng for Dark Sky's API
#
# @param String loc What to send to the endpoint (city, state or ZIP)
# @returns Dict
#
def get_location(loc):
    r = geocode_api("geocode", loc)

    if r != False:
        return r["results"][0]
    else:
        raise Exception("That location could not be found")


#
# Get the current conditions for the location
#
# @param Integer|String id Accuweather location key
# @returns Dict or False
#
def get_current_conditions(loc):
    if loc == False:
        return False

    endpoint = f"forecast"
    conditions = darksky_api(endpoint, f"{loc['lat']}, {loc['lng']}")
    return conditions


#
# Builds the dict of data for the location provided
#
# @param Integer|String id City, state
# @returns Dict or Error
#
def build_data(loc):
    try:
        location = get_location(loc)
        data = {
            "location": location,
            "current": get_current_conditions(location["location"]),
        }

        return data
    except:
        print("Something went wrong. Please check that you've provided a valid location")


#
# Forms a conversational response to requests for weather details
#
# @param Dict dict returns from build_data
# @returns String
#
def build_response(data):
    # wx_adjective = build_wx_adjectives(data["current"][0]["WeatherText"])
    response = f'Right now, in {data["location"]["address_components"]["city"]}, {data["location"]["address_components"]["state"]}, it is {data["current"]["currently"]["summary"].lower()} and feels like {round(int(data["current"]["currently"]["apparentTemperature"]))} degrees. You can expect {data["current"]["hourly"]["summary"].lower()}'
    return response


#
# Takes common weather conditions and returns them in their adjective form
#
# @param String wx weather condition
# @returns String
#
def build_wx_adjectives(wx):
    map = {
        "Rain": "Rainy",
        "Snow": "Snowy"
    }

    if wx in map:
        return map["wx"]
    else:
        return wx


data = build_data("10025")
response = build_response(data)

print(response)
