##Follow object by color tracking 
#https://www.youtube.com/watch?v=UP29EJ-f2dA


import cv2
import numpy as np
import imutils


cap = cv2.VideoCapture(0)

# Tạo cửa sổ và trackbars để điều chỉnh HSV
def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.createTrackbar('H Lower', 'Trackbars', 20, 179, nothing)
cv2.createTrackbar('S Lower', 'Trackbars', 40, 255, nothing)
cv2.createTrackbar('V Lower', 'Trackbars', 40, 255, nothing)
cv2.createTrackbar('H Upper', 'Trackbars', 100, 179, nothing)
cv2.createTrackbar('S Upper', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('V Upper', 'Trackbars', 255, 255, nothing)

while (True):
    ret, frame = cap.read()


    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Lấy giá trị HSV từ trackbar
    h_lower = cv2.getTrackbarPos('H Lower', 'Trackbars')
    s_lower = cv2.getTrackbarPos('S Lower', 'Trackbars')
    v_lower = cv2.getTrackbarPos('V Lower', 'Trackbars')
    h_upper = cv2.getTrackbarPos('H Upper', 'Trackbars')
    s_upper = cv2.getTrackbarPos('S Upper', 'Trackbars')
    v_upper = cv2.getTrackbarPos('V Upper', 'Trackbars')
    lower = np.array([h_lower, s_lower, v_lower])
    upper = np.array([h_upper, s_upper, v_upper])

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