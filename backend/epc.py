import os
from dotenv import load_dotenv
import requests

load_dotenv()

PAGE_SIZE = 5000
BASE_URL = 'https://api.get-energy-performance-data.communities.gov.uk'

def get_epc_for_council(council_name):
    token = os.getenv('EPC_BEARER_TOKEN')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    url = f'{BASE_URL}/api/domestic/search'
    results = []
    current_page = 1

    while True:
        params = {
            'council[]': council_name,
            'page_size': PAGE_SIZE,
            'current_page': current_page,
        }

        r = requests.get(url, headers=headers, params=params)

        if r.status_code == 404:
            break

        if r.status_code != 200:
            print(f'EPC API error {r.status_code}: {r.text[:300]}')
            break

        body = r.json()
        rows = body.get('data', [])

        for row in rows:
            address_parts = filter(None, [
                row.get('addressLine1'),
                row.get('addressLine2'),
                row.get('addressLine3'),
                row.get('addressLine4'),
            ])
            results.append({
                'address': ', '.join(address_parts),
                'postcode': row.get('postcode'),
                'energy_rating': row.get('currentEnergyEfficiencyBand'),
                'certificate_number': row.get('certificateNumber'),
            })

        pagination = body.get('pagination', {})
        if current_page >= pagination.get('totalPages', 1):
            break

        current_page += 1

    return results


def get_epc_for_postcode(postcode, house_number=None):
    token = os.getenv('EPC_BEARER_TOKEN')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    url = f'{BASE_URL}/api/domestic/search'
    results = []
    current_page = 1

    while True:
        params = {
            'postcode': postcode,
            'page_size': PAGE_SIZE,
            'current_page': current_page,
        }

        r = requests.get(url, headers=headers, params=params)

        if r.status_code == 404:
            break

        if r.status_code != 200:
            print(f'EPC API error {r.status_code}: {r.text[:300]}')
            break

        body = r.json()
        rows = body.get('data', [])

        for row in rows:
            address_parts = filter(None, [
                row.get('addressLine1'),
                row.get('addressLine2'),
                row.get('addressLine3'),
                row.get('addressLine4'),
            ])
            results.append({
                'address': ', '.join(address_parts),
                'postcode': row.get('postcode'),
                'energy_rating': row.get('currentEnergyEfficiencyBand'),
                'certificate_number': row.get('certificateNumber'),
            })

        pagination = body.get('pagination', {})
        if current_page >= pagination.get('totalPages', 1):
            break

        current_page += 1

    # --- everything below runs AFTER the loop has finished ---

    if house_number:
        house_number = str(house_number).lower()
        matches = []

        for r in results:
            address = r['address'].lower()

            if address.startswith(house_number + " ") or address.startswith(house_number + ","):
                matches.append(r)
            elif (", " + house_number + " ") in address or (", " + house_number + ",") in address:
                matches.append(r)

        results = matches

    return results

if __name__ == '__main__':
    broadland = get_epc_for_postcode('nr103pl', '165')
    print(broadland)












