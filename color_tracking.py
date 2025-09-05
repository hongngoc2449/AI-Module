##Follow object by color tracking 
#https://www.youtube.com/watch?v=UP29EJ-f2dA

import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()

    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Tăng dải màu để nhận diện nhiều màu hơn (ví dụ: xanh lá, vàng, xanh dương)
    lower = np.array([20, 40, 40])
    upper = np.array([100, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    ball_cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ball_cnts = imutils.grab_contours(ball_cnts)

    if (len(ball_cnts) > 0):
        for c in ball_cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break