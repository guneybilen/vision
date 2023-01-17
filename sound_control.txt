import cv2
import time
import numpy as np
import alsaaudio
import math

from handTracker import HandTracker as ht


mixer = alsaaudio.Mixer()
value = mixer.getvolume()[0]
#print(value)

"""print(value)
value = value + 5
if value > 100:
	value = 100
	mixer.setvolume(value)"""


vCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, vCam)
cap.set(4, hCam)

detector = ht(detectionCon=0.9)
mixer.setvolume(100)
volRange = value
minVol = 0
maxVol = 100
volPer = (value/100) * 100
volBar=0
yVolPer = 0

while True:
	sucess, img = cap.read()
	img = detector.findHands(img)
	lmList = detector.getPosition(img, draw=False)
	if len(lmList) != 0:
		#print(lmList[4], lmList[0])

		x1, y1 = lmList[4][1], lmList[4][2]
		x2, y2 = lmList[8][1], lmList[8][2]


		cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
		cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
		cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 9)

		length = math.hypot(x2-x1, y2-y1)
		volPer = (length/100) * 100
		yVolPer = (400 * volPer)/100
				
		vol = np.interp(length, [50, 100], [minVol, maxVol])
		#print(int(vol))
		mixer.setvolume(int(vol))

	cv2.rectangle(img, (100, 450), (150, int(450-yVolPer)), (0,255,0), cv2.FILLED)
	cv2.putText(img, 'FPS:{0} %'.format(int(volPer)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 3)


	cv2.imshow("Img", img)
	cv2.waitKey(1)
