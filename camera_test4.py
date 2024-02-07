# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:49:45 2022

@author: 사용자
"""

from datetime import datetime
import cv2
import numpy as np
import serial
import time

ArduinoSerial=serial.Serial('com4',9600,timeout=5) #arduino시리얼과 연결포트 설정
time.sleep(1)

def detect(img):
    lower_range=np.array([40,150,150], dtype="uint8")
    upper_range=np.array([70,255,255], dtype="uint8")
    img=cv2.inRange(img,lower_range,upper_range)
    cv2.imshow("Range", img)
    m=cv2.moments(img)
    if(m["m00"] != 0) :
        x=int(m["m10"]/m["m00"])
        y=int(m["m01"]/m["m00"])
    else:
        x=0
        y=0
    return (x, y)

cam=cv2.VideoCapture(0)
count=1
last_x=0
last_y=0
count=1

    
while(cam.isOpened()):
    ret, frame=cam.read()    
    cur_x, cur_y=detect(frame)
    cv2.line(frame, (cur_x, cur_y), (last_x, last_y), (0, 0, 200), 5)
    last_x=cur_x
    last_y=cur_y
    
    if last_x is 0 & last_y is 0:
       cv2.imshow('frame', frame)
       print('Image load failed!')
    else:
       ArduinoSerial.write(b'a')
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break
    
cam.release()
cv2.destroyAllWindows()
       



