# import paramiko
#
# private_key = paramiko.RSAKey.from_private_key_file("/root/node_manage/id_rsa", password='123456')
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect(hostname="147.182.171.221", port=22, username="root", pkey=private_key)
#
# # stdin, stdout, stderr = ssh.exec_command("ifconfig")
# #
# # result = stdout.read()
# #
# # print(result.decode())
#
#
# stdin1, stdout1, stderr1 = ssh.exec_command("yum")
#
# result1 = stdout1.read()
#
# print(result1)
#
# ssh.close()
#

import paramiko
import time
private_key = paramiko.RSAKey.from_private_key_file("/root/node_manage/id_rsa", password='123456')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="206.189.205.148", port=22, username="root", pkey=private_key)

channel = ssh.get_transport().open_session()

channel.get_pty()
channel.invoke_shell()


cmd1 = f"yum -y install wget;wget -N --no-check-certificate -q https://cdn.jsdelivr.net/gh/h31105/trojan_v2_docker_onekey/deploy.sh && \
chmod +x deploy.sh && bash deploy.sh"
# command = "/root/tcpx.sh"
channel.send(cmd1 + "\n")

while True:
    if channel.recv_ready():
        output = channel.recv(1024).decode('utf-8')
        print(output)
        if "请输入数字" in output:
            channel.send("1" + "\n")
            time.sleep(3)

        if "请输入TLS端口" in output:
            channel.send("443" + "\n")
            time.sleep(3)


        if "请输入你的域名信息" in output:
            channel.send("443" + "\n")
            time.sleep(3)


    else:
        time.sleep(0.5)
        if not(channel.recv_ready()):
            break


ssh.close()


# stdin, stdout, stderr = ssh.exec_command("ifconfig")
#
# result = stdout.read()
#
# print(result.decode())


