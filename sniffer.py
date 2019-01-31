import socket
import os

# 监听的主机
host="192.168.213.134"

# 创建原始套接字，然后绑定在公开接口上
if os.name=="nt":
    socket_protocol=socket.IPPROTO_IP
else:
    socket_protocol=socket.IPPROTO_ICMP

sniffer=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# 设置在捕获的数据包中的包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 在windows系统上，我们要IOCTL以启用混杂模式
if os.name=="nt":
    sniffer.ioctl(socket.SID_RCVALL, socket.RCVALL_ON)

print sniffer.recvfrom(65565)

# 在windows平台上关闭混杂模式
if os.name=="nt":
    sniffer.ioctl(socket.SID_RCVALL, socket.RCVALL_OFF)

