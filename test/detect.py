#Import required libraries
import cv2, os
import numpy as np

cascade_dirs = ['cascades']

#Load an input test image (which has had fiducial markers applied).
#In practice an image would be received from the RPi camera and markers applied.
img = cv2.imread(os.environ['HOME']+'/git/CV-Star-Sensor/stellarium/images/check579.png')

#Create a detection function.
def stardetection(cascade, ra, dec, minn, sf, xmlname):
  #Specifies the cascade file to be loaded.
  stars_cascade = cv2.CascadeClassifier(xmlname)

  #Applies the detectMultiScale3 function with the appropriate parameters.
  stars, rejectLevels, levelWeights = stars_cascade.detectMultiScale3(
    img,
    scaleFactor = 1.05,
    minNeighbors = int(minn),
    flags = 0,
    minSize = (300, 300),
    maxSize = (400, 400),
    outputRejectLevels = True
    )

  #Create some additional variables = 0 for use in later 'for loops'.
  i = 0
  highweight = 0
  big_w = 0
  weighted = 0

  #The purpose of this if statement is to see if any detection has been made.
  if(len(stars) > 0):
    for (x,y,w,h) in stars:

      #This if statement will find the detection with the largest bounding box.
      if w > big_w:
        highweight = levelWeights[i]
        weighted = float(highweight)*float(sf)
        x1 = x
        y1 = y
        w1 = w
        h1 = h

    #The if statement below sets the levelWeights value bounds for a 'successful' detection.
    if (weighted > 4) and (weighted < 6):
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(img,cascade,(x1,y1-16), font,0.9,(0,0,255),2,cv2.LINE_AA)
      cv2.putText(img,str(weighted),(x1,y1+h1+25), font,0.7,(0,0,255),2,cv2.LINE_AA)
      cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
      cenpixx = int(x1 + 0.5 * w1)
      cenpixy = int(y1 + 0.5 * h1)
      cv2.putText(img,str(cenpixx)+', '+str(cenpixy),(x1,y1-45), font,0.9,(0,0,255),2,cv2.LINE_AA)
      shrunk_img = cv2.resize(img, (1344, 756))
      cv2.imshow("Star Pattern Detections",shrunk_img)
      print(f'Cascade number {cascade} DETECTS:', end='')
      # position and RA/Dec coordinate
      print(f'({cenpixx},{cenpixy}), ({ra},{dec})')
      print(weighted, end='\n\n')
    else:
      print(f'Cascade number {cascade} POOR DETECTION')
      print(weighted, end='\n\n')
  else:
    print('Cascade number '+cascade+' NO DETECTION', end='\n\n')

#Runs the detection function for each cascade file within the specified folder.
for directory in cascade_dirs:
  for xmlname in os.listdir(directory):
    parts = xmlname[:-4].split(',')
    if len(parts) != 5:
      continue
    stardetection(*parts, os.path.sep.join([directory,xmlname]))

