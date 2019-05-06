from socket import *
host  = '192.168.31.119' # This is the gray ip displayed on the phone.
port = 9999 #Greater than 3 digits, and then fill in the third column of the mobile phone
bufsize = 1024
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)
while 1:
	data=input("Press \"Enter\" to confirm:\n")
	if data=="":
		pass
	else:
		data = data.encode()
		udpClient.sendto(data,addr)
		print("Send over")
