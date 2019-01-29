import socket

target_host='127.0.0.1'
target_port=80

client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto('aaabbbccc', (target_host, target_port))

date, addr=client.recvfrom(4096)

print addr
print data

