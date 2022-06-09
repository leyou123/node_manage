import os
import sys
import json
import time
import paramiko
import requests


class Config(object):
    """
    创建p12文件
    """


    # def __init__(self):
        # self.transporter_path = ITMSTRANSPORTER_PATH
        # self.log_file = os.path.join(TEMP_FILE_PATH, "create_p12.txt")


    def start(self):
        """
        app 创建
        :param host:
        :param port:
        :param apple_name:
        :param apple_password:
        :return:
        """

        try:
            private_key = paramiko.RSAKey.from_private_key_file("/root/node_manage/id_rsa", password='123456')

            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #
            # ssh.connect(hostname="159.223.137.129", port=22, username="root", pkey=private_key)
            #
            # stdin, stdout, stderr = ssh.exec_command("ifconfig")

            HOST = "217.69.1.102"

            trans = paramiko.Transport((HOST, 22))
            trans.start_client()
            trans.auth_password(username="root", password="Leyou2020")
            # trans.auth_publickey(username="root", key=private_key)
            print("link succeed")
        except Exception as e:
            print(e)
            return {'status': 404, 'msg': "计算机连接错误或者主机用户或者密码错误"}

        channel = trans.open_session()  # 打开一个通道
        channel.settimeout(7200)
        channel.get_pty()  # 获取一个终端
        channel.invoke_shell()  # 激活器


        cmd_private = "yum"
        channel.send(cmd_private)
        time.sleep(3)
        private_res = channel.recv(1024).decode('utf-8')
        print(private_res)

        # cmd_csr = 'openssl req -new -sha256 -key {private_key} -out {csr_path}\r'.format(private_key=private_key,
        #                                                                                  csr_path=csr_path)
        # print(cmd_csr)
        channel.send(cmd_private)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        time.sleep(1)
        rst = channel.recv(1024).decode('utf-8')
        print(rst)
        # if not rst:
        #     channel.close()
        #     trans.close()
        #     return {'status': 404, 'msg': "连接超时"}

        channel.close()
        trans.close()
        return None



    # def submit_p12(self, file_path, user_name):
    #     """
    #     提交p12 文件存入oss
    #     """
    #     url = "{url}upload".format(url=URL)
    #     files = {'files': open(file_path, 'rb')}
    #     data = {"name": user_name}
    #     response = requests.post(url=url, data=data, files=files)
    #     print(response)



    def run(self, name):
        """
            app 启动
        :return:
        """
        try:
           print(11)
        except Exception as e:
            print(e)


def main():
    time.sleep(10)


if __name__ == '__main__':
    main()

    config=Config()

    config.start()