


import socket
clinet =socket.socket()
clinet.connect(("3.101.129.40",9000))
#循环输入

msg = "207.246.80.128"
clinet.send(msg.encode("utf-8"))
print(type(msg.encode("utf-8")))
data = clinet.recv(1024)
print(data.decode("utf-8"))
clinet.close()