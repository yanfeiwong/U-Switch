import time
from socket import *
port=9996
bufsize=1024
udpClient=socket(AF_INET,SOCK_DGRAM)
def get_host_ip():
    ip='127.0.0.1'
    try:
        s=socket(AF_INET,SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip
print(get_host_ip())

t=0
while t<=20:
    ip=get_host_ip().split(".")
    host=ip[0]+'.'+ip[1]+'.'+ip[2]+'.1'
    addr=(host,port)
    data=ip[3]
    data=data.encode()
    udpClient.sendto(data,addr)
    time.sleep(3)
    t=t+1
udpClient.close()
    
