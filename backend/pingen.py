from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

pingen_url = "https://api.pingen.com"
pingen_staging_url = "https://api-staging.pingen.com"
YOUR_ORGANISATION_UUID = "b8ed873a-6cd6-4b0c-b357-e7620579a36f"

url_file_upload = f'https://api-staging.pingen.com/file-upload'
url_letters = f"https://api-staging.pingen.com/organisations/{YOUR_ORGANISATION_UUID}/letters"

client_id = os.getenv("PINGEN_CLIENT_ID")
client_secret = os.getenv("PINGEN_CLIENT_SECRET")

#Get Access token which is needed

def getAccessToken():
    url = f"{pingen_staging_url}/auth/access-tokens"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, json= data)
    return response.json().get('access_token')




def create_letter():
    access_token = getAccessToken()
    response = requests.get(url_file_upload, headers = {
        'Authorization': 'Bearer {}'.format(access_token),
    })

    data = response.json()['data']
    file_url = data['attributes']['url']
    file_url_signature = data['attributes']['url_signature']

    file = open('test_letter.pdf', 'rb')
    requests.put(file_url, data=file)
    file.close()

    payload = {
        'data': {
            'type': 'letters',
            'attributes': {
                'file_original_name': 'test_letter.pdf',
                'file_url': file_url,
                'file_url_signature': file_url_signature,
                'address_position': 'left',
                'auto_send': False
            }
        }
    }
    result = requests.post(
        url_letters,
        json = payload,
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
    return result.json()




def post_letter():

    letter_id = create_letter()['data']['id']
    print("letter_id:", letter_id)
    url = f"https://api-staging.pingen.com/organisations/{YOUR_ORGANISATION_UUID}/letters/{letter_id}/send"
    access_token = getAccessToken()

    payload = {
        'data': {
            'id': letter_id,
            'type': 'letters',
            'attributes': {
                'delivery_product': 'fast',
                'print_mode': 'simplex',
                'print_spectrum': 'color'
            }
        }
    }

    time.sleep(5)
    post = requests.patch(
        url,
        json = payload,
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(access_token)
        })
    print("send status:", post.status_code)
    print("send response:", post.json())
    return post


post_letter()