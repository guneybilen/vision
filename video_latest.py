import cv2
import numpy as np
import os
import re
import time
import mediapipe as mp
import time
from VideoSaverSqlAlchemy import VideoToDatabase
from iteration_utilities import deepflatten
from pathlib import Path


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

capture_duration = 10

# capturing video
capture = cv2.VideoCapture(2)


width= int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_format = "mp4"

result = {}
object_to_be_modified = {}

#result["video_name"] = "output0.mp4"
ext = ".%s"%(video_format)

package_dir = Path(__file__).parent.absolute()
dir_path = os.path.dirname(package_dir)

video_base_name = input("Please enter video name: ")
#print(type(video_base_name + ext))


for root, dirs, files in os.walk(dir_path):
	for dir in dirs:
		for file in files:
			if file.endswith(ext):
				while video_base_name + ext == file:
					video_base_name = input("That name already exists. Please enter another name: ")
				

description = input("Please, enter a description: ")  

#for the following statement is not needed.
result["video_name"] = video_base_name + ext

result["codec"] = cv2.VideoWriter_fourcc(*'mp4v')
result["fps"] = 16
result["total_size"] = (width,height)


counter = 0
sorted_list_biggest = 0


if os.path.exists("output%d.%s"%(sorted_list_biggest, video_format)):
    result["video_name"] = "%s%d.%s"%(video_base_name, video_format)

object_to_be_modified_for_video_name = cv2.VideoWriter(result["video_name"], result["codec"], result["fps"], result["total_size"]) 

start_time = time.time()

# capture.isOpened() is for waiting a keboard key for finishing the video capture.
# while(capture.isOpened()):

# the timing way of capturing video is not very accurate.
# while( int(time.time() - start_time) < capture_duration ):

# it may be best to fiddle around with ways of capturing video, but for now
# upto a frame seemed most optimized for comparison, IMHO.
for i in range(0, 120):
    capture.set(1, i)

    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 7, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Detecting Motion...", img)
   
    object_to_be_modified_for_video_name.write(img)
    if cv2.waitKey(1) == ord('q'):
	    break


# saving video to database mariadb which is exactly same as mysql RDMS:
VideoToDatabase.record(name = result["video_name"].split(".")[:-1][0], extension = ext, description = description)

capture.release()
cv2.destroyAllWindows()









    
