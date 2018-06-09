from socket import * #导入我们要用到的库
host = '' #监听所有端口
port = 123 #用来接收消息的端口
bufsize = 1024 #buf大小，暂时不管
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM) #通讯类别，对这两个参数感兴趣的可以自己查一下，我后面也会介绍
udpServer.bind(addr)#开始监听
while 1: #死循环
    data,addr = udpServer.recvfrom(bufsize) #接收data
	data=data.decode() #收到的data是bytes类型这里编码成utf8
    if data == "exit": #收到exit以后关闭端口退出程序
        udpServer.close() #不关闭端口的话这个端口在关闭idle以前再用不了了
		print("已退出")
        exit(0) 
    else:
        print(data)
        #if data==..... do .... 干你想干的
