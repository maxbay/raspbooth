#!/usr/local/bin/python
import os
import time
import cv2
import numpy as np

class Capture():
    def __init__(self):
        self.c = cv2.VideoCapture(0)

    def startCapture(self):

        self.capturing = True #fall into while loop
        cap = self.c

        DELAY = 6
        FAUX_FLASH = 30
        epoch_time = np.int(time.time())

        snap1 = epoch_time + DELAY + 5
        snap2 = snap1 + DELAY
        snap3 = snap2 + DELAY
        snap4 = snap3 + DELAY
        snap_lst = [snap1, snap2, snap3, snap4]
        take_snap = [True, True, True, True]
        snap_count = 0

        HOME_DIR = os.path.expanduser('~')
        snaps_dir = os.path.join(HOME_DIR,'Desktop/tmp_photos',str(epoch_time))

        while(self.capturing):


            ret, frame = cap.read()

            gray = Capture.cropVideo(frame) # crops video into 3:4 ratio
            gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY) # converts to gray
            gray = cv2.flip(gray,1) # flips to create mirrior image
            gray_copy = gray # unmanipulated copy for writing to disk

            FONT = cv2.FONT_HERSHEY_COMPLEX # font
            SCALE = 2 # pt size
            THICKNESS = 5 # boldness factor

            cur_time = time.time() # time of instance, float
            cur_time_int = int(cur_time) # instance of time, discretized

            if cur_time > snap_lst[snap_count]: # advances snap count if current time > end of previous snap period
                snap_count += 1


            remaining_float = snap_lst[snap_count] - cur_time - 1 # time remaining in snap period, used for flash taking snap
            remaining = snap_lst[snap_count] - cur_time_int - 1 # int of time remaining, used for display

            if remaining <= 1: # displays remaining time on screen, but last two seconds "SMILE!" is displayed
                text = "SMILE!"
            else:
                text = str(remaining)

            if remaining_float > 0 and remaining_float < .25: # increase image values to make fake flash
                gray = np.array(np.add(gray,FAUX_FLASH)).astype(np.uint8)

                if take_snap[snap_count]: # check if picture for this snap period needs to be taken, if so...

                    if not os.path.exists(snaps_dir): # make dir for all 4 pictures if it has not been created yet
                        os.makedirs(snaps_dir)
                    file_name = os.path.join(snaps_dir,"test_image{0}.tif".format(str(snap_count + 1)))
                    cv2.imwrite(file_name,gray_copy) # write picture to disk
                    take_snap[snap_count] = False #indicate that picture has been taken, and another for this snap period not needed

                    if snap_count == len(snap_lst) - 1: # breaks from while loop if snap count > scheduled snaps
                        self.capturing = False

                    print(str(snap_count))

            mid_x, mid_y = Capture.findCenter(gray,text,FONT,SCALE,THICKNESS) # find x, y values in image to display text
            cv2.putText(gray,text,(mid_x,mid_y),FONT,SCALE,(255,255,255),THICKNESS) # insert text at x, y
            cv2.imshow("CaptureFrame", gray) # display image with text
            cv2.waitKey(5)



        cv2.destroyAllWindows() # exit from display window

    def printBtn(self):
        print "Pressed Btn"

    @staticmethod
    def findCenter(array, text, FONT, SCALE, THICKNESS): # values for x, y such that text is centered
        x = np.size(array[0,:])
        y = np.size(array[:,0])

        half_width = np.int(np.round(cv2.getTextSize(text,FONT,SCALE,THICKNESS)[0][0]/2,0))
        mid_x = np.int(np.round(x/2,0) - half_width)
        mid_y = np.int(np.round(y/2,0))

        return mid_x, mid_y # x value, y value

    @staticmethod
    def cropVideo(array): #crops video to 3:4 ratio

        width = np.int(np.size(array[0,:])/3)
        height  = np.int(np.size(array[:,0])/3)
        target_width = np.int((height * .75))
        start  = np.int((width/2) - (target_width/2))
        end    = np.int((width/2) + (target_width/2))

        array = array[:,start:end]

        return array

    """
    def quitCapture(self):
        print "pressed Quit"
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()
        """
