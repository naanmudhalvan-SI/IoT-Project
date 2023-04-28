# importing necessary libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt

import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#Provide your IBM Watson Device Credentials
organization = "96ei56"
deviceType = "SQUID"
deviceId = "12333"
authMethod = "token"
authToken = "27042023"


def ibmstart(x):
    
    def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])
        print(cmd)

    try:
      deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
      deviceCli = ibmiotf.device.Client(deviceOptions)
      #..............................................
      
    except Exception as e:
      print("Caught exception connecting device: %s" % str(e))
      sys.exit()
    
    deviceCli.connect()
    lat=random.randint(9,37)
    long=random.randint(68,97)
    data = { 'latitude' : lat, 'longitude': long ,'Status': x}
    #data = { 'Status' : x}
    #print data
    def myOnPublishCallback():
        print ("Published Status = %s" % x, "to IBM Watson")

    success = deviceCli.publishEvent("SQUID", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
                
        
    deviceCli.commandCallback = myCommandCallback
    deviceCli.disconnect()
    

# read a cracked sample image
img = cv2.imread('Input Set/Cracked_07.jpg')
flag=0
# Convert into gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Image processing ( smoothing )
# Averaging
blur = cv2.blur(gray,(3,3))

# Apply logarithmic transform
img_log = (np.log(blur+1)/(np.log(1+np.max(blur))))*255

# Specify the data type
img_log = np.array(img_log,dtype=np.uint8)

# Image smoothing: bilateral filter
bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)

# Canny Edge Detection
edges = cv2.Canny(bilateral,100,200)

# Morphological Closing Operator
kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Create feature detecting method
# sift = cv2.xfeatures2d.SIFT_create()
# surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=1500)

# Make featured Image
keypoints, descriptors = orb.detectAndCompute(closing, None)
featuredImg = cv2.drawKeypoints(closing, keypoints, None)

# Create an output image
cv2.imwrite('Output Set/CrackDetected-7.jpg', featuredImg)
flag=1

# Use plot to show original and output image
plt.subplot(121),plt.imshow(img)
plt.title('Original'),plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(featuredImg,cmap='gray')
plt.title('Output Image'),plt.xticks([]), plt.yticks([])
print(flag)
ibmstart(flag)
plt.show()

