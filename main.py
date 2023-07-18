import cv2
import numpy as np
#####
#  cap= cv2.VideoCapture(?) (for Real-Time detector)
#####

widthImg = 500
heightImg = 640
def findpaper(img):
    Gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(img,(5,5),1)
    Canny = cv2.Canny(Blur,200,200)
    kernel = np.ones((5,5))
    Dial = cv2.dilate(Canny,kernel,iterations=2)
    Thres = cv2. erode(Dial,kernel,iterations=1)
    return Thres

def reorder (Coordinates):
    Coordinates = Coordinates.reshape((4, 2))
    New_Coordiantes = np.zeros((4,1,2),np.int32)
    sumption = Coordinates.sum(1)
    New_Coordiantes[0]=Coordinates[np.argmin(sumption)]
    New_Coordiantes[3]=Coordinates[np.argmax(sumption)]
    diff=np.diff(Coordinates, 1)
    New_Coordiantes[1] = Coordinates[np.argmin(diff)]
    New_Coordiantes[2] = Coordinates[np.argmax(diff)]
    return New_Coordiantes


def getContours(img):
    Coordinates = np.array([])
    contours,hierachy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >5000:
            peri=cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            if len(approx) >= 4:
                Coordinates = approx
                cv2.drawContours(imgContour,Coordinates, -1, (255, 0, 0), 20)
    return Coordinates
def getWarp(imgContour,big):
    biggest= reorder(big)
    cor1 = np.float32(biggest)
    cor2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
    Transformer =cv2.getPerspectiveTransform(cor1,cor2)
    imgOutput =cv2.warpPerspective(img, Transformer, (widthImg,heightImg))
    return imgOutput

while True:
    img = cv2.imread("resource/d70d4225789aa8c4f18b.jpg") ###### adjust path of image here ######
    #####
    # img= cap.read() for Real-time detector
    #####
    img=cv2.resize(img,(500,640))
    imgContour= img.copy()
    imgThres = findpaper(img)
    Coordinate =getContours(imgThres)
    imgOutput= getWarp(imgContour, Coordinate)
    cv2.imshow("result", imgThres)
    cv2.imshow("draw", imgContour)
    cv2.imshow("output", imgOutput)
    cv2.waitKey(0) ##### cv2.waitkey(1) for Real-time detector