# CV-Star-Sensor

# Forked from https://github.com/raspberrystars/CV-Star-Sensor

## Repo usage 

To use *driver.py* in the top-level directory:
- The directory name should be cv_star_sensor, as the repo, to locate scripts

./driver.py
- Specify 1 or more negative sets to use (default neg_southern2)  
`python3 driver.py --negatives neg_southern2,neg_sports`  
The negatives would be used in training
- Disable erosion of image (removal of some less bright stars) in processing  
`python3 driver.py --noerode`  
This is mentioned to have been done in a later step
- Specify test (input) image  
`python3 driver.py --test=stellarium/images/check001.png`  
This will add fiducial markers to the image  
then run all cascades on the image, reporting statistics  
the final image will be displayed

./data/
- The negatives folder contains archives and a script to decompress them
- The negatives script can be ran directly or from driver.py
- The positives folder contains a script to put fiducial markings on an image
- The marking script optionally erodes the image (as in the source paper)
- The marked image can be saved, a small cropped image can be saved
- The marked image (as a cv2 image object) is returned

./stellarium/
- Folder contains the Stellarium scripts from the original repo
- Stellarium scripts modified for stellarium version
- Stellarium script modifications are within a comment section

./test/
- cascades folder contains saved trained model parameters for cv classifiers
- detect.py contains a function, runtest, which takes a cv2 image or filename
- The image should be one marked by the ./data/positives/ script
- For each cascade, identified star regions are marked

# Welcome to you if you're coming from Instructables!

## MSc Project repo for computer vision star identification and satellite orientation project (CURRENTLY ACTIVE)

Please see a short explanatory video on [YouTube](https://www.youtube.com/watch?v=aYilzSxmrGo).

Additionally, this [tutorial](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/) is a really useful beginner's guide to OpenCV classifier training.

**Contents so far:**
- Stellarium scripts used to capture thousands of images from Stellarium in order to be processed into negative image datasets for machine learning training.
- Zipped folders containing negative image datasets, as well as bg.txt files, and python programs used to create these.
- Python programs used to create the positive images used for cascade training. 
- Image files of the fiducial markers applied to starfields, to identify the patterns of bright stars that the machine learning relies upon for the identification.
- A sample set of 31 trained cascades for the northern celestial hemisphere.
- Python programs used to test the trained cascades against a supplied starfield image.

**What next?:**

19/08/19, I have finished working on this project as part of my University course. I hope to be able to spend further time on it as a hobby in order to keep developing the system, there are lots of improvements and additions I would like to have time to make. I hope that this repository may be of use to someone, and if you have questions please contact me, I will continue to monitor and work on this project. The best source of reference here is my MSc Thesis itself, which can be found above.

25/05/20, I've been putting more thought into the potential improvement and applications of this project. I hope that the Instructables writeup will help other people find this repo, and hopefully we can work together to develop this further!
