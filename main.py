import cv2
import numpy as np

frameWidth = 1600
frameHeight = 900
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
cap.set(cv2.CAP_PROP_FPS, 10)


renkler = [[94, 80, 2, 126, 255, 255], [145, 179, 128, 255, 255, 255], [57, 76, 0, 100, 255, 255]]
renkDeger = [[255, 0, 0], [255, 0, 255], [0, 255, 0]]

noktalar = []   ##[x, y, renkId]pyinstaller

def renkBul(img, renkler, renkDeger):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sayac = 0
    newNoktalar= []
    for renk in renkler:
        lower = np.array(renk[0:3])
        upper = np.array(renk[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 5, renkDeger[sayac], cv2.FILLED)
        if x!=0 and y!=0:
            newNoktalar.append([x,y,sayac])
        sayac = sayac + 1
        #cv2.imshow(str(color[0]),mask)
    return newNoktalar

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (0, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def ekranaCiz(noktalar,renkDeger):
    for nokta in noktalar:
        cv2.circle(imgResult, (nokta[0], nokta[1]), 10, renkDeger[nokta[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newNoktalar = renkBul(img, renkler, renkDeger)
    if len(newNoktalar) != 0:
        for newN in newNoktalar:
            noktalar.append(newN)
    if len(noktalar) != 0:
        ekranaCiz(noktalar, renkDeger)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
