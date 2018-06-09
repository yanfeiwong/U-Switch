from socket import *
host  = '192.168.31.119' # 这是手机上显示的那个灰色的ip
port = 9999 #接口选择大于3位数的，然后填写在手机端的第三栏（手机端其余不变）
bufsize = 1024
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)
while 1:
	data=input()#等待输入要发送的消息（输入完回车确认）
	if data=="":
		pass
	else:
		data = data.encode()
		udpClient.sendto(data,addr)
		print("send over")
