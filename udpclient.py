import socket

target_host='127.0.0.1'
target_port=80

# 与tcpclient.py里面的类似，SOCK_DGRAM代表创建的是UDP套接字
client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 由于UDP是面向无连接的，所以直接使用saendto()和recvfrom()来发送和接收数据
client.sendto('aaabbbccc', (target_host, target_port))

date, addr=client.recvfrom(4096)

print addr
print data

