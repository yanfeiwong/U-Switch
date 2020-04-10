#a simple demo to stream real time video to your phone with U-Switch
import cv2,math,time
from socket import *
cap = cv2.VideoCapture(0)
#setup video size
cap.set(3,690)
cap.set(4,360)
host  = '192.168.3.17'
port = 9921 #your receiving port
bufsize = 1024.0
addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)

while True:
      ret, image_np = cap.read()
      cv2.imshow('frame',image_np)
      udpClient.sendto(("sta").encode(),addr) # start message for receive a frame
      data=cv2.imencode(".jpg",image_np,[cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()
      cut=int(math.ceil(len(data)/(bufsize)))
      strr="size;"+str(cut)# tell your phone how many cuts you will send to avoid broken image
      udpClient.sendto(strr.encode(),addr)
      for i in range(cut):
          udpClient.sendto(data[i*int(bufsize):(i+1)*int(bufsize)],addr)#cut and send all cuts
      udpClient.sendto(("end").encode(),addr)#end message
      if cv2.waitKey(25) & 0xFF == 27:
        udpClient.sendto(("clear").encode(),self.addr)
        cv2.destroyAllWindows()
        cap.release()
