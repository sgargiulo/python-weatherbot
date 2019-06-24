import requests
import os
import re
from pprint import pprint
from dotenv import load_dotenv


# Load the keys from the env file
load_dotenv()


#
# Calls the darksky api
#
# Global function that calls the specified endpoint
# and passes the specified query. The API key is required and is
# captured from the DARKSKY_API environment variable.
# @returns Dict, List or False
#
def darksky_api(query=False):  # this will prevent blank calls from going to the API
    api_key = os.environ.get("DARKSKY_KEY")

    if query == False:
        raise Exception("You must provide lat and lng")

    url = f"https://api.darksky.net/forecast/{api_key}/{query}"

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
# @param String query What to send to the endpoint
# @returns Dict, List or False
#
def geocode_api(query=False):
    api_key = os.environ.get("GEOCODIO_KEY")

    url = f"https://api.geocod.io/v1.3/geocode?api_key={api_key}"

    if(query != False):
        url = f"{url}&q={query}"

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
    r = geocode_api(loc)

    if r != False:
        # The geocode API responds with the original query and a LIST of results
        # Here, we're only taking the first result, as it is the most accurate
        # https://www.geocod.io/docs/#single-address for more details
        return r["results"][0]
    else:
        # If the geocode API failed to find a lat and lng for the entered location
        # throw an error and stop the program
        raise Exception("That location could not be found")


#
# Get the current conditions for the location
#
# @param Integer|String id Accuweather location key
# @returns Dict or False
#
def get_current_conditions(loc=False):
    if loc == False:
        return False

    conditions = darksky_api(f"{loc['lat']}, {loc['lng']}")
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

    sunblock = False
    umbrella = False

    if "rain" in data["current"]["currently"]["summary"].lower():
        umbrella = True

    if data["current"]["currently"]["uvIndex"] > 5:
        sunblock = True

    for hour in data["current"]["hourly"]["data"]:
        if hour["uvIndex"] > 5:
            sunblock = True

        # needed to make the summary lower case to account for when the word rain could have capital letters
        if "rain" in hour["summary"].lower():
            umbrella = True

    if "city" in data["location"]["address_components"]:
        response = f'Right now, in {data["location"]["address_components"]["city"]}, {data["location"]["address_components"]["state"]}, it is {data["current"]["currently"]["summary"].lower()} and feels like {round(int(data["current"]["currently"]["apparentTemperature"]))} degrees. You can expect {data["current"]["hourly"]["summary"].lower()}'

        if sunblock == True:
            response = f"{response} Wear sunblock, the UV will exceed 5 in the next 24 hours."

        if umbrella == True:
            response = f"{response} There's rain in the forecast so bring an umbrella."
    else:
        response = f"Sorry, we couldn't find that location. Please make sure you entered a valid city and state or zipcode and try again"

    return response


location = input("Please enter your city and state or zip: ")

data = build_data(location)
response = build_response(data)

print(response)
