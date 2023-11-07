#! /usr/bin/env python3

import cv2, os
from cv_star_sensor.test.boxmerge import combine_boxes

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
  # ***
  #  levelWeights are rejectLevels' weights . . .
  #  I'm not sure this is what is intended
  # ***
  stars, rejectLevels, levelWeights = stars_cascade.detectMultiScale3(
    img,
    scaleFactor = 1.05,
    minNeighbors = int(minn),
    flags = 0,
    minSize = (300, 300),
    maxSize = (400, 400),
    outputRejectLevels = True
    )

  print(f'Cascade number {cascade}, ({ra},{dec}), ', end='')
  #Track new boxes
  box = []
  #The purpose of this if statement is to see if any detection has been made.
  if len(stars) > 0:
    #highweight = 0
    maxsize = 0
    for i, (x,y,w,h) in enumerate(stars):
      #This if statement will find the detection with the largest bounding box.
      #if levelWeights[i] > highweight:
      #  highweight = levelWeights[i]
      if w*h > maxsize:
        maxsize = w*h
        weighted = levelWeights[i]*sf
        x0 = x
        y0 = y
        x1 = x+w
        y1 = y+h

    #Sets the levelWeights value bounds for a 'successful' detection.
    if weighted > 4 and weighted < 6:
      label = f'{cascade}, {round(weighted,2)}: {(x0+x1)//2}, {(y0+y1)//2}'
      box = [(label,x0,y0,x1,y1)]
      print('DETECTS\n')
    else:
      print(f'POOR DETECTION {round(weighted,2)}\n')
  else:
    print('NO DETECTION\n')
  return box

def runtest(imgname):
  img = cv2.imread(imgname) if type(imgname) is str else imgname
  boxes = []
  #Run the detection function for each cascade file
  for directory in cascades:
    for xmlname in os.listdir(directory):
      parts = xmlname[:-4].split(',')
      if len(parts) != 5:
        continue
      boxes += stardetection(*parts,
                              os.path.sep.join([directory,xmlname]),
                              img)
  boxes = combine_boxes(img, boxes)
  #boxes[i] = (label,x0,y0,x1,y1)
  for i, box in enumerate(boxes):
    if not box:
      continue
    if len(box) == 3:
      for j, line in enumerate(box[0].split('\n')):
        cv2.putText(img,
                    line,
                    (box[1], box[2] + 44 - 28*(j+2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0,0,255), 2,
                    cv2.LINE_AA)
    else:
      cv2.putText(img,
                  box[0],
                  (box[1], box[2] - 16*(box[0].count('\n')+1)),
                  cv2.FONT_HERSHEY_SIMPLEX,
                  0.9, (0,0,255), 2,
                  cv2.LINE_AA)
      cv2.rectangle(img, (box[1],box[2]), (box[3],box[4]), (0,255,0), 2)
  shrunk_img = cv2.resize(img, (1344, 756))
  cv2.imshow("Star Pattern Detections", shrunk_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

