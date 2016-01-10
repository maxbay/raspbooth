#!/usr/local/bin/python
import os
import time
import cv2
import numpy as np

class Capture():
    def __init__(self):
        self.c = cv2.VideoCapture(0)

    def startCapture(self):

        self.capturing = True
        cap = self.c

        DELAY = 6
        FAUX_FLASH = 75
        epoch_time = np.int(time.time())

        snap1 = epoch_time + DELAY + 5
        snap2 = snap1 + DELAY
        snap3 = snap2 + DELAY
        snap4 = snap3 + DELAY
        snap_lst = [snap1, snap2, snap3, snap4]
        take_snap = [True, True, True, True]
        snap_count = 0

        snaps_dir = os.path.join("/Users/maxwellbay/Desktop/tmp_photos",str(epoch_time))

        while(self.capturing):


            ret, frame = cap.read()

            gray = Capture.cropVideo(frame)
            gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
            gray = cv2.flip(gray,1)
            gray_copy = gray

            FONT = cv2.FONT_HERSHEY_SIMPLEX
            SCALE = 2
            THICKNESS = 5

            cur_time = time.time()
            cur_time_int = int(cur_time)

            if cur_time > snap_lst[snap_count]:
                snap_count += 1
            if snap_count > 3:
                cv2.destroyAllWindows()
                break

            remaining = snap_lst[snap_count] - cur_time_int - 1
            remaining_float = snap_lst[snap_count] - cur_time - 1

            if remaining <= 1:
                text = "SMILE!"
            else:
                text = str(remaining)

            if remaining_float > 0 and remaining_float < .25:
                gray = np.array(np.add(gray,FAUX_FLASH)).astype(np.uint8)

                if take_snap[snap_count]:

                    if not os.path.exists(snaps_dir):
                        os.makedirs(snaps_dir)
                    file_name = os.path.join(snaps_dir,"test_image{0}.tif".format(str(snap_count + 1)))
                    cv2.imwrite(file_name,gray_copy)
                    take_snap[snap_count] = False
                    print(file_name)

            mid_x, mid_y = Capture.findCenter(gray,text,FONT,SCALE,THICKNESS)
            cv2.putText(gray,text,(mid_x,mid_y),FONT,SCALE,(255,255,255),THICKNESS)
            cv2.putText
            cv2.imshow("CaptureFrame", gray)
            cv2.waitKey(5)

        cv2.destroyAllWindows()

    def printBtn(self):
        print "Pressed Btn"

    @staticmethod
    def findCenter(array, text, FONT, SCALE, THICKNESS):
        x = np.size(array[0,:])
        y = np.size(array[:,0])

        half_width = np.int(np.round(cv2.getTextSize(text,FONT,SCALE,THICKNESS)[0][0]/2,0))
        mid_x = np.int(np.round(x/2,0) - half_width)
        mid_y = np.int(np.round(y/2,0))

        return mid_x, mid_y

    @staticmethod
    def cropVideo(array):

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
