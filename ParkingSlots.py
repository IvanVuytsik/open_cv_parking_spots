import cv2
import pickle
import cvzone
import numpy as np


cap = cv2.VideoCapture('carPark.mp4')
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


w,h = 105, 45

def checkParkingSpace(imgProc):
    slotCount = 0
    for pos in posList:
        x, y = pos

        # cropping
        imgCrop = imgProc[y:y+h, x:x+w]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 850:
            color = (0, 255, 0)
            thickness = 5
            slotCount += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0]+w, pos[1]+h), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + h - 2), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {slotCount} / {len(posList)}', (0, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))

while True:
    # looping the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16) #black/white img
    imgMedian = cv2.medianBlur(imgThreshold, 5) #removes noize
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    cv2.waitKey(10)

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0]+w, pos[1]+h), (0, 255, 0), 2)
    # cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThr", imgThreshold)
    # cv2.imshow("ImageMed", imgMedian)
    # cv2.imshow("ImageDil", imgDilate)
    #cv2.waitkey(10)