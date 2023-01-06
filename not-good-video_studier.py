import cv2
from get_background import get_background
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import matplotlib

counter1 = 0
counter2 = 0
simlarityIndex = []

# Load a video from file
videoname1 = input("Enter name of first video file - do not Enter .mp4 format - default is output4.mp4: ")
if videoname1 == "":
	videoname1 = "output4"
cap1 = cv2.VideoCapture(videoname1+".mp4")
amount_of_frames1 = cap1.get(cv2.CAP_PROP_FRAME_COUNT)
videoname2 = input("Enter name of second video file - do not Enter .mp4 format - default is output5.mp4: ")
if videoname2 == "":
	videoname2 = "output5"
#consecutive_frame = input("Enter the consecutive_frame: ")
#if consecutive_frame == "":
#	consecutive_frame = 1
cap2 = cv2.VideoCapture(videoname2+".mp4")
#amount_of_frames2 = capture1.get(cv2.CAP_PROP_FRAME_COUNT)
#print(amount_of_frames2)


# get the background model
background1 = get_background(videoname1+".mp4")
background2 = get_background(videoname2+".mp4")

# convert the background model to grayscale format
background1 = cv2.cvtColor(background1, cv2.COLOR_BGR2GRAY)
background2 = cv2.cvtColor(background2, cv2.COLOR_BGR2GRAY)

frame_count = 0
#consecutive_frame = consecutive_frames

while counter1 < 51:
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()

    if ret == True:
        frame_count += 1
        orig_frame1 = frame1.copy()
        orig_frame2 = frame2.copy()

	    # IMPORTANT STEP: convert the frame to grayscale first
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        #if frame_count % consecutive_frame == 0 or frame_count == 1:
        frame_diff_list1 = []
        frame_diff_list2 = []

		# find the difference between current frame and base frame
        frame_diff1 = cv2.absdiff(gray1, background1)

		# find the difference between current frame and base frame
        frame_diff2 = cv2.absdiff(gray2, background2)

	    # thresholding to convert the frame to binary
        ret, thres1 = cv2.threshold(frame_diff1, 50, 255, cv2.THRESH_BINARY)

	    # thresholding to convert the frame to binary
        ret, thres2 = cv2.threshold(frame_diff2, 50, 255, cv2.THRESH_BINARY)

	    # dilate the frame a bit to get some more white area...
	    # ... makes the detection of contours a bit easier
        dilate_frame1 = cv2.dilate(thres1, None, iterations=2)
        dilate_frame2 = cv2.dilate(thres2, None, iterations=2)


	    # append the final result into the `frame_diff_list`
        frame_diff_list1.append(dilate_frame1)
        frame_diff_list2.append(dilate_frame2)


	    # if we have reached `consecutive_frame` number of frames
        #if (len(frame_diff_list1) and len(frame_diff_list2)) == consecutive_frame:

        # add all the frames in the `frame_diff_list`
        sum_frames1 = sum(frame_diff_list1)

        # add all the frames in the `frame_diff_list`
        sum_frames2 = sum(frame_diff_list2)

        # find the contours around the white segmented areas
        contours1, hierarchy = cv2.findContours(sum_frames1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy = cv2.findContours(sum_frames2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
		# draw the contours, not strictly necessary
        for i, cnt in enumerate(contours1):
            cv2.drawContours(orig_frame1, contours1, i, (0, 0, 255), 3)
            img_np1 = np.squeeze(orig_frame1)

        for i, cnt in enumerate(contours2):
            cv2.drawContours(orig_frame2, contours2, i, (0, 0, 255), 3)
            img_np2 = np.squeeze(orig_frame2)

        outcome = ssim(img_np1, img_np2, channel_axis=2)
		# print(simlarityIndex)
        simlarityIndex.append(outcome)


		# show the frame on the screen
        winname1 = "Video1"
        cv2.namedWindow(winname1)        # Create a named window
        cv2.moveWindow(winname1, 40, 10)
        cv2.imshow(winname1, frame1)
		
        winname2 = "Video2"
        cv2.namedWindow(winname2)        # Create a named window
        cv2.moveWindow(winname2, 850, 10)
        cv2.imshow(winname2, frame2)
		
        counter1 = counter1 + 1
		
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    else:
        break

mean = np.mean(simlarityIndex)

bigger_than_average = np.count_nonzero(np.asarray(simlarityIndex) > 0.5)

v=[]
n=range(0, 101, 2)
for m in n:
	j = m/100
	v.append(j)

plt.xlabel('Video1')
plt.xticks([0.2, 0.4, 0.6, 0.8, 1.0])
plt.ylabel('Video2')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])
plt.annotate('mean number: ' +str(mean), xy=(mean, mean), xytext=(mean,mean),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.title(str(bigger_than_average) + " frames are above 0.5 average similarity of 1.0 whole point.")
plt.scatter(simlarityIndex, v, marker='o') 
thismanager = plt.get_current_fig_manager()
thismanager.window.wm_geometry("+400+500")
# https://stackoverflow.com/questions/7449585/how-do-you-set-the-absolute-position-of-figure-windows-with-matplotlib

plt.show()

cap1.release()
cap2.release()
cv2.destroyAllWindows()








"""
for contour in contours1:
    # continue through the loop if contour area is less than 500...
    # ... helps in removing noise detection
    if cv2.contourArea(contour) < 500:
        continue
    # get the xmin, ymin, width, and height coordinates from the contours
    (x, y, w, h) = cv2.boundingRect(contour)
    # draw the bounding boxes
    cv2.rectangle(orig_frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

for contour in contours2:
    # continue through the loop if contour area is less than 500...
    # ... helps in removing noise detection
    if cv2.contourArea(contour) < 500:
        continue
    # get the xmin, ymin, width, and height coordinates from the contours
    (x, y, w, h) = cv2.boundingRect(contour)
    # draw the bounding boxes
    cv2.rectangle(orig_frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
"""	
