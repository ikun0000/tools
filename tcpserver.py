import socket
import threading

bind_ip='0.0.0.0'
bind_port=9999

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TCP服务端要使用bind()指定监听地址和端口，并且使用listen()设置最大连接数
server.bind((bind_ip, bind_port))
server.listen(5)
print '[*] Listening on %s:%d' % (bind_ip, bind_port)

# 线程函数
def handle_client(client_socket):
    request=client_socket.recv(4096)
    print '[*] Received: %s' % request
    client_socket.send('ACK!')
    client_socket.close()

while True:
    # 之后使用accept()进入监听并返回链接的实例和地址端口信息
    # addr[0] : client ip address
    # addr[0] : client port
    client,addr=server.accept()
    print '[*] Accept connection from %s:%d' % (addr[0], addr[1])
    client_handler=threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
