#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install easyocr')
get_ipython().system('pip install imutils')


# In[213]:


import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import os


# In[307]:


img = cv2.imread('image2.jpeg')
# change color of picture (BGR to GRAY)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2 accepts image in RGB
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))


# In[308]:


bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # noise reduction
edged = cv2.Canny(bfilter, 20, 200) # edge detection
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))


# In[309]:


plt.imshow(cv2.cvtColor(bfilter, cv2.COLOR_BGR2RGB))


# In[310]:


# try to find shape, try to find contour with four point
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]


# In[311]:


location = None
for contour in contours:
  approx = cv2.approxPolyDP(contour, 10, True)
  if len(approx) == 4:
    location = approx 
    break


# In[312]:


location


# In[313]:


# first created a blank mask as same shape as original gray image
mask = np.zeros(gray.shape, np.uint8)
# draw our contours within that image so to that we have passed through our temporary image which is our mask and specified what contour we want to draw
new_image = cv2.drawContours(mask, [location], 0, 255, -1)
# then we overlayed that mask over our original image
new_image = cv2.bitwise_and(img, img, mask = mask)


# In[314]:


plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))


# In[315]:


# we start with finding out every single section where our image isnt black, we are storing those in variables x and y
(x,y) = np.where(mask == 255)
# then we grabbed the minimum x value and minimum y value to ideally get this point up here
(x1,y1) = (np.min(x), np.min(y))
# then we grabbed the maximum x value and maximum y value to ideally get this point up here
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1 : x2 + 1, y1:y2+1]


# In[316]:


plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))


# In[317]:


reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
result


# In[318]:


num = result[0][1]
num = num.replace(" ", "")
print(num)


# In[322]:


import mysql.connector


# In[324]:


mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "Rohitsh@rm@23",
database = "vehicle"
)


# In[325]:


print(mydb)


# In[326]:


cursor = mydb.cursor(buffered=True)


# In[320]:


cursor.execute("CREATE DATABASE vehicleVerification")


# In[330]:


cursor.execute("CREATE TABLE NumberPlateVerification (name VARCHAR(255), plateno VARCHAR(255), phoneno VARCHAR(255))")


# In[331]:


# sql = "DROP TABLE vehicledetails"


# In[333]:


# cursor.execute(sql)


# In[334]:


sql = "INSERT INTO NumberPlateVerification (name, plateno, phoneno) VALUES (%s, %s, %s)"
val = ("Yash", "MH20DV2363", "9759754343")
cursor.execute(sql, val)


# In[336]:


mydb.commit()


# In[337]:


sql = "INSERT INTO NumberPlateVerification (name, plateno, phoneno) VALUES (%s, %s, %s)"
val = ("Garvit", "MHOZEP1543", "9759754343")
cursor.execute(sql, val)


# In[338]:


mydb.commit()


# In[340]:


cursor.execute("SELECT PHONENO FROM NumberPlateVerification where plateno = '" + num + "'")


# In[341]:


myResult = cursor.fetchall()


# In[342]:


print(myResult)


# In[343]:


import requests


# In[346]:


url = 'https://www.fast2sms.com/dev/bulkV2'
message = 'Greeting From Yash Chauhan'
payload = f'sender_id=TXTIND&message=${message}&route=V3&language=english&numbers=${myResult}'

headers = {
    'authorization' : 'JuNmPITACKGwRikU1sWDcyh9BYaEjfSXz3QgxdnL4t2vOqrVeb5r6JoQF1geNbSPxikl7GvY9UXLIEKy',
    'Content-type' : 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url = url, data = payload, headers = headers)


# In[347]:


print(response.text)


# In[ ]:





# In[ ]:




