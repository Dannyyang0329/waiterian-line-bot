import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_restaurant(lat, lng, radius, min_price, keyword):
    radius      = 3000 if radius    is None else radius
    min_price   =    0 if min_price is None else min_price
    keyword     =   '' if keyword   is None or keyword == '無' else keyword

    typestr = 'type=food|restaurant&'
    if type == 'CAFE':
        typestr = 'type=cafe&'
    if type == 'DESSERT':
        keyword = 'dessert'

    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    search_url += f"key={os.getenv('GOOGLE_API_TOKEN', default='')}&"
    search_url += f"location={lat},{lng}&"
    search_url += f"minprice={min_price}&"
    search_url += f"radius={radius}&"
    search_url += typestr
    search_url += "opennow=true&"
    search_url += "language=zh-TW&"
    if len(keyword) > 0:
        search_url += f"keyword={keyword}"

    try:
        response = requests.get(search_url).json()
        return response['results']
    except Exception as e:
        print(e)
        return "ERROR"


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

# load_dotenv()
# restaurant = get_restaurant(22.993, 120.219, 3000, None, None, "RESTAURANT")
# restaurant = get_restaurant(23.308, 120.721, 5000, None, None, "RESTAURANT")
# print(restaurant)
# print()
# print()
#
# print(get_restaurant_url(restaurant))
#
# print(get_restaurant_photo(restaurant))

