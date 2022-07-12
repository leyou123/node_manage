import time
import json
import requests
from dingding import DataLoggerAPI

base_url = "https://nodes.9527.click"
username = "getnodes"
password = "TxPo4gNO3FpEiWYT9bgp"
URL_DL_ADMIN = "https://agri-dl.holdingbyte.com"


class Servers(object):

    def get_now_time(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_node_all(self):
        datas = {
            "username": username,
            "password": password
        }
        url = f"{base_url}/get_all_node"
        response = requests.post(url, data=datas)
        return json.loads(response.text)

    def check_status(self, datas):
        number_count = 0
        country_count = 0
        for k, v in datas.items():
            status = datas[k]["connect"]
            if status == "open":
                number_count += 1
            country_count += 1
        return number_count, country_count

    def check_flow(self, total_flow, already_flow, tag):
        """
        判断流量是否超过了 95%
        :param total_flow:
        :param already_flow:
        :return:
        """
        max_flow = 0.95
        if not total_flow or not already_flow:
            return False
        res = round(float(already_flow) / float(total_flow), 2)
        # print(total_flow,already_flow,res)
        if res > max_flow:
            return True
        # elif str(tag) == "-999":
        #     return True
        else:
            return False

    def delete_node(self, instance_id):
        # url = f"http://54.177.55.54:7000/node/Node_close"
        url = f"{base_url}/node/Node_close"
        data = {
            "instance_id": instance_id
        }
        res = requests.post(url=url, json=data)
        # print(res.status_code)
        # print(res.text)

    def update_node(self, node_id):
        # url = f"http://54.177.55.54:7000/node/Node_update"
        url = f"{base_url}/node/Node_update"
        data = {
            "node_id": node_id,
            "type": "update"
        }
        res = requests.post(url=url, json=data)
        print(res.status_code)
        print(res.text)

    def clear_data(self):
        node_datas = self.get_node_all()
        max_number = 3
        datas = node_datas.get("nodes", "")
        dingding_api = DataLoggerAPI("6543720081", "1mtv8ux938ykgw030vi2tuc3yc201ikr")

        for data in datas:
            instance_id = data.get("instance_id", "")
            total_flow = data.get("total_flow", 0)
            already_flow = data.get("already_flow", 0)
            tag = data.get("tag", 0)
            name = data.get("name", "")
            host = data.get("host", "")
            node_id = data.get("id", "")
            check_reulst = self.check_flow(total_flow, already_flow, tag)

            if check_reulst:
                print(f"{host}流量超过95%")
                # self.delete_node(instance_id)
                self.update_node(node_id)
                continue
            if str(tag) == "-999":
                self.delete_node(instance_id)

            instance_id = data.get("instance_id", "")
            ip = data.get("ip", "")
            if not instance_id:
                continue
            connect_data = data.get("connect_data", "")

            if connect_data:
                json_connect_data = json.loads(connect_data)
                open_count, country = self.check_status(json_connect_data)
                if country >= max_number:
                    if open_count == 0:
                        print(f"清除:{instance_id},ip:{ip},连接数：{open_count},国家数：{country}")
                        self.delete_node(instance_id)

                        # url = f"{base_url}/node/clear_servers"
                        # send_data = {
                        #     "instance_id": instance_id
                        # }
                        # reponse = requests.post(url=url, json=send_data)
                        # if reponse.status_code == 200:
                        #     print(f"清除:{instance_id},ip:{ip},连接数：{open_count},国家数：{country}")
                        #
                        #     now_time = self.get_now_time()
                        #     message = f"{now_time} \r\n" \
                        #               f"服务器{name} \r\n" \
                        #               f"域名:{host} \r\n" \
                        #               f"状态:关闭  \r\n" \
                        #               f"无法连接"
                        #     dingding_api.dd_send_message(message, "vpnoperator")
                    else:
                        print(f"服务正常:{instance_id},ip:{ip},连接数：{open_count},国家数：{country}")

            else:
                print(f"国家缺少:{instance_id},ip:{ip}")


if __name__ == '__main__':
    while True:
        try:

            servers = Servers()
            servers.clear_data()
            print("等待2分钟")
        except Exception as e:
            print(e)
        time.sleep(60 * 2)
