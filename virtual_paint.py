import cv2
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3,540)
cap.set(4,380)
cap.set(10,100)

myColors = [[18,107,104,64,232,255], [5,107,0,19,255,255],[62,87,68,94,218,255], [171,129,0,179,203,217]]
myColorV=[[32,159,227],[32,87,227],[23,130,4],[4,12,130]]
mypoints=[]

def findColor(img,myColors,myColorV):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHsv, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgRes,(x,y),5,myColorV[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area>500:
            # cv2.drawContours(imgRes, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y




def drawOnCanvas(mypoints,myColorV):
    for point in mypoints:
        cv2.circle(imgRes, (point[0], point[1]), 10, myColorV[point[2]], cv2.FILLED)


while True:
    success, img=cap.read()
    if img is None:
        break
    imgRes = img.copy()
    newPoints=findColor(img,myColors,myColorV)
    if len(newPoints)!= 0:
        for newp in newPoints:
            mypoints.append(newp)
    if len(mypoints) != 0:
        drawOnCanvas(mypoints,myColorV)

    cv2.imshow("video", imgRes)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

