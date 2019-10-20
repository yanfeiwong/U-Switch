#手机创建热点，“心跳”程序每5秒发送一次本机ip给手机
#“心跳”程序可设置为开机自启
import time
from socket import *
port=9922
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
#print(get_host_ip())
ip=get_host_ip().split(".")
t=1
while t<=254:
    #把接收方的IP发送给接收方，120版本后没什么卵用了
    host=ip[0]+'.'+ip[1]+'.'+ip[2]+"."+str(t)
    #print(host)
    addr=(host,port)
    data=str(addr)
    data=data.encode()
    udpClient.sendto(data,addr)
    t=t+1
    
host=ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+ip[3]
t=1
while t<=20:
    #每五秒发送一次设备ip给接收方，发送20次
    #print(host)
    addr=(host,port)
    data=str(addr)
    data=data.encode()
    udpClient.sendto(data,addr)
    t=t+1
    time.sleep(5)
udpClient.close()

