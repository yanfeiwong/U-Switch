import os
from pygame import mixer
from socket import *


host = ''
phone_ip = 'your phones ip'
port = 123
sendport = 9999
bufsize = 1024
addr = (host,port)
addr1 = (phone_ip,sendport)
udpClient = socket(AF_INET,SOCK_DGRAM)
udpServer = socket(AF_INET,SOCK_DGRAM)
udpServer.bind(addr)



def findmus():
    L=[]
    l=os.listdir()
    for f in l:
        if f.find(".mp3")==len(f)-4 or f.find(".flac")==len(f)-5:
            L.append(f)  
    return(L)

def play(x):
    try:
        mixer.music.load(x)
        mixer.music.play()
        return 0
    except:
        return 1


def send(sdata):
    sdata = sdata.encode()
    udpClient.sendto(sdata,addr1)

def Is_Int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

L=findmus()
mixer.init()
nowplaying=0
print("Player has started")
print("Find the following song：")
n=0
for i in L:
    n=n+1
    print(str(n)+"."+i)

while 1:
    data,addr = udpServer.recvfrom(bufsize)
    data=data.decode()
    if data=="exit":
        udpServer.close()
        mixer.quit()
        exit(0)
        
    elif data=="what do we have":
        n=0
        for i in L:
            n=n+1
            send(str(n)+"."+i)
            
    elif Is_Int(data):
        if play(L[int(data)-1])==0:
            nowplaying=int(data)-1
            send("Playing:"+ L[nowplaying])
        
    elif data=="play":
        try:
            mixer.music.play()
        except:
            play(L[nowplaying])
            send("Playing"+L[nowplaying])

    elif data=="pause":
        mixer.music.pause()

    elif data=="stop":
        mixer.music.stop()

    elif data=="next":
        nowplaying=nowplaying+1
        if nowplaying>=len(L):
            nowplaying=0
        play(L[nowplaying])
        send("Playing"+L[nowplaying])

    elif data=="last":
        nowplaying=nowplaying-1
        if nowplaying<0:
            nowplaying=len(L)-1
        play(L[nowplaying])
        send("Playing"+L[nowplaying])
    else:
        send("Sorry, I only support these instructions now:what do we have,digital on-demand, play, pause, stop, next, last, exit")
