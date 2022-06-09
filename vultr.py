import requests
import json

api_token = 'HAPGVVPV33HBOOW4KFLSR3QF44BP7BHQLSLQ'
api_url_base = 'https://api.vultr.com'

headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {api_token}'}


def account():
    api_url = f'{api_url_base}/v2/account'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        res1 = json.loads(response.content.decode('utf-8'))
        print(res1)
        return res1
    else:
        return None


def get_server():
    api_url = f'{api_url_base}/v2/instances'
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        res1 = json.loads(response.content.decode('utf-8'))
        print(res1)
        return res1
    else:
        return None


def delete_server(instance_id):
    api_url = f'{api_url_base}/v2/instances/{instance_id}'
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def create_instance(region, plan, label, snapshot_id):
    datas = {
        "region": region,
        "plan": plan,
        "label": label,
        "backups": "disabled",
        "hostname": "",
        "snapshot_id": snapshot_id
    }
    api_url = f'{api_url_base}/v2/instances'
    response = requests.post(api_url, headers=headers, json=datas)
    if response.status_code == 202:
        data = json.loads(response.text)
        return data.get("instance", "")
    else:
        print(f"创建实例失败：{response.text}")
        return None


def get_instance(instance_id):
    # id = "e266d305-fe6f-40f3-9970-6e79e61e8a34"
    api_url = f'{api_url_base}/v2/instances/{instance_id}'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        instance_data = json.loads(response.text)
        return instance_data.get("instance", "")
    else:
        return None


def get_region():
    url = "https://api.vultr.com/v2/regions"

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.text)


def get_plan():
    """
        获取实例配置列表
    :return:
    """
    api_url = f'{api_url_base}/v2/plans'
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        res1 = json.loads(response.content.decode('utf-8'))
        print(res1)
        return res1
    else:
        return None


if __name__ == '__main__':
    # region = "ewr"
    # plan = "vc2-1c-1gb"
    # label = "Example Instance"
    # snapshot_id = "a902d5a8-fc43-4297-9998-00d970ecb917"
    #
    # create_instance(region, plan, label, snapshot_id)

    get_plan()
    # get_region()