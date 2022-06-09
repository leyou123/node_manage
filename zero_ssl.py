import requests
import json

base_url = "https://api.zerossl.com"
access_key = "b5c20276a0793eef06cfa416128be112"
key_url = "https://csrgenerator.com/generate"
file_path = "/root/node_manage/temp"


class Certificates(object):

    @classmethod
    def list_all(cls):
        """
            获取所有证书
        :return:
        """

        url = f"{base_url}/certificates"
        certificate_status = "issued"
        search = ""
        limit = "100"
        page = "1"

        payload = {
            'access_key': access_key,
            'certificate_status': certificate_status,
            'search': search,
            'limit': limit,
            'page': page,

        }

        response = requests.get(url, params=payload)

        print(response.status_code)
        print(response.text)

    @classmethod
    def get_info(cls, cert_id):
        """
        获取证书信息
        :param cert_id:
        :return:
        """

        url = f"{base_url}/certificates/{cert_id}"
        payload = {
            'access_key': access_key,
            'id': cert_id,
        }

        response = requests.get(url, params=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return ""

    @classmethod
    def create(cls, do_main):
        """
        创建证书
        liunx 下生成
        openssl req -nodes -newkey rsa:2048 -sha256 -keyout private.key -out example.csr
        :param cert_id:
        :return:
        """

        csr = """
                -----BEGIN CERTIFICATE REQUEST-----
        MIICrTCCAZUCAQAwUTELMAkGA1UEBhMCQ04xETAPBgNVBAgMCHNoYW5naGFpMREw
        DwYDVQQHDAhzaGFuZ2hhaTEcMBoGA1UECgwTRGVmYXVsdCBDb21wYW55IEx0ZDCC
        ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALR1pqa8ONNg03axt9EXWe4r
        OkYoKHJWJBe+2a6WCEOXlpUjAWZekASdUOzi+Zwzcnh3k9Um4Yb6Y8QTgeQILIvE
        KymnzRxlqtJ0RKvxUjUELtGJu5hG/OSX4oDgA0n434xrtrAFWoXyUfwKq9JEncro
        zMAnZ4TY8MXSkD5KDkcPoS4ufTonlmcp+e50Lmb+ipwJ7otuyCyatgTQgjjuw8+a
        EEX4axq+oNepXNTWRyoCe+fWN02RJ9C0HQImUvR/8XMsuP7oWOK50Vx+VPYjQ1yK
        hj9TbfgHvpqBaHaxwQCPrnxZ6ffzCndWSnH41KCotzzoHSZyLSl+G+L55lD6x00C
        AwEAAaAXMBUGCSqGSIb3DQEJBzEIDAYxMjM0NTYwDQYJKoZIhvcNAQELBQADggEB
        AFClGwElYACqgT8W/nGe5Bk7RB9th5j3hHCEPB6YcrOYULjxAOjoso+KhIZOrlpU
        Fpc5jEupxk7wHt48OqXP1W7NmM/HKWpyr1fom1H6C+iVl/hFYGDPq5dnl2P08he9
        yHLVdWejHXmgUJv3OBxbCo+QjNowyOjhQaok45bGXRaM/AP65UGndQLtiUoVyBA5
        Kso0h34gADSs61zPpbLL5S8iOWgM/fKnokaMQ7r54IjDIeYuu1gUrM+jUdUjbdwU
        Ead3WC6l2QaU5ofqW4IlNsFhLBqqs7BGEYfT6yRMgD1SL/5veBJ0pAYH2kPOzxo2
        9NE+YDxZA2zmPJ6SmGYdFLM=
        -----END CERTIFICATE REQUEST-----
        """

        url = f"{base_url}/certificates"
        # do_main = 'tj1002.9527.click'
        payload = {
            'access_key': access_key
        }

        datas = {
            'certificate_domains': do_main,
            'certificate_csr': csr
        }
        response = requests.post(url, params=payload, data=datas)

        if response.status_code == 200:
            cert_data = json.loads(response.text)
            id = cert_data.get("id", "")
            common_name = cert_data.get("common_name", "")
            cname_validation_p1 = cert_data["validation"]["other_methods"][common_name].get("cname_validation_p1", "")
            cname_validation_p2 = cert_data["validation"]["other_methods"][common_name].get("cname_validation_p2", "")

            data = {
                "id": id,
                "cname_validation_p1": cname_validation_p1,
                "cname_validation_p2": cname_validation_p2
            }

            return data
        else:
            return {}

        # print(response.status_code)
        # print(response.text)

    @classmethod
    def cancel(cls, cert_id):
        """
        取消证书  请注意，只有具有状态draft或pending_validation可以取消的证书。

        :param cert_id:
        :return:
        """
        url = f"{base_url}/certificates/{cert_id}/cancel"
        payload = {
            'access_key': access_key,
            'id': cert_id,
        }

        response = requests.post(url, params=payload)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return ""

    @classmethod
    def revoke_cert(cls, cert_id):
        """
        吊销证书
        请务必小心使用此端点，并且只吊销您真正想要吊销的证书。只有具有状态的证书issued才能被吊销。如果证书已被成功吊销，您仍然会收到成功响应。
        :param cert_id:
        :return:
        """

        url = f"{base_url}/certificates/{cert_id}/revoke"
        payload = {
            'access_key': access_key,
            'id': cert_id,
        }
        response = requests.post(url, params=payload)

        print(response.status_code)
        print(response.text)

    @classmethod
    def verify_domain(cls, cert_id):
        """
        验证域名
        :param cert_id:
        :return:
        """

        url = f"{base_url}/certificates/{cert_id}/challenges"
        payload = {
            'access_key': access_key,
            'id': cert_id,
            "validation_method": "CNAME_CSR_HASH"
        }
        response = requests.post(url, params=payload)
        data = {}
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return data

    @classmethod
    def verify_domain_status(cls, cert_id):
        """
            验证证书 状态
        :param cert_id:
        :return:
        """

        url = f"{base_url}/certificates/{cert_id}/challenges"
        payload = {
            'access_key': access_key
        }
        datas = {
            "validation_method": "CNAME_CSR_HASH"
        }
        response = requests.post(url, params=payload, data=datas)

        if response.status_code == 200:
            data = json.loads(response.text)
            status = data.get("success", True)
            if status:
                print(f"{cert_id}验证成功：{data}")
                return True
            else:
                print(f"{cert_id}验证失败：{data}")
                return False
        else:
            return False

    @classmethod
    def cert_dowload(cls, cert_id, file_name):
        """
        证书下载
        :param cert_id:
        :return:
        """
        url = f"{base_url}/certificates/{cert_id}/download"
        payload = {
            'access_key': access_key,
        }

        response = requests.get(url, params=payload)

        cert_path = f'{file_path}/{file_name}.zip'

        if response.status_code == 200:
            error = ""
            try:
                datas = json.loads(response.text)
                error = datas["error"].get("type", "")
            except Exception as e:
                print(e)
            if error == "certificate_not_issued":
                return None

            with open(cert_path, 'ab') as f:
                f.write(response.content)
                f.flush()
            return cert_path
        else:
            return None


if __name__ == '__main__':
    # cert_id = "85f826bc918ca23781834034d1a2a5a4"

    id = "669eaf865a49ac3f18effc01273a8c24"
    # Certificates.create()
    # Certificates.verify_domain_status(id)
    # Certificates.list_all()
    # Certificates.delete_cert(id)
    # file_name = "tj4353.9527.click"
    # res = Certificates.cert_dowload(cert_id,file_name)
    # print(res)

    res = Certificates.get_info(id)
    print(res)
