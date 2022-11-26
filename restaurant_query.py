import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_restaurant(lat, lng, radius, keyword=''):
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    search_url += f"key={os.getenv('GOOGLE_API_TOKEN', default='')}&"
    search_url += f"location={lat},{lng}&"
    search_url += f"radius={radius}&"
    search_url += "type=food|restaurant&"
    search_url += "opennow=true&"
    search_url += "language=zh-TW&"
    if len(keyword) > 0:
        search_url += f"keyword={keyword}"

    response = requests.get(search_url).json()
    return response['results']


def get_restaurant_photo(restaurant):
    if restaurant.get('photos') is None:
        return None

    photo_ref = restaurant['photos'][0]['photo_reference']
    max_width = restaurant['photos'][0]['width']
    search_url = "https://maps.googleapis.com/maps/api/place/photo?"
    search_url += f"key={os.getenv('GOOGLE_API_TOKEN', default='')}&"
    search_url += f"photoreference={photo_ref}&"
    search_url += f"maxwidth={max_width}"
    return search_url


def get_restaurant_url(restaurant):
    lat = restaurant['geometry']['location']['lat']
    lng = restaurant['geometry']['location']['lng']
    id = restaurant['place_id']
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}&query_place_id={id}"

# restaurant = get_restaurant(22.993, 120.219, 500)[0]
# print(restaurant['rating'])
# print()
# print()
#
# print(get_restaurant_url(restaurant))
#
# print(get_restaurant_photo(restaurant))

