import requests
import json

api_token = 'd237aa2c7c5a4cb450dc342f4b6390bac4d01232170f35df911be7fa70376cfc'
api_url_base = 'https://api.digitalocean.com/v2/'

headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {api_token}'}


def get_account_info():
    api_url = '{0}account'.format(api_url_base)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        res1 = json.loads(response.content.decode('utf-8'))
        return res1
    else:
        return None


def get_all_server():
    api_url = 'https://api.digitalocean.com/v2/droplets'
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        res1 = json.loads(response.content.decode('utf-8'))
        print(res1)
        return res1
    else:
        return None


def create_server():
    ssh_key = "27:10:ac:5c:8a:61:0e:7a:36:46:c6:25:88:a0:1f:6f"
    data = {
        "name": "test4",
        "region": "nyc1",
        "size": "s-1vcpu-1gb",
        "image": "CentOS-7-x64",
        "ssh_keys": [ssh_key],
        "backups": False,
        "ipv6": False,
        "user_data": None,
        "private_networking": None,
        "volumes": None,
        "tags": ["web"]
        }
    response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, json=data)

    print(response.status_code)
    print(response.text)


def get_all_images():
    params = (
        ('page', '1'),
        ('per_page', '1'),
    )

    response = requests.get('https://api.digitalocean.com/v2/images', headers=headers, params=params)
    # print(response.status_code)
    print(response.text)




if __name__ == '__main__':
    # get_all_images()

    create_server()
