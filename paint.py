import cv2
import numpy as np
import matplotlib.pyplot as plt

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

#yellow,purple,green,blue

myColors = [
            [22, 93, 0,45,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
myColorValues = [       
                 [0,255,255],  
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]

myPoints = []       #[x,y,colorID]

def findColor(img,myColors,myColorValues):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for index, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imghsv,lower,upper)
        x,y = findContours(mask)
        cv2.circle(imgresult,(x,y),10,color=myColorValues[index],thickness=cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,index])
        # cv2.imshow(str(color[0]),mask)
    return newPoints

def findContours(img):

    # imgblur = cv2.GaussianBlur(frame,(7,7),1)
    # imggray = cv2.cvtColor(imgblur, cv2.COLOR_BGR2GRAY)
    # # imgCanny = cv2.Canny(imgblur,255,154)

    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgresult,cnt,-1,(255,255,255),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
            # cv2.rectangle(imgresult,(x,y),(x+w,y+h),(255,255,0),2)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgresult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)


while True:
    ret, frame = cap.read()
    imgresult = frame.copy()

    newPoints = findColor(frame,myColors,myColorValues)
    if len(newPoints) !=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints,myColorValues)


    # imgresult = cv2.rotate(imgresult,cv2.ROTATE_90_CLOCKWISE)
    imgresult = imgresult[100:400,100:400]
    imgresult = cv2.flip(imgresult,0)
    imgresult = cv2.rotate(imgresult,cv2.ROTATE_180)
    cv2.imshow('Virtual Paint',imgresult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()