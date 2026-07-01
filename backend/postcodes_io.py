import requests

def find_postcode(postcode):

    url = f"https://api.postcodes.io/postcodes/{postcode}"

    payload = {}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    result = response.text
    return result


def nearest_postcodes(postcode):

    url = f"https://api.postcodes.io/postcodes/{postcode}/nearest"

    payload = {}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    result = response.text
    return result

