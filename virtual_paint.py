import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# cap.set(3, 800)
# cap.set(4, 1200)

# [5, 107, 0, 19, 255, 255], [133, 56, 0, 159, 156, 255], [57, 76, 0, 100, 255, 255],

myColors = [[71, 74, 33, 105, 255, 255]]

# 0, 204, 204 in RGB so 204, 204, 0 in BGR
myColorValues = [[204, 204, 0]]

myPoints = []  # x, y, colorID


def findColor(img, myColors, myColorValues):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])

        mask = cv2.inRange(hsv_image, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 5, myColorValues[count], cv2.FILLED)
        # cv2.imshow(str(color[0]), mask)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints


def getContours(img):
    x, y, w, h = 0, 0, 0, 0
    contours, heirarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # objCorners = len(approx)

            # getting coordinates and with and height

            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]),
                   5, myColorValues[point[2]], cv2.FILLED)


while True:
    success, frame = cap.read()
    imgResult = frame.copy()
    newPoints = findColor(frame, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    # cv2.imshow("frame1", frame)
    # imgResult = cv2.bitwise_not(imgResult)
    imgResult = cv2.flip(imgResult, 1)
    cv2.imshow("frame", imgResult)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
