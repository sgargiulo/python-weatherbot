import requests
import os


#
# Calls the accuweather api
#
# Global function that calls the specified endpoint
# and passes the specified query. The API key is required and is
# captured from the ACCUWEATHER_KEY environment variable.
#
# @param String endpoint Valid Accuweather API endpoint
# @param String query What to send to the endpoint
# @returns Dict, List or False
#
def accuweather_api(endpoint, query=False):
    api_key = os.environ["ACCUWEATHER_KEY"]
    url = f"https://dataservice.accuweather.com/{endpoint}?apikey={api_key}"

    if(query != False):
        url += f"&q={query}"

    r = requests.get(url)

    if [200, 301, 302, 304].index(r.status_code) > -1:
        return r.json()
    else:
        return False


#
# Gets the Accuweather Location ID for the city state
#
# @param String loc What to send to the endpoint
# @returns Dict or False
#
def get_location_id(loc):
    r = accuweather_api("locations/v1/search", loc)
    return r[0]


#
# Gets the Current conditions for the city state
#
# @param String loc What to send to the endpoint
# @returns Dict or False
#
def get_current_conditions(loc):
    id = get_location_id(loc)
    id = id["Key"]
    endpoint = f"currentconditions/v1/{id}"
    conditions = accuweather_api(endpoint)
    return conditions


print(get_current_conditions("Babylon, NY"))
