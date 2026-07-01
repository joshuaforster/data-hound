import requests

def get_latlon(postcode):
    r = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    result = r.json()['result']
    return result['latitude'], result['longitude']

def street_view_link(lat, lon):
    return (
        "https://www.google.com/maps/@?api=1&map_action=pano"
        f"&viewpoint={lat},{lon}"
    )

