#! /usr/bin/env python3

import cv2, imutils, os, sys

thisdir = os.path.realpath(__file__).split(os.path.sep)[:-1]
thisdir = os.path.sep.join(thisdir)
fiducial_80x80 = os.path.sep.join([thisdir, 'fiducial_80x80.png'])
rectangle_black = os.path.sep.join([thisdir, 'rectangle_black.png'])

def markimg(imgname, savename=None, smallname=None, doerosion=True):
  #Load the fiducial marker
  #This image is a circular markers on a rectangular transparent background.
  fg_img = cv2.imread(fiducial_80x80, cv2.IMREAD_UNCHANGED)
  #Get the dimensions of the fiducial marker image.
  fg_height, fg_width = fg_img.shape[:2]
  #Handle the alpha channel of the fiducial marker image
  # needed for the transparency.
  alpha_s = fg_img[:, :, 3] / 255.0
  alpha_l = 1.0 - alpha_s

  #Load background star and black rectangle images.
  #The black rectangle is of the same resolution as bg_img.
  bg_img = cv2.imread(imgname)
  height, width = bg_img.shape[:2]
  rectangle = cv2.imread(rectangle_black)
  if (height, width) != rectangle.shape[:2]:
    rectangle = cv2.resize(rectangle, (width, height))

  #Enlarge bg_img to prevent erosion stage from removing too many stars.
  contours = cv2.resize(bg_img, (width*2, height*2))
  #Greyscale the enlarged background star image.
  contours = cv2.cvtColor(contours, cv2.COLOR_BGR2GRAY)
  #Threshold, erode, and dilate the stars on this image.
  contours = cv2.threshold(contours, 175, 255, cv2.THRESH_BINARY)[1]
  #Conditionally erode image
  if doerosion:
    contours = cv2.erode(contours, None, iterations=1)
  contours = cv2.dilate(contours, None, iterations = 2)
  #Resize back to original resolution.
  contours = cv2.resize(contours, (width, height))
  contours = cv2.findContours(contours,
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)

  rectangle_build = rectangle.copy()

  #For each identified contour (bright star)
  # applies a fiducial marker to that location.
  #Adds the fiducial markers to the black rectangle.
  for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    y1 = int((y + 0.5 * h) - 0.5 * fg_height)
    y2 = y1 + fg_height

    x1 = int((x + 0.5 * w) - 0.5 * fg_width)
    x2 = x1 + fg_width

    rectangle_temp = rectangle.copy()

    if y1 > 0 and y2 < height and x1 > 0 and x2 < width:
      for c in range(0, 3):
        rectangle_temp[y1:y2, x1:x2, c] = \
                    alpha_s * fg_img[:, :, c] + \
                    alpha_l * rectangle[y1:y2, x1:x2, c]

      rows,cols,channels = rectangle_temp.shape
      roi = rectangle_build[0:rows, 0:cols ]
      img2gray = cv2.cvtColor(rectangle_temp,cv2.COLOR_BGR2GRAY)
      ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
      mask_inv = cv2.bitwise_not(mask)
      img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
      img2_fg = cv2.bitwise_and(rectangle_temp,rectangle_temp,mask = mask)
      dst = cv2.add(img1_bg,img2_fg)
      rectangle_build[0:rows, 0:cols ] = dst

  #Merge the rectangular image with fiducial markers
  # onto the background sky image.
  rows,cols,channels = rectangle_build.shape
  roi = bg_img[0:rows, 0:cols ]
  img2gray = cv2.cvtColor(rectangle_build,cv2.COLOR_BGR2GRAY)
  ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
  mask_inv = cv2.bitwise_not(mask)
  img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
  img2_fg = cv2.bitwise_and(rectangle_build,rectangle_build,mask = mask)
  dst = cv2.add(img1_bg,img2_fg)
  bg_img[0:rows, 0:cols ] = dst

  #Specifies area of main image to crop for positive image.
  y=390
  x=810
  h=300
  w=300

  #Crop section of main image with markers, name it positive file and save.
  if smallname:
    crop_img = bg_img[y:y+h, x:x+w]
    grey_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    shrunk_img = cv2.resize(grey_img, (50, 50))
    cv2.imwrite(smallname, shrunk_img)

  if savename:
    #Name and create a test file
    # which cascades trained on this positive image can be checked against.
    big_image_name = savename
    cv2.imwrite(big_image_name, bg_img)

  # Return the marked image
  return bg_img

def print_usage():
  print('This script will mark an image with the fiducial markers')
  print('Usage:')
  print(f'python3 {sys.argv[0]} input.png output.png')
  print('The output image name is optional')
  print('If no output filename given output will be input_marked.png')

if __name__ == '__main__':
  if len(sys.argv) != 2 and len(sys.argv) != 3:
    print_usage()
    sys.exit(0)
  if not os.path.isfile(sys.argv[1]):
    print_usage()
    print(f'# {sys.argv[1]} is not a valid filename')
    sys.exit(1)
  outname = '.'.join(sys.argv[1].split('.')[:-1]) + '_marked.png' if \
            len(sys.argv) == 2 else sys.argv[2]
  markimg(sys.argv[1], savename=outname)

