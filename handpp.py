import cv2
import  numpy as np
from cvzone.HandTrackingModule import HandDetector
from collections import deque

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
blue_points = [deque(maxlen=512)]
green_points = [deque(maxlen=512)]
red_points = [deque(maxlen=512)]
yellow_points = [deque(maxlen=512)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
color_index = 0

paintWindow = np.zeros((471, 636, 3)) + 255

paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

cv2.namedWindow("Paint")


cap = cv2.VideoCapture(0)
paintWindow = np.zeros((471, 636, 3)) + 255

detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = cv2.rectangle(img, (40, 1), (140, 65), (0, 0, 0), 2)
    img = cv2.rectangle(img, (160, 1), (255, 65), colors[0], -1)
    img = cv2.rectangle(img, (275, 1), (370, 65), colors[1], -1)
    img = cv2.rectangle(img, (390, 1), (485, 65), colors[2], -1)
    img= cv2.rectangle(img, (505, 1), (600, 65), colors[3], -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "CLEAR ALL", (49, 33), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "BLUE", (185, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "GREEN", (298, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "RED", (420, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "YELLOW", (520, 33), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    hands, img = detector.findHands(img)
    if hands:
        hand1=hands[0]
        lmList1=hand1["lmList"]
        bbox=hand1["bbox"]
        centerpoint1=hand1["center"]
        handtype1=hand1["type"]
        finger1=detector.fingersUp(hand1)
        cv2.circle(img, lmList1[8][:2], 20, colors[0], -1)
        center=lmList1[8][:2]

        if finger1==[0,1,0,0,0]:
            if center[1] <= 65:
                if 40 <= center[0] <= 140:

                    blue_points = [deque(maxlen=512)]
                    green_points = [deque(maxlen=512)]
                    red_points = [deque(maxlen=512)]
                    yellow_points = [deque(maxlen=512)]

                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0

                    paintWindow[67:, :, :] = 255

                elif 160 <= center[0] <= 255:
                    color_index = 0

                elif 275 <= center[0] <= 370:
                    color_index = 1

                elif 390 <= center[0] <= 485:
                    color_index = 2

                elif 505 <= center[0] <= 600:
                    color_index = 3

            else:
                if color_index == 0:
                    blue_points[blue_index].appendleft(center)

                elif color_index == 1:
                    green_points[green_index].appendleft(center)

                elif color_index == 2:
                    red_points[red_index].appendleft(center)

                elif color_index == 3:
                    yellow_points[yellow_index].appendleft(center)



        else:
            blue_points.append(deque(maxlen=512))
            blue_index += 1

            green_points.append(deque(maxlen=512))
            green_index += 1

            red_points.append(deque(maxlen=512))
            red_index += 1

            yellow_points.append(deque(maxlen=512))
            yellow_index += 1

        points = [blue_points, green_points, red_points, yellow_points]

        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue

                    cv2.line(img, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)



    cv2.imshow("paint", paintWindow)
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
