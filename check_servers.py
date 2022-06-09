import socket
import re
import requests
import paramiko

username = "root"
password = "Leyou2020"
port = 22


class Servers(object):
    """
        检测服务
    """

    @classmethod
    def exec_cmd(cls, ip):
        try:
            cmds = "ls"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmds)
            results = stdout.readlines()

            if len(results) > 0:
                return True
            else:
                return False
        except Exception as e:
            # print(e)
            print("服务器无法连接")
            return False
        finally:
            client.close()

    @classmethod
    def get_host_ip(cls):
        """
        查询本机ip地址
        :return:
        """
        response = requests.get("http://txt.go.sohu.com/ip/soip")
        ip = ""
        if response.status_code == 200:
            content = response.text
            ip = re.findall(r'\d+.\d+.\d+.\d+', content)
            print(f"本机公网：{ip[0]}")
            return ip
        return ip

    @classmethod
    def start_socket(cls):
        server = socket.socket()
        ip = cls.get_host_ip()
        if not ip:
            print("无法获取到ip")
            return

        server.bind(("0.0.0.0", 9000))
        server.listen()
        # 连接循环 可以不断接受新连接
        while True:
            clinet, addr = server.accept()
            # 通讯循环 可以不断的收发数据
            while True:
                try:
                    # 如果是windows 对方强行关闭连接 会抛出异常
                    # 如果是linux 不会抛出异常 会死循环收到空的数据包
                    data = clinet.recv(1024)
                    if not data:
                        clinet.close()
                        break
                    host = data.decode("utf-8")
                    ping_result = "no"
                    status = Servers.exec_cmd(host)
                    if status:
                        ping_result = "yes"
                    clinet.send(ping_result.encode("utf-8"))

                except ConnectionResetError:
                    print("关闭了客户端连接")
                    clinet.close()
                    break
        cliner.close()
        server.close()


if __name__ == '__main__':
    """
        1.开放9000端口
        2.启动服务
          nohup python3 check_servers.py  > /root/check_servers_log.txt 2>&1 &
    """
    Servers.start_socket()