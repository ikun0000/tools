import socket

target_host='www.baidu.com'
target_port=80

# 创建socket套接字，AF_INET代表使用标准IPv4地址，SOCK_STREAM代表创建TCP套接字
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

# 像百度发送HTTP头部
client.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")

# 返回4096个字节的数据
response=client.recv(4096)

print response
