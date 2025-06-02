import cv2
import time
import os


import HTModule as htm


wcam, hcam = 640,480

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

folderpath = "fingers"
myList=os.listdir(folderpath)
print(myList)

overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime=0
detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]
while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) != 0:
        fingers=[]
        #thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #forefingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)

        h,w,c=overlayList[totalFingers-1].shape
        img[0:h,0:w]=overlayList[totalFingers-1]

        cv2.rectangle(img,(20,225),(170,425),(255,0,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(43,375),cv2.FONT_HERSHEY_PLAIN,10,(0,0,255),25)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS:{int(fps)}',(400,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)