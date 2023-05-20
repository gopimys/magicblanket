import cv2
import numpy as np
import time
  
# goal is to replace the red pixels ( or undesired area ) with background pixels to generate the invisibility feature.
   
# in order to check the cv2 version
print(cv2.__version__)   
  
# set path of cam footage or 0 to get feed from webcam
capture_video = cv2.VideoCapture(0)
  
# give the camera to warm up
time.sleep(1) 
count = 0 
background = 0 
  
# capturing the background in range of 60

for i in range(60):
    return_val, background = capture_video.read()
    if return_val == False :
        continue 
  
background = np.flip(background, axis = 1) # flipping of the frame 
  
# we are reading from video 
while (capture_video.isOpened()):
    return_val, img = capture_video.read()
    if not return_val :
        break 
    count = count + 1
    img = np.flip(img, axis = 1)
  
    # convert the image - BGR(An RGB color space is defined by: Chromaticity coordinates of the red, green, and blue additive primaries.) 
    # to HSV((hue, saturation, value)) as we focused on detection of red color 
    # converting BGR to HSV for better detection or you can convert it to gray
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
  
    #-------------------------------------BLOCK----------------------------#
    # ranges should be carefully chosen
    # setting the lower and upper range for mask1
    lower_red = np.array([100, 40, 40])       
    upper_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # setting the lower and upper range for mask2
    lower_red = np.array([155, 40, 40])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    #----------------------------------------------------------------------#
  
    # the above block of code could be replaced with
    # some other code depending upon the color of your cloth 
    mask1 = mask1 + mask2
  
    # Refining the mask corresponding to the detected red color
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                         np.uint8), iterations = 2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1)
    mask2 = cv2.bitwise_not(mask1)
  
    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
  
    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
     # Press ESC to exit
    if k == 27:
        break
    
