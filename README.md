# Contactless-fingerprint-capturing
Segmenting fingertips for finger print scanning

Skin colour based hand segmentation!
Reference:
A. Cheddad , J. Condell, K. Curran, and P. McKevitt . “A new colour space for skin tone detection.” IEEE International Conference on Image Processing (ICIP) ICIP), 2009 16th, pages 497 500, Nov 2009.

Program algorithm:
1. Capturing the image from the camera.
2. Image Smoothing: using median filter to reduce the number of blobs after thresholding.
3. Create bounding boxes around each fingertip

Next Steps:
1. enhance the quality of the finger tip
2. compare the fingerprints with the database.


Skintone Thresholding using the reference paper:
1. Set the red colour matrix to zero and create a new matrix with the largest values from green or Blue colour.
2. Create another matrix which is the Gray scale of the captured image.
3. Determine the error matrix which is the difference of the above two matrix.
4. According to the skin probability map – the boundaries of skin colour is between 0.02511 and 0.1177  or 6 and 30 (uint type).
5. Threshold the error matrix using the above values. i.e
  1 if	 0.02511 <= e(x) <= 0.1177
  0	otherwise
6. Fine adjustments can be done using a track bar.

Sample output:

roi and roi1:
Filtering the blobs after thresholding:
The area of all the blobs are calculated and the largest area is selected, on the assumption that the hand is the largest blob of the captured image.
The region of interest of this hand blob is cropped and used for further analysis.

roi2 and roi3:
The Region of interest contains both fingers and palm. To differentiate between the fingers and the palm, a black line is drawn across the image which divides the palm and the fingers.

roi4:
To extract the fingerprint a rectangle is created at the tip of the finger with the length = 1.5 times the width of the finger.


