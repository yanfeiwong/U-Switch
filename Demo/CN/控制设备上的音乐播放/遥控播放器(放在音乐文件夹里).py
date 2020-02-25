import os
from pygame import mixer
from socket import *


host = ''
shoujiip = '手机的ip'
port = 123
sendport = 9999
bufsize = 1024
addr = (host,port)
addr1 = (shoujiip,sendport)
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
print("播放器已启动")
print("找到以下歌曲：")
n=0
for i in L:
    n=n+1
    print(str(n)+"."+i)

while 1:
    data,addr = udpServer.recvfrom(bufsize)
    data=data.decode()
    if data=="退出":
        udpServer.close()
        mixer.quit()
        exit(0)
        
    elif data=="有什么歌":
        n=0
        for i in L:
            n=n+1
            send(str(n)+"."+i)
            
    elif Is_Int(data):
        if play(L[int(data)-1])==0:
            nowplaying=int(data)-1
            send("正在播放:"+ L[nowplaying])
        
    elif data=="播放":
        try:
            mixer.music.play()
        except:
            play(L[nowplaying])
            send("正在播放"+L[nowplaying])

    elif data=="暂停":
        mixer.music.pause()

    elif data=="停":
        mixer.music.stop()

    elif data=="下一首":
        nowplaying=nowplaying+1
        if nowplaying>=len(L):
            nowplaying=0
        play(L[nowplaying])
        send("正在播放"+L[nowplaying])

    elif data=="上一首":
        nowplaying=nowplaying-1
        if nowplaying<0:
            nowplaying=len(L)-1
        play(L[nowplaying])
        send("正在播放"+L[nowplaying])
    else:
        send("对不起现在只支持这些指令：有什么歌，数字点播，播放，暂停，停，下一首，上一首,退出")
