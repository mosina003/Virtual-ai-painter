import cv2
import numpy as np
import time
import os
import HTModule as htm  # Ensure this is implemented correctly

# Brush and eraser thickness
brushThickness = 15
eraserThickness = 100

# Load header images
folderpath = "C:/Users/Mosina.S/PycharmProjects/Handtracking/header"
myList = os.listdir(folderpath)
print("Loaded header images:", myList)

overlayList = []
headerSize = (1280, 125)  # Resize target (width, height)
for impath in myList:
    image = cv2.imread(f'{folderpath}/{impath}')
    image = cv2.resize(image, headerSize)  # Resize to avoid shape mismatch
    overlayList.append(image)

print("Total header images:", len(overlayList))

# Set initial header and draw color
header = overlayList[0]
drawColor = (255, 0, 255)

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

# Hand detector
detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0  # Previous coordinates for drawing

# Canvas for drawing
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Get tip of index and middle fingers
        
        x1, y1 = lmList[8][1:]   # Index
        x2, y2 = lmList[12][1:]  # Middle

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)

        # 4. Selection mode – two fingers up
        if fingers[1] and fingers[2]:
            
            print("Selection Mode")

            # Select header/tool
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (0, 255, 255)  # yellow
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 255)    # pink
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (255, 0, 0)    # blue
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)      # Eraser

            # Draw selection rectangle
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)

        # 5. Drawing mode – only index finger up
        elif fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):  # Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1
        else:
            xp, yp = 0, 0
    # 6. Combine image and canvas
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # 7. Add header image on top
    img[0:125, 0:1280] = header

    # 8. Show output
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
