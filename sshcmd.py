import threading
import paramiko
import subprocess
import getopt
import sys

def usage():
    print "Usage: "
    print 
    print "-t --target=[ip addr]        - the target ip "
    print "-u --usernm=[username]       - the username"
    print "-p --passwd=[password]       - the password"
    print "-c --cmd=[execute command]   - the execute command"
    print 

def ssh_command(ip, user, passwd, command):
    client=paramiko.SSHClient()
    #client.load_host_keys('/home/snake/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=user, password=passwd)
    except:
        print "[-] Failed to connect %s" % ip
        client.close()
        return

    ssh_session=client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)

    return

def main():
    ip=""
    usernm=""
    passwd=""
    command=""

    try:
        opts,args=getopt.getopt(sys.argv[1:], "t:u:p:c:",
                ["target=","usernm=","passwd=","cmd="])
    except getopt.GetoptError as err:
        print str(err)
        usage()


    for o,a in opts:
        if o in ('-t','--target'):
            ip=a
        elif o in ('-u','--usernm'):
            usernm=a
        elif o in ('-p','--passwd'):
            passwd=a
        elif o in ('-c','--cmd'):
            command=a

    if len(ip) and len(usernm) and len(passwd) and len(command):
        ssh_command(ip, usernm, passwd, command)


if __name__ == "__main__":
    main()

