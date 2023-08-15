import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

def image_to_plateNumber(img):
    # change color of picture (BGR to GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # noise reduction
    edged = cv2.Canny(bfilter, 20, 200) # edge detection

    # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
    # plt.show()

    # plt.imshow(cv2.cvtColor(bfilter, cv2.COLOR_BGR2RGB))
    # plt.show()

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, 
		cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    
    location = None
    for contour in contours:
      approx = cv2.approxPolyDP(contour, 10, True)
      if len(approx) == 4:
        location = approx 
        break
    # print(location)
    
    # first created a blank mask as same shape as original gray image
    mask = np.zeros(gray.shape, np.uint8)
    # draw our contours within that image so to that we have passed through our temporary image   
        which is our mask and specified what contour we want to draw
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    # then we overlayed that mask over our original image
    new_image = cv2.bitwise_and(img, img, mask = mask)
        
    # plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
    # plt.show()

    # we start with finding out every single section where our image isnt black, we are storing  
       those in variables x and y
    (x,y) = np.where(mask == 255)
    # then we grabbed the minimum x value and minimum y value to ideally get this point up here
    (x1,y1) = (np.min(x), np.min(y))
    # then we grabbed the maximum x value and maximum y value to ideally get this point up 
       here
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1 : x2 + 1, y1:y2+1]

    # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    # plt.show()

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    num = result[0][1]
    num = num.replace(" ", "")
    return num

image_filepath = 'image2.jpg'

img = cv2.imread(image_filepath)

plate_number = image_to_plateNumber(img)

print("Number plate = ", plate_number)

