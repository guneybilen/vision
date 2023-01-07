import cv2
import numpy as np
import os
import re
import time
from VideoSaverSqlAlchemy import VideoToDatabase
from iteration_utilities import deepflatten
from pathlib import Path

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



temp = 0
ary = []
flatten_list = []
flattened = []
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


    # to read frame by frame
    _, img_1 = capture.read()
    _, img_2 = capture.read()

    
    # find difference between two frames
    diff = cv2.absdiff(img_1, img_2)

    # to convert the frame to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # apply some blur to smoothen the frame
    diff_blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

    # to get the binary image
    _, thresh_bin = cv2.threshold(diff_blur, 20, 255, cv2.THRESH_BINARY)

    # to find contours
    contours, hierarchy = cv2.findContours(thresh_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 300:
            cv2.rectangle(img_1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #print(contour[0], contour[1])

    cv2.imshow("Detecting Motion...", img_1)
   
    object_to_be_modified_for_video_name.write(img_1)
    if cv2.waitKey(1) == ord('q'):
	    break

# saving video to database mariadb which is exactly same as mysql RDMS:
VideoToDatabase.record(name = result["video_name"].split(".")[:-1][0], extension = ext, description = description)

capture.release()
cv2.destroyAllWindows()


    
