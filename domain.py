import requests
import json

base_url = "https://api.name.com"
username = "huangzugang"
token = "2da3aa15a099209056c90543cb9e5b62e3fcfa5a"
my_domain = "9527.click"

class Domain(object):

    @classmethod
    def get_all(cls):
        url = f"{base_url}/v4/domains"
        response = requests.get(url, auth=(username, token))
        json_data = {}
        if response.status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            return json_data

    @classmethod
    def records_all(cls):
        """
            创建域名
        :param host: 域名头
        :param domain: 域名
        :param ip: 地址
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }
        url = f"{base_url}/v4/domains/{my_domain}/records"
        response = requests.get(url, headers=headers, auth=(username, token))

        if response.status_code == 200:
            json_data = json.loads(response.text)
            records = json_data.get("records")

            all_record = []
            for record in records:
                host = record.get("host", "")
                domainName = record.get("domainName", "")
                temp_domain = f"{host}.{domainName}"
                all_record.append(temp_domain)
            return all_record
        else:
            return []

    @classmethod
    def create_records(cls, host, ip):
        """
            创建域名
        :param host: 域名头
        :param domain: 域名
        :param ip: 地址
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "host": host,
            "type": "A",
            "answer": ip,
            "ttl": 300
        }
        url = f"{base_url}/v4/domains/{my_domain}/records"
        response = requests.post(url, headers=headers, json=data,
                                 auth=(username, token))

        datas = {}
        if response.status_code == 200:
            json_data = json.loads(response.text)
            datas["id"] = json_data.get("id")
            return datas
        else:
            return datas

    @classmethod
    def delete_records(cls, records_id, domain):
        """
            删除域名
        :param records_id:
        :param domain:
        :return:
        """
        url = f"{base_url}/v4/domains/{domain}/records/{records_id}"
        response = requests.delete(url, auth=(username, token))

        if response.status_code == 200:
            return True
        else:
            return False

    @classmethod
    def update_records(cls, host, domain, ip):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "host": host,
            "type": "A",
            "answer": ip,
            "ttl": 300
        }
        url = f"{base_url}/v4/domains/{domain}/records"
        response = requests.put(url, headers=headers, json=data, auth=(username, token))
        datas = {}
        if response.status_code == 200:
            json_data = json.loads(response.text)
            datas["id"] = json_data.get("id")
            return datas
        else:
            return datas

    @classmethod
    def create_records_cname(cls, cname_validation_p1, cname_validation_p2):
        """
            创建域名验证
        :param host: 域名头
        :param domain: 域名
        :param ip: 地址
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "host": cname_validation_p1,
            "type": "CNAME",
            "answer": cname_validation_p2,
            "ttl": 3600
        }
        url = f"{base_url}/v4/domains/{my_domain}/records"
        response = requests.post(url, headers=headers, json=data,
                                 auth=(username, token))
        datas = {}
        # print(response.text)
        # print(response.status_code)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            datas["id"] = json_data.get("id")
            return datas
        else:
            Domain.delete_set_records_cname(cname_validation_p1)
            return datas

    @classmethod
    def delete_set_records_cname(cls, fqdn_v1):
        print(f"清除Canme：{fqdn_v1}")
        headers = {
            'Content-Type': 'application/json',
        }
        url = f"{base_url}/v4/domains/{my_domain}/records"
        response = requests.get(url, headers=headers, auth=(username, token))

        if response.status_code == 200:
            json_data = json.loads(response.text)
            datas = json_data.get("records")

            for data in datas:
                fqdn_v2 = data.get("fqdn", "")
                records_id = data.get("id", "")
                if fqdn_v1 in fqdn_v2:
                    url = f"{base_url}/v4/domains/{my_domain}/records/{records_id}"
                    response = requests.delete(url, auth=(username, token))
                    if response.status_code == 200:
                        print(f"Cname成功删除{records_id}:{fqdn_v2}")
                        return True
                    else:
                        return False

    @classmethod
    def del_records_all(cls):
        """
            清空不在服务器内域名
        :param host: 域名头
        :param domain: 域名
        :param ip: 地址
        :return:
        """
        headers = {
            'Content-Type': 'application/json',
        }
        url = f"{base_url}/v4/domains/{my_domain}/records"
        response = requests.get(url, headers=headers, auth=(username, token))

        if response.status_code == 200:
            json_data = json.loads(response.text)
            records = json_data.get("records")

            all_record = []
            for record in records:
                temp_dict = {}
                id = record.get("id", "")
                host = record.get("host", "")
                domainName = record.get("domainName", "")
                temp_domain = f"{host}.{domainName}"
                temp_dict[temp_domain]= id
                all_record.append(temp_dict)
            return all_record
        else:
            return []


if __name__ == '__main__':
    # host = "tj1001"
    # my_domain = "9527.click"
    # ip = "3.101.129.40"
    #
    # records_id = "208972677"
    #
    # domain = Domain()
    # domain.delete_records(records_id, my_domain)

    # domain.create_records(host, my_domain, ip)
    #
    # domain.update_records(host, my_domain, ip)
    #
    # host = f"_bbbb798573aac3fe345527379273"
    # answer = "3aaaafb0cbc5974996fa16fb8c050721.80cc3ff761f2bae30a96bb2b40eaf937.6cf0f6a09c1bfc3.comodoca.com"
    # # my_domain = "9527.click"
    #
    # Domain.create_records_cname(host, answer)
    # Domain.records_all()

    # Domain.delete_set_records_cname()

    datas = Domain.del_records_all()

    del_domain = []
    for i in range(1000):
        temp_str = f"tj{i+1}.9527.click"
        del_domain.append(temp_str)
    print(del_domain)

    for data in datas:
        for k,v in data.items():
            if k in del_domain:
                records_id = v
                url = f"{base_url}/v4/domains/{my_domain}/records/{records_id}"
                response = requests.delete(url, auth=(username, token))
                if response.status_code == 200:
                    print(f"Cname成功删除{records_id}:{k}")

