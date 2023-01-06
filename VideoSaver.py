

# This file is just a trial to show myself that
# even the numpy array saving of a video is not feasible
# in the long term when considering scalibility.
import numpy as np

ary = []
total = []
def VideoSaver(vid):
    print(np.array(vid))
	# create a numpy 1d-array
    x = np.array(vid)
 
    print("Size of the array: ", x.size)

    print("Memory size of one array element in bytes: ", x.itemsize)
 
    # memory size of numpy array in bytes
    print("Memory size of numpy array in bytes:", x.size * x.itemsize)
    #total.append(arr)
    #return len(ary)
