from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import cv2
import matplotlib
from VideoSaver import VideoSaver as saver
import os
from VideoSaverSqlAlchemy import DatabaseInformation as DI

counter1 = 0
counter2 = 0
simlarityIndex = []

EXT = ".mp4"
DEFAULT_VIDEONAME1 = "trial1"+EXT
DEFAULT_VIDEONAME2 = "trial2"+EXT

# Load a video from file
videoname1 = input("Enter name of first video file - do not Enter .mp4 format - default is trial1.mp4: ")
out, ext1 = os.path.splitext(videoname1)
if videoname1 == "":
    videoname1 = DEFAULT_VIDEONAME1
elif ext1 != "":
	 videoname1 = out + ext1 
else:
	ext1 == ""
	videoname1 = out + EXT 

#print(videoname1.split(".")[:-1][0])

DI.getInfo(videoname1.split(".")[:-1][0], ext1)
capture1 = cv2.VideoCapture(videoname1)

amount_of_frames1 = capture1.get(cv2.CAP_PROP_FRAME_COUNT)
#print(amount_of_frames1)
videoname2 = input("Enter name of second video file - do not Enter .mp4 format - default is trial2.mp4: ")
out, ext2 = os.path.splitext(videoname2)
if videoname2 == "":
    videoname2 = DEFAULT_VIDEONAME2
elif ext2 != "":
	videoname2 = out + ext2 
else:
	ext2 == ""
	videoname2 = out + EXT 

#print(videoname1.split(".")[:-1][0])
DI.getInfo(videoname2.split(".")[:-1][0], ext2)
capture2 = cv2.VideoCapture(videoname2)

amount_of_frames2 = capture1.get(cv2.CAP_PROP_FRAME_COUNT)
#print(amount_of_frames2)


while amount_of_frames1 >= 1 and amount_of_frames2 >= 1:
#while True: 
    #print("amount_of_frames1", amount_of_frames1)
    #print("amount_of_frames2", amount_of_frames2)
    # capture frame-by-frame from video file
    ret, frame1 = capture1.read()
    ret, frame2 = capture2.read() 
        
    img_np1 = np.squeeze(frame1)
    img_np2 = np.squeeze(frame2)
    outcome = ssim(img_np1, img_np2, channel_axis=2)
    # print(simlarityIndex)
    simlarityIndex.append(outcome)
    # similarity index denotes how much your images are similar, 
    # the greater the values the similar the images.

	# show the frame on the screen
    winname1 = "Video1"
    cv2.namedWindow(winname1)        # Create a named window
    cv2.moveWindow(winname1, 40, 10)
    cv2.imshow(winname1, frame1)
    
    winname2 = "Video2"
    cv2.namedWindow(winname2)        # Create a named window
    cv2.moveWindow(winname2, 850, 10)
    cv2.imshow(winname2, frame2)
    
    amount_of_frames1 = amount_of_frames1 - 1
    amount_of_frames2 = amount_of_frames2 - 1  

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

mean = np.mean(simlarityIndex)

bigger_than_average = np.count_nonzero(np.asarray(simlarityIndex) > 0.5)

#v=[]
#n=range(0, 241, 2)
#for m in n:
#	j = m/100
#	v.append(j)

plt.xlabel('Video1')
plt.xticks([0.2, 0.4, 0.6, 0.8, 1.0])
plt.ylabel('Video2')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])
plt.annotate('mean number: ' +str(mean), xy=(mean, mean), xytext=(mean,mean),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.title(str(bigger_than_average) + " frames are above 0.5 average similarity of 1.0 whole point.")
print("simlarityIndex: ", len(simlarityIndex))
print("mean ", mean)
plt.bar(simlarityIndex, simlarityIndex) 
thismanager = plt.get_current_fig_manager()
thismanager.window.wm_geometry("+400+500")
# https://stackoverflow.com/questions/7449585/how-do-you-set-the-absolute-position-of-figure-windows-with-matplotlib


plt.show()


capture1.release()
capture2.release()
cv2.destroyAllWindows()
