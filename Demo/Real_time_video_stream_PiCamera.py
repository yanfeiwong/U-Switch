import math,time,sys
from picamera import PiCamera
from socket import *
from io import BytesIO


#udp setup
host  = 'your ip'
port = 9966
bufsize = 1024.0
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)

#camera setup
res_x=640
res_y=480
framerate=40
iso=400
jpeg_quality=20



with PiCamera() as camera:
    camera.resolution=(res_x,res_y)
    camera.framerate=framerate
    camera.iso=iso
    stream=BytesIO()
    for foo in camera.capture_continuous(stream,"jpeg",quality=jpeg_quality,use_video_port=True):#resize=(1080,360),
        size=sys.getsizeof(stream)
        stream.seek(0)
        udpClient.sendto(("sta").encode(),addr)
        cut=int(math.ceil(size)/(bufsize))
        strr="size;"+str(cut)
        udpClient.sendto(strr.encode(),addr)
        for i in range(cut):
            d=stream.read(int(bufsize))
            udpClient.sendto(d,addr)
        udpClient.sendto(("end").encode(),addr)
        stream.seek(0)
        stream.truncate()

