import cv2
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import alsaaudio
import math

from handTracker import HandTracker as ht


result = {}
object_to_be_modified = {}

#################################################################
#FMI: THE FOLLOWING MEASUREMENTS ARE IN PARAMOUNT IMPORTANCE.
#OTHERWISE THE VIDEO IS BEING RECORDED AS 20kb AND NOT WATCHABLE.
vCam, hCam = 640, 480
#################################################################
result["video_name"] = "output0.avi"
result["codec"] = cv2.VideoWriter_fourcc(*'MJPG')
result["fps"] = 20
result["total_size"] = (vCam,hCam)

#mixer = alsaaudio.Mixer()
#value = mixer.getvolume()[0]
#print(value)

"""print(value)
value = value + 5
if value > 100:
	value = 100
	mixer.setvolume(value)"""



cap = cv2.VideoCapture(0)
cap.set(3, vCam)
cap.set(4, hCam)

amount_of_frames1 = 0

detector = ht(detectionCon=0.9)
#mixer.setvolume(100)
#volRange = value
#minVol = 0
#maxVol = 100
#volPer = (value/100) * 100
#volBar = 0
#yVolPer = 0
area_beginning1 = 0
area_end1 = 0
area_beginning2 = 0
area_end2 = 0
area_beginning3 = 0
area_end3 = 0
area_beginning4 = 0
area_end4 = 0
area_beginning5 = 0
area_end5 = 0
PI = 3.141569

area_median_array1 = []
area_median_array2 = []
area_median_array3 = []
area_median_array4 = []
area_median_array5 = []

object_to_be_modified_for_video_name = cv2.VideoWriter(result["video_name"], result["codec"], result["fps"], result["total_size"]) 

dataFrame={}

while amount_of_frames1 <= 201:

	sucess, img = cap.read()
	img = detector.findHands(img)
	lmList = detector.getPosition(img, draw=False)
	if len(lmList) != 0:
		#print(lmList[4], lmList[0])
		
		q1, w1 = lmList[4][1], lmList[4][2]
		q2, w2 = lmList[5][1], lmList[5][2]

		x1, y1 = lmList[8][1], lmList[8][2]
		x2, y2 = lmList[5][1], lmList[5][2]

		t1, z1 = lmList[12][1], lmList[12][2]
		t2, z2 = lmList[9][1],  lmList[9][2]
		
		a1, s1 = lmList[16][1], lmList[16][2]
		a2, s2 = lmList[13][1], lmList[13][2]
		
		b1, n1 = lmList[20][1], lmList[20][2]
		b2, n2 = lmList[17][1], lmList[17][2]
		
		
		cv2.circle(img, (q1, w1), 5, (255,0,0), cv2.FILLED)
		cv2.circle(img, (q2, w2), 5, (255,0,0), cv2.FILLED)
		
		cv2.circle(img, (x1, y1), 5, (255,0,0), cv2.FILLED)
		cv2.circle(img, (x2, y2), 5, (255,0,0), cv2.FILLED)
		
		cv2.circle(img, (t1, z1), 5, (255,0,0), cv2.FILLED)
		cv2.circle(img, (t2, z2), 5, (255,0,0), cv2.FILLED)
		
		cv2.circle(img, (a1, s1), 5, (255,0,0), cv2.FILLED)
		cv2.circle(img, (a2, s2), 5, (255,0,0), cv2.FILLED)
		
		cv2.circle(img, (b1, n1), 5, (255,0,0), cv2.FILLED)
		cv2.circle(img, (b2, n2), 5, (255,0,0), cv2.FILLED)
		#cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 9)
		
		distance1  = math.sqrt((q2-q1)*(q2-q1) + (w2-w1)*(w2-w1))
		distance2  = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
		distance3  = math.sqrt((t2-t1)*(t2-t1) + (z2-z1)*(z2-z1))
		distance4  = math.sqrt((a2-a1)*(a2-a1) + (s2-s1)*(s2-s1))
		distance5  = math.sqrt((b2-b1)*(b2-b1) + (n2-n1)*(n2-n1))

		area_beginning1 = 2 * PI * 180*180
		area_end1 = (2 * PI) * distance1 * distance1
		area_median_array1_calc = (area_beginning1 + area_end1)/2
		area_median_array1.append(int(area_median_array1_calc))
		
		area_beginning2 = 2 * PI * 180*180
		area_end2 = (2 * PI) * distance2 * distance2
		area_median_array2_calc = (area_beginning2 + area_end2)/2
		area_median_array2.append(int(area_median_array2_calc))
		
		area_beginning3 = 2 * PI * 180*180
		area_end3 = (2 * PI) * distance3 * distance3
		area_median_array3_calc = (area_beginning3 + area_end3)/2
		area_median_array3.append(int(area_median_array3_calc))
		
		area_beginning4 = 2 * PI * 180*180
		area_end4 = (2 * PI) * distance4 * distance4
		area_median_array4_calc = (area_beginning4 + area_end4)/2
		area_median_array4.append(int(area_median_array4_calc))
		
		area_beginning5 = 2 * PI * 180*180
		area_end5 = (2 * PI) * distance5 * distance5
		area_median_array5_calc = (area_beginning5 + area_end5)/2
		area_median_array5.append(int(area_median_array5_calc))

		dct = { 
			'thumb': area_median_array1, 
			'pointingFinger': area_median_array2,
			'middleFinger': area_median_array3, 
			'ringFinger': area_median_array4,
			'pinky': area_median_array5 
		} 
		dataFrame = pd.DataFrame(dct)
		df = dataFrame.mean()
		print(df)
		
		for key in dct:
		  df.plot(x=key, y=np.array(dct[key]), kind="bar", label=key, rot=5, fontsize=4)

	cv2.rectangle(img, (25, 450), (125, (450-int(area_end1/125))), (0,255,0), cv2.FILLED)
	cv2.rectangle(img, (150, 450), (250, (450-int(area_end2/125))), (0,255,0), cv2.FILLED)
	cv2.rectangle(img, (275, 450), (400, (450-int(area_end3/125))), (0,255,0), cv2.FILLED)
	cv2.rectangle(img, (425, 450), (550, (450-int(area_end4/125))), (0,255,0), cv2.FILLED)
	cv2.rectangle(img, (575, 450), (700, (450-int(area_end5/125))), (0,255,0), cv2.FILLED)
	#cv2.putText(img, 'FPS:{0} %'.format(int(area_end/125)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 3)
	
	amount_of_frames1 = amount_of_frames1 + 1
	
	object_to_be_modified_for_video_name.write(img)

	cv2.imshow("Fingers Analysis", img)
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
plt.show()



