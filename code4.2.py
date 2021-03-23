##Student Research Project
##Image Processing
##Contactless fingerprint capturing
##
##using opencv  and python 2.7.5
##December 2019
##Mahesh M Dhananjaya


from __future__ import print_function
import cv2 as cv
import numpy as np
import random as rng

while True:


    max_value = 255
    low_H = 0
    high_H = max_value
    window_capture_name = 'Video Capture'
    window_detection_name = 'Object Detection'
    low_H_name = 'Low H'
    high_H_name = 'High H'

    ##Track bar for thresholding the mask
    def on_low_H_thresh_trackbar(val):
        global low_H
        global high_H
        low_H = val
        low_H = min(high_H-1, low_H)
        cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
    def on_high_H_thresh_trackbar(val):
        global low_H
        global high_H
        high_H = val
        high_H = max(high_H, low_H+1)
        cv.setTrackbarPos(high_H_name, window_detection_name, high_H)

    cap = cv.VideoCapture(0)
    cv.namedWindow(window_capture_name)
    cv.namedWindow(window_detection_name)
    cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value, on_high_H_thresh_trackbar)

    while True:

        ##capturing video : each frame of the hand
        _, frame = cap.read()
        if frame is None:
            break
        ##basic smoothing filter to reduce the no of blobs further
        frame = cv.medianBlur(frame,5)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        ##skin tone detection algo
        new = frame.copy()
        new[:,: ,2] =0
        new1 = new.max(2)
        new1 = gray - new1  

        ##choice between trackbar or the skin probability
        frame_threshold = cv.inRange(new1, (low_H), (high_H))
        #frame_threshold = cv.inRange(new1, (5), (35))
        frame_threshold1 = frame_threshold.copy()


        ##find the contours of the mask 
        _,contours, hierarchy = cv.findContours(frame_threshold1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            
        contours_poly = [None]*len(contours)
        boundRect = [None]*len(contours)
        minRect = [None]*len(contours)
        ##creates a polygon, rect and rotated rect around each countour
        for i, c in enumerate(contours):
            contours_poly[i] = cv.approxPolyDP(c, 3, True)
            boundRect[i] = cv.boundingRect(contours_poly[i])
            minRect[i] = cv.minAreaRect(contours_poly[i])
            

        
        
        drawing = np.zeros((frame_threshold1.shape[0], frame_threshold1.shape[1], 3), dtype=np.uint8)

        ##select the largest blob of the captured image on the assumption that it is the hand 
        largest_contour = 0
        for c in range(len(contours)):
            if (cv.contourArea(contours[c]) > cv.contourArea(contours[largest_contour])):
                largest_contour = c

               # cv.rectangle(drawing, (int(boundRect[c][0]), int(boundRect[c][1])), \
               #   (int(boundRect[c][0]+boundRect[c][2]), int(boundRect[c][1]+boundRect[c][3])), color, 2)
               
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours_poly, largest_contour , color)
        box = cv.boxPoints(minRect[largest_contour])
        box = np.intp(box)
        cv.drawContours(drawing, [box], 0, color, 2)

        cnt = contours[largest_contour]

        cv.imshow('Contours1', drawing)
         
        cv.imshow(window_capture_name, frame)
        cv.imshow(window_detection_name, frame_threshold)
        
        
        ##region of intrest of only the hand is cropped for further analysis
        x, y, width, height = boundRect[largest_contour]
        roi = frame_threshold[y:y+height, x:x+width]
        #cv.imwrite("roi.png", roi)
        roi1 = frame[y:y+height, x:x+width]
        #cv.imwrite("roi1.png", roi1)
        #cv.destroyAllWindows()

        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            cap.release()
            #cv.destroyAllWindows()
            break
        




    img = roi.copy()
    img1 = roi1.copy()
    
    imgcopy = img.copy()
    height, width = img.shape


    ##finger seperation from the palm
    img[ height/4 : height/4+5,:] = 0

    _,contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    maxcnt = len(contours)
    while True :
        height = height + 5
        img = imgcopy.copy()
        img[ height/4 : height/4+5,:] = 0
        #cv.imshow('roi', img)
        #cv.imwrite("roi3.png", img)
        _,contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if (len(contours) != maxcnt):
            #img[ height/4 : ,:] = 0
            #_,contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            break

    ##contours and rotated rect are drawn acound each finger and palm
    contours_poly = [None]*len(contours)
    minRect = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        minRect[i] = cv.minAreaRect(contours_poly[i])

    ##reduce the finger rotated tect to the tip fingerprint region
    drawing1 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for c in range(len(contours)):
        if (cv.contourArea(contours[c]) > 500) :
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            box = cv.boxPoints(minRect[c])
            box = np.intp(box)
            cv.drawContours(drawing, [box], 0, color, 2)
            length = np.linalg.norm(box[0] - box[1])
            width = np.linalg.norm(box[0] - box[3])
        #scale = 3
            if (length > width) :
                scale = length / (1.6*width)
                box[0] =  ((scale-1)*box[1] + box[0])/scale
                box[3] =  ((scale-1)*box[2] + box[3])/scale
            if (width >= length ) :
                scale = width / (1.6*length)
                box[1] =  ((scale-1)*box[2] + box[1])/scale
                box[0] =  ((scale-1)*box[3] + box[0])/scale
            cv.drawContours(img1, [box], 0, color, 2)
            cv.drawContours(drawing1, [box], 0, color, 2)


    cv.imshow('Contour', img1)


    cv.imshow('Contours', drawing1)

    #cv.imwrite("roi2.png", drawing)
    #cv.imwrite("roi4.png", img1)


    while True:
        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
       # cap.release()
            cv.destroyAllWindows()
            break
        
