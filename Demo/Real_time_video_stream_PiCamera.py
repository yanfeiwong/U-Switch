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
res_x=640  #照片分辨率
res_y=480
framerate=40 #拍摄帧率，低帧率会模糊
iso=400   #拍摄iso
jpeg_quality=20 #照片质量，太大会卡



with PiCamera() as camera:
    #配置相机
    camera.resolution=(res_x,res_y)
    camera.framerate=framerate
    camera.iso=iso
    #准备内存stream
    stream=BytesIO()
    #处理每一张照片（foo）
    for foo in camera.capture_continuous(stream,"jpeg",quality=jpeg_quality,use_video_port=True):#resize=(1080,360),
        size=sys.getsizeof(stream) #内存写入文件的大小
        stream.seek(0) #指针到stream的0位置
        udpClient.sendto(("sta").encode(),addr) #通知手机开始接收一张图片
        cut=int(math.ceil(size)/(bufsize)) #计算切多少片
        strr="size;"+str(cut) 
        udpClient.sendto(strr.encode(),addr) #发送切片数量
        for i in range(cut): #循环发送每一个切片
            d=stream.read(int(bufsize))
            udpClient.sendto(d,addr)
        udpClient.sendto(("end").encode(),addr) #通知手机接受完成显示图片
        stream.seek(0)
        stream.truncate() #内存流刷新

#这个脚本可能有一些问题，会在图片末尾有黑边

