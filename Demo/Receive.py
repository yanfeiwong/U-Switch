from socket import *
host = ''
port = 127 
bufsize = 1024 
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) 
udpServer.bind(addr)
while 1: 
    data,addr = udpServer.recvfrom(bufsize) 
    data=data.decode()
    if data == "exit":
        udpServer.close()
        print("Exited")
        exit(0) 
    else:
        print(data)
        #if data==..... do ....
