## Description of these programs and files

**get_descriptor.py** - this is used to generate the bg.txt file that is required for the cascade training.

**neg_northern.zip** - contains the neg images of the northern celestial hemisphere and bg.txt file generated using neg_process4.py from images captured in Stellarium using one of the Stellarium scripts provided in this repository. These negative images are largely unaltered.

**neg_northern2.zip** - contains the neg images of the northern celestial hemisphere and bg.txt file generated using neg_process5.py from images captured in Stellarium using one of the Stellarium scripts provided in this repository. Extra processes were applied to the star images to produce these negatives including removing small stars and enlarging the prominent stars.

**neg_process4.py** - produces basic negative images from Stellarium captures. It is run on Windows 10. The program reads them, crops them, greyscales them, shrinks them to 100x100 pixels, and then saves them as a new file.

**neg_process5.py** - produces processed negative images from Stellarium captures. Same as neg_process4 but processes the images to remove small stars and exaggerate prominent ones. 

**neg_southern.zip** - contains the neg images of the southern celestial hemisphere and bg.txt file generated using neg_process4.py from images captured in Stellarium using one of the Stellarium scripts provided in this repository. These negative images are largely unaltered.

**neg_southern2.zip** - contains the neg images of the southern celestial hemisphere and bg.txt file generated using neg_process5.py from images captured in Stellarium using one of the Stellarium scripts provided in this repository. Extra processes were applied to the star images to produce these negatives including removing small stars and enlarging the prominent stars.

**neg_sports.zip** - contains almost 2000 images of general sports scenes taken originally from the ImageNet database. ImageNet was undermaintenance at the time of writing this, so this set of images was downloaded from this [OpenCV Tutorial](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/).

**negatives_plus.zip** - contains a much larger dataset of 5010 images, merging neg_sports with additional images collected by raspberry stars. Also includes bg.txt file needed.

**negatives_huge.zip** - the largest dataset I experimented with, contains 8898 images. Merges negatives_plus with some additional images from Stellarium with fiducial markers. Also includes required bg.txt file.
