import paramiko
import socket
import time
import json
import requests
from dingding import DataLoggerAPI

domain = "https://nodes.9527.click"
# domain = "http://54.177.55.54:7000"
password = "Leyou2020"
username = "root"
port = 22


def get_config(datas):
    url = f"{domain}/node/get_config"
    response = requests.post(url, json=datas)

    if response.status_code == 200:
        data = json.loads(response.text)
        config = data.get("datas", [])
        return config
    else:
        return []


def send_data(url, datas):
    response = requests.post(url, json=datas)
    if response.status_code == 200:
        return True
    else:
        return False


class TestServer(object):

    @classmethod
    def exec_cmd(cls, ip,cmds="ls"):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmds)
            results = stdout.readlines()
            return results

        except Exception as e:
            # print(e)
            print("服务器正在开启，耐心等待3-5分钟")
            return []
        finally:
            client.close()


class UploadFile(object):
    """
        上传文件
    """

    @classmethod
    def start(cls, ip, file_path, target_path):
        t = paramiko.Transport((ip, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(file_path, target_path)
        t.close()


def parsing_domain_name(domain):
    """
        解析域名
    :param domain:
    :return:
    """
    parsing_ip = ""
    try:
        parsing_ip = socket.gethostbyname(domain)
    except socket.error as e:

        print(f"{domain}解析域名异常")
    return parsing_ip


def send_node_data(datas):
    url = f"{domain}/add_node"

    response = requests.post(url, json=datas)
    if response.status_code == 200:
        return True
    else:
        return False


def check_servers(check_host):
    all_host = ["8.142.77.126", "147.139.22.212", "8.215.37.6"]
    # all_host = ["147.139.22.212"]

    all_result = []

    api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")

    for host in all_host:

        url = f"http://{host}:9000/check_servers"
        data = {
            "ip": check_host
        }
        try:
            response = requests.post(url=url, json=data)
            if response.status_code == 500:
                timeStamp = time.time()
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print(api.dd_send_message(f"时间：{otherStyleTime}，检测节点异常：{host}", "vpnoperator"))
                all_result.append(False)
                continue
            print(response.status_code)
            print(response.text)
            if response.status_code == 200:
                res_data = json.loads(response.text)
                status = res_data.get("status",False)
                all_result.append(status)
            else:
                all_result.append(False)
        except Exception as e:
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print(api.dd_send_message(f"时间：{otherStyleTime}，检测节点异常：{host}", "vpnoperator"))
            print(e)
            return False

    if False in all_result:
        return False
    else:
        return True


def clear_servers_data(instance_id):
    clear_url = f"{domain}/node/clear_servers"
    json_data = {"instance_id": instance_id}
    send_data(clear_url, json_data)


if __name__ == '__main__':
    pass
    # ip = "207.246.80.128"
    # file_path = "/root/node_manage/zero/new_sll.zip"
    # target_path = "/root/new_sll.zip"
    # UploadFile.start(ip,file_path,target_path)

    # print(parsing_domain_name())  # 打印解析完毕的ip

    res = check_servers("149.28.100.85")
    print(res)
