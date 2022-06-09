from core import get_config, send_data, TestServer, UploadFile, parsing_domain_name, send_node_data, check_servers, \
    clear_servers_data
from vultr import create_instance, get_instance, delete_server
from domain import Domain, my_domain
from zero_ssl import Certificates
from check_all_server import Servers
import time
import random

domain = "https://nodes.9527.click"

"""
    1.开启服务
    2.检测是否被封
    3.指定域名
    4.生成ssl证书.放到服务器
    5.启动服务
"""


class ServerManager(object):

    def __init__(self):
        self.stop = 0
        self.running = 1
        self.start_server = 2
        self.available = 3
        self.generate_domain = 4
        self.complete_ssl = 5
        self.succeed = 6
        self.clear_ssl = 7

    def start_operator(self):
        info = {
            "run_status": self.stop
        }
        datas = get_config(info)
        if not datas:
            return

        for data in datas:
            operator = data.get("operator", "")
            config = data.get("config", "")
            name = data.get("name", "")
            snapshot = data.get("snapshot", "")
            region = data.get("region_id", "")
            id = data.get("id", "")
            print(f"{name}正在创建服务器")


            if operator == "Vultr":
                create_datas = create_instance(region, config, name, snapshot)
                if not create_datas:
                    continue
                url = f"{domain}/node/upload_config"
                instance_data = {
                    "id": id,
                    "instance_id": create_datas.get("id", ""),
                    "run_status": self.start_server,
                }
                send_data(url, instance_data)

    def check_instance_status(self):
        info = {
            "run_status": self.start_server
        }
        datas = get_config(info)
        if not datas:
            return

        for data in datas:
            name = data.get("name", "")
            operator = data.get("operator", "")
            instance_id = data.get("instance_id", "")
            id = data.get("id", "")
            print(f"{name}正在检测")
            if operator == "Vultr":
                server_data = get_instance(instance_id)
                if not server_data:
                    clear_servers_data(instance_id)
                    continue
                ip = server_data.get("main_ip", "")
                if ip == "0.0.0.0":
                    continue
                servers = TestServer.exec_cmd(ip)
                if not servers:
                    continue

                url = f"{domain}/node/upload_config"
                instance_data = {
                    "id": id,
                    "ip": ip,
                    "run_status": self.available,
                }
                send_data(url, instance_data)

                # 删除旧服务器
                old_instance_id = data.get("old_instance_id", "")
                response = delete_server(old_instance_id)
                if response:
                    clear_url = f"{domain}/node/del_servers"
                    json_data = {"instance_id": old_instance_id}
                    send_data(clear_url, json_data)

                print(f"{name}服务器检测成功")

                # test_data = check_servers(ip)
                # if test_data:
                #
                # else:
                #     # 清空服务器数据
                #     clear_servers_data(instance_id)
                #     delete_server(instance_id)
            elif operator == "Other":
                # server_data = get_instance(instance_id)
                # if not server_data:
                #     clear_servers_data(instance_id)
                #     continue
                ip = server_data.get("main_ip", "")
                if ip == "0.0.0.0":
                    continue
                servers = TestServer.exec_cmd(ip)
                if not servers:
                    continue

                url = f"{domain}/node/upload_config"
                instance_data = {
                    "id": id,
                    "ip": ip,
                    "run_status": self.available,
                }
                send_data(url, instance_data)

                # 删除旧服务器
                # old_instance_id = data.get("old_instance_id", "")
                # response = delete_server(old_instance_id)
                # if response:
                #     clear_url = f"{domain}/node/del_servers"
                #     json_data = {"instance_id": old_instance_id}
                #     send_data(clear_url, json_data)

                print(f"{name}服务器检测成功")

    def set_domain(self):
        info = {
            "run_status": self.available
        }
        datas = get_config(info)
        if not datas:
            return

        for data in datas:
            print("正在生成域名")
            domain_datas = Domain.records_all()

            id = data.get("id", "")
            ip = data.get("ip", "")

            available_domain = ""
            upload_domain = ""
            for i in range(1, 1000):
                num = random.randint(1000, 10000)
                create_domain = f"tj{num}"
                menger_domain = f"{create_domain}.{my_domain}"
                if menger_domain not in domain_datas:
                    available_domain = create_domain
                    upload_domain = menger_domain
                    break

            if not available_domain:
                return

            create_data = Domain.create_records(available_domain, ip)
            if create_data:
                domain_id = create_data.get("id")
                url = f"{domain}/node/upload_config"
                instance_data = {
                    "id": id,
                    "run_status": self.generate_domain,
                    "domain_id": domain_id,
                    "domain": upload_domain
                }
                send_data(url, instance_data)
                print("域名创建成功")

    def create_ssl(self):
        info = {
            "run_status": self.generate_domain
        }
        datas = get_config(info)
        if not datas:
            return

        for data in datas:
            print("开始创建SSL证书")
            id = data.get("id", "")
            check_do_main = data.get("domain", "")
            ip = data.get("ip", "")
            server_cert_id = data.get("cert_id", "")
            cname_validation_p1 = data.get("cname_validation_p1", "")
            cname_validation_p2 = data.get("cname_validation_p2", "")

            if not check_do_main:
                continue
            print(f"{check_do_main}开始检测域名")

            parsing_ip = parsing_domain_name(check_do_main)
            if parsing_ip != ip:
                print(f"{check_do_main}解析域名失败，等待重试")
                continue

            print(f"{check_do_main}解析域正确")
            # 创建SSL证书

            if server_cert_id:
                cret_data = Certificates.get_info(server_cert_id)
                print("==================================================")
                print(cret_data)
                print("==================================================")
                status = cret_data.get("status")

                if status == "issued":
                    print(f"{check_do_main}验证域名成功")
                    # 修改状态
                    url = f"{domain}/node/upload_config"
                    instance_data = {
                        "id": id,
                        "run_status": self.complete_ssl
                    }
                    send_data(url, instance_data)
                    print(f"{check_do_main}创建证书成功")
                    continue
            else:
                cert_data = Certificates.create(check_do_main)
                server_cert_id = cert_data.get("id", "")
                cname_validation_p1 = cert_data.get("cname_validation_p1", "")
                cname_validation_p2 = cert_data.get("cname_validation_p2", "")

                url = f"{domain}/node/upload_config"
                instance_data = {
                    "id": id,
                    "cert_id": server_cert_id,
                    "run_status": self.complete_ssl,
                    "cname_validation_p1": cname_validation_p1.lower(),
                    "cname_validation_p2": cname_validation_p2.lower()
                }
                send_data(url, instance_data)

            if not cname_validation_p1 or not cname_validation_p2 or not server_cert_id:
                print(f"{check_do_main},没发现解析值或者证书id")
                continue

            domain_header = cname_validation_p1.split('.')[0]
            # print(domain_header)
            # print(cname_validation_p2)

            # 创建Cname等待验证
            create_records_data = Domain.create_records_cname(domain_header, cname_validation_p2)
            if not create_records_data:
                # url = f"{domain}/node/upload_config"
                # instance_data = {
                #     "id": id,
                #     "run_status": self.clear_ssl
                # }
                # send_data(url, instance_data)
                print(f"{check_do_main}创建证书域名失败,删除cname")
                continue

            # 验证证书
            print(f"{check_do_main}等待30秒Cname生效")
            time.sleep(30)
            verify_cert = Certificates.verify_domain_status(server_cert_id)
            if not verify_cert:
                print(f"{check_do_main}证书验证失败")
                continue
            else:
                print(f"{check_do_main}成功等待生效60秒")
                time.sleep(60)

    def trojan_start(self, domain):
        ssl_path = "/root/ssl/"
        del_old_file = f"rm -rf /root/ssl/certificate.crt /root/ssl/ca_bundle.crt /root/ssl/fullchain.crt"

        target_path = f"{ssl_path}cert.zip"
        # 解压文件
        unzip_cmd = f"unzip {target_path} -d {ssl_path}"
        # 证书转化
        conv_cert = f"cat {ssl_path}certificate.crt {ssl_path}ca_bundle.crt > {ssl_path}fullchain.crt"
        # 修改文件
        modfiyfile_1 = f"sed -i 's/^.*sni.*/\"sni\": \"{domain}\",/g' /etc/trojan/conf/server.json"
        modfiyfile_2 = f"sed -i 's/^.*fallback_addr.*/\"fallback_addr\":\"{domain}\",/g' /etc/trojan/conf/server.json"
        modfiyfile_3 = f"sed -i 's/^.*server_name.*/server_name {domain};/g' /etc/nginx/conf/conf.d/default.conf"
        # 启动nginx
        nginx_cmd = f"systemctl restart nginx"
        # 启动trojan
        trojan_cmd = f"systemctl start trojan.service"
        # python3 cmd
        python_cmd = f"nohup python3 /root/vpn_NodeService/start.py  > /root/vpn_NodeService_log.txt 2>&1 &"
        all_cmds = f"{del_old_file};{unzip_cmd};{conv_cert};{modfiyfile_1};{modfiyfile_2};{modfiyfile_3};{nginx_cmd};{trojan_cmd};{python_cmd}"
        print(all_cmds)
        return all_cmds

    def start_servers(self):

        info = {
            "run_status": self.complete_ssl
        }
        datas = get_config(info)
        if not datas:
            return
        print("启动服务开启")
        for data in datas:
            id = data.get("id", "")
            ip = data.get("ip")
            cert_id = data.get("cert_id")
            my_domain = data.get("domain")
            print("开始上传文件")

            upload_res = self.upload_file(ip, cert_id, my_domain)
            if upload_res is False:
                continue
            print("上传文件成功")

            trojan_cmd = self.trojan_start(my_domain)

            TestServer.exec_cmd(ip, trojan_cmd)
            url = f"{domain}/node/upload_config"
            instance_data = {
                "id": id,
                "ip": ip,
                "status": 1,
                "run_status": self.succeed
            }
            send_data(url, instance_data)

            name = data.get("name", "")
            node_type = data.get("node_type", "")
            port = data.get("port", "443")
            country = data.get("country", "")
            region = data.get("region", "")
            national_flag = data.get("national_flag", "")
            node_data = {
                "name": name,
                "domain": my_domain,
                "ip": ip,
                "node_type": node_type,
                "port": port,
                "country": country,
                "region": region,
                "national_flag": national_flag
            }
            send_node_data(node_data)

            print("服务器启动成功")

    def upload_file(self, ip, server_cert_id, domain):

        # 下载证书
        dowload_path = Certificates.cert_dowload(server_cert_id, domain)

        if not dowload_path:
            print("下载证书失败")
            return False

        time.sleep(10)

        # 上传证书到服务器
        target_path = f"/root/ssl/cert.zip"
        UploadFile.start(ip, dowload_path, target_path)

        # # 上传私钥
        private_target_path = f"/root/ssl/private.key"
        private_path = f"/root/node_manage/private.key"
        UploadFile.start(ip, private_path, private_target_path)

        # # 删除本地证书
        # del_cmd = f"rm -rf {dowload_path}"
        # os.system(del_cmd)
        return True

    def start(self):
        self.start_operator()
        self.check_instance_status()
        self.set_domain()
        self.create_ssl()
        self.start_servers()


if __name__ == '__main__':
    server_manager = ServerManager()
    servers = Servers()
    while True:
        try:
            servers.clear_data()
            server_manager.start()
            print("等待2分钟")
        except Exception as e:
            print(e)
        time.sleep(60*2)
