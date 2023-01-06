import cv2
import numpy as np
from pathlib import Path
from iteration_utilities import deepflatten
import os
import re
import time


capture_duration = 10

# capturing video
capture = cv2.VideoCapture(2)


width= int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_format = "mp4"

result = {}
object_to_be_modified = {}

result["video_name"] = "output0.mp4"
result["codec"] = cv2.VideoWriter_fourcc(*'mp4v')
result["fps"] = 16
result["total_size"] = (width,height)


package_dir = Path(__file__).parent.absolute()
dir_path = os.path.dirname(package_dir)

print(dir_path)

temp = 0
ary = []
flatten_list = []
flattened = []
counter = 0
sorted_list_biggest = 0


for root, dirs, files in os.walk(dir_path):
	for dir in dirs:
		for file in files:
			if file.endswith('.mp4'):
				test_string = file.split(".")[0]
				temp = re.findall(r'\d+', test_string)
				ary.append(temp)
				flatten_list = list(deepflatten(ary))
				flattened = [int(e) for e in flatten_list]	
				sorted_list_biggest=sorted(flattened)[-1]

counter = sorted_list_biggest + 1

if os.path.exists("output%d.%s"%(sorted_list_biggest, video_format)):
    result["video_name"] = "output%d.%s"%(counter, video_format)

object_to_be_modified_for_video_name = cv2.VideoWriter(result["video_name"], result["codec"], result["fps"], result["total_size"]) 

start_time = time.time()
# while capture.isOpened():
while( int(time.time() - start_time) < capture_duration ):

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


result.release()
cv2.destroyAllWindows()

