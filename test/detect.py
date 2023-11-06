#! /usr/bin/env python3

import cv2, os

thisdir = os.path.realpath(__file__).split(os.path.sep)[:-1]
cascades = ['cascades']
cascades = [os.path.sep.join(thisdir+[cascade]) for cascade in cascades]

#Load an input test image (which has had fiducial markers applied).
#In practice images would be received from the RPi camera and markers applied.

#Detection function.
def stardetection(cascade, ra, dec, minn, sf, xmlname, img):
  sf = float(sf)
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

  #The purpose of this if statement is to see if any detection has been made.
  if len(stars) > 0:
    highweight = 0
    for i, (x,y,w,h) in enumerate(stars):
      #This if statement will find the detection with the largest bounding box.
      if levelWeights[i] > highweight:
        highweight = levelWeights[i]
        weighted = highweight*sf
        x0 = x
        y0 = y
        x1 = x+w
        y1 = y+h

    #Sets the levelWeights value bounds for a 'successful' detection.
    if weighted > 4 and weighted < 6:
      #Bounding box: x0,y0 to x1,y1
      #Center pixels: x and y = cenpixx, cenpixy
      cenpixx = (x0+x1)//2
      cenpixy = (y0+y1)//2
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(img,
                  f'{cascade}, {round(weighted,2)}: {cenpixx}, {cenpixy}',
                  (x0,y0-16),
                  font,0.9,(0,0,255),
                  2,
                  cv2.LINE_AA)
      cv2.rectangle(img, (x0,y0), (x1,y1), (0,255,0), 2)
      print(f'Cascade number {cascade} DETECTS: ', end='')
      # position and RA/Dec coordinate
      print(f'({cenpixx},{cenpixy}), ({ra},{dec})')
      print(weighted, end='\n\n')
    else:
      print(f'Cascade number {cascade} POOR DETECTION')
      print(weighted, end='\n\n')
  else:
    print(f'Cascade number {cascade} NO DETECTION', end='\n\n')

def runtest(imgname):
  img = cv2.imread(imgname) if type(imgname) is str else imgname
  #Run the detection function for each cascade file
  for directory in cascades:
    for xmlname in os.listdir(directory):
      parts = xmlname[:-4].split(',')
      if len(parts) != 5:
        continue
      stardetection(*parts, os.path.sep.join([directory,xmlname]), img)
  shrunk_img = cv2.resize(img, (1344, 756))
  cv2.imshow("Star Pattern Detections", shrunk_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

