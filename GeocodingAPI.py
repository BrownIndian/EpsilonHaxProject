api_key="AIzaSyBRaXTG382Cm_hvgMzHrUy7DTEAat8Dzgg"
import requests
from urllib.parse import urlencode

data_type = 'json'
endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
params = {"address": "1600 Amphitheatre Parkway, Mountain View, CA", "key": api_key}
url_params = urlencode(params)

url = f"{endpoint}?{url_params}"
print(url)

def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

extract_lat_lng("1600 Amphitheatre Parkway, Mountain View, CA")


from urllib.parse import urlparse, parse_qsl
to_parse = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyB2nSEJAXySQN36qi2q4f6AhRUTNtTx5es&place_id=ChIJoYg9VYrAj4ARjz2XBn3XRkA"

urlparse(to_parse)

parsed_url = urlparse(to_parse)
query_string = parsed_url.query
query_string

query_tuple = parse_qsl(query_string)
print(query_tuple)

endpoint = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
print(endpoint)
