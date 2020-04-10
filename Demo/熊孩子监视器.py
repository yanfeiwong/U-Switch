from socket import *
from threading import Thread
from PIL import ImageGrab
from io import BytesIO
from numpy import array
from sys import platform
from math import ceil
import  cv2

#弹窗警告功能暂时只针对win平台
if platform == "win32" or platform == "win64":
    ISWIN = True
    import ctypes

Use_WebCam=False
WebCam_starting=False


#接收端ip列表，当接收端地址从其中移除将不再向其发送
#支持多端接收
Running=[]
#发送分辨率
Res_x=690
Res_y=360

#配置UDP
r_host = ''
r_port = 127  #电脑的接收端口
s_port = 9921 #手机的接收端，使用4位数的端口（受部分安卓系统限制）
bufsize = 1024 
r_addr = (r_host,r_port)
r_udpServer = socket(AF_INET,SOCK_DGRAM) 
r_udpServer.bind(r_addr)

#接收线程
class Rec_Thread(Thread):
    def __init__(self, server: socket):
        super().__init__()
        self.server = server
    def run(self):
        global Running
        global Use_WebCam
        while 1:
            data,addr = self.server.recvfrom(bufsize)
            data=data.decode()
            if data=="exit":
                Running=[]
                if Use_WebCam:
                    Use_WebCam=False
                    try:
                        cap.release()
                    except:
                        pass
                exit(0)
            if data=="start" and not addr[0] in Running:
                Running.append(addr[0]) #将发来start命令的ip地址添加到列表
                stream_thread = Send_Thread(addr[0]) #创建发送线程
                stream_thread.start()
            elif data=="stop" and addr[0] in Running:
                Running.remove(addr[0])
            elif data=="warning":
                Msg_Box_thread = Msg_Box(0)
                Msg_Box_thread.start()
            elif data=="camera" and not WebCam_starting: #摄像头启动有延迟请耐心
                if Use_WebCam:
                    Use_WebCam=False
                    try:
                        cap.release()
                    except:
                        pass
                else:
                    Use_WebCam=True
            else:
                Msg_Box_thread = Msg_Box(1,addr[0],data)
                Msg_Box_thread.start()

                
#发送线程
class  Send_Thread(Thread):
    def __init__(self,host):
        super().__init__()
        self.host = host
        self.addr = (host,s_port)
        self.udpClient = socket(AF_INET,SOCK_DGRAM)
    def run(self):
        while self.host in Running: 
            captureImage = ImageGrab.grab() #捕获屏幕截图
            captureImage = captureImage.resize((Res_x,Res_y))
            #转变为cv格式以便编码发送
            captureImage = cv2.cvtColor(array(captureImage), cv2.COLOR_RGB2BGR)
            #如果启用摄像头将进行图片叠加
            if Use_WebCam:
                try:
                    get, image_np = cap.read()
                    if get :
                        rows, cols = image_np.shape[:2]
                        captureImage[:rows, :cols]=image_np
                    elif not WebCam_starting:
                        Cam_thread = Set_Webcam()
                        Cam_thread.start()
                except:
                    if not WebCam_starting:
                        Cam_thread = Set_Webcam()
                        Cam_thread.start()

            #captureImage.resize((690,360))
            data=cv2.imencode(".jpg",captureImage,[cv2.IMWRITE_JPEG_QUALITY, 30])[1].tobytes()
            cut=int(ceil(len(data)/(bufsize)))#计算切片数
            strr="size;"+str(cut)# 通知手机开始接收切片
            self.udpClient.sendto(strr.encode(),self.addr)
            for i in range(cut):
              self.udpClient.sendto(data[i*int(bufsize):(i+1)*int(bufsize)],self.addr)#切片并且发送
            self.udpClient.sendto(("end").encode(),self.addr)#通知手机显示图片
        self.udpClient.sendto(("clear").encode(),self.addr)#结束，清理手机上显示的图片,V1.2.7以后版本可用


#弹窗警告功能
class  Msg_Box(Thread):
    def __init__(self,Type,addr="",Text=""):
        super().__init__()
        self.Type=Type
        self.addr=addr
        self.Text=Text
    def run(self):
        if ISWIN:
            if self.Type == 0: #警告
                ctypes.windll.user32.MessageBoxW(0,  "专心学习！", "不专心警告:",16+4096)
            if self.Type == 1: #其他消息
                ctypes.windll.user32.MessageBoxW(0,  self.Text, "来自:"+self.addr,1+4096)
        
#异步摄像头启动
class  Set_Webcam(Thread):
    def run(self):
        global WebCam_starting
        global cap
        WebCam_starting=True
        cap = cv2.VideoCapture(0)
        cap.set(3,int(Res_x/3.0))
        cap.set(4,int(Res_y/3.0))
        WebCam_starting=False
        
# 获取本机ip
def get_host_ip():
    ip='127.0.0.1'
    try:
        s=socket(AF_INET,SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

        
    


server_thread = Rec_Thread(r_udpServer)
server_thread.start()
#提示本机ip便于接收
Msg_Box_thread = Msg_Box(1,"熊孩子监视器","本机IP:"+get_host_ip()+"\n接收端口:"+str(r_port))
Msg_Box_thread.start()

