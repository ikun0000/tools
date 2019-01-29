import sys
import socket
import getopt
import threading
import subporcess

listen=False
command=False
upload=False
execute=""
target=""
upload_destination=""
port=0

def usage():
    print "Net Cat Tool"
    print 
    print "Usage: netcat.py -t target_host -p target_port"
    print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given given file upoon receiving a connection"
    print "-c --command             - initialize a command shell"
    print "-u --upload=destination  - upoon receiving connection upload a file and write to [destination]"
    print 
    print 
    print "Example: "
    print "netcat.py -t 192.168.0.1 -p 5555 -l -c"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netcat.py -t 192.168.0.1 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts,args=getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--commandshell"):
            command=True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port=int(a)
        else:
            assert False,"Unhandled Option"

    if not listen and len(target) and prot > 0:
        buffer=sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

if __name__ == "__main__":
    main()


def client_sender(buffer):
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:
            recv_len=1
            response=""

            while recv_len:
                data=clinet.recv(4096)
                recv_len=len(data)
                response+=data

                if recv_len < 4096:
                    break
        
            print response,

            buffer=raw_input("")
            buffer+="\n"

            client.send(buffer)
    
    except:
        print "[*] Exception! Exiting."
        client.close()


def server_loop():
    global target

    if not len(target):
        target="0.0.0.0"

    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr=server.accept()
        client_thread=threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    command=command.rstrip()

    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="Failed to execute command. \r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer=""

        while True:
            data=client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer+=data

            try:
                file_destination=open(upload_destination,"wb")
                file_destination.write(file_buffer)
                file_destination.close()

                client_socket.send("Successful saved file to %s\r\n" % upload_destination)
            except:
                client_socket.send("Failed to saved file to %s\r\n" % upload_destination)

    if len(execute):
        output=run_command(execute)
        client_sock.send(output)

    if command:
        while True:
            client_socket.send("BHP:#> ")

            cmd_buffer=""
            while '\n' not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
                response=run_command(cmd_buffer)

                client_socket.send(response)


