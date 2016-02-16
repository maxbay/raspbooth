
# import the necessary packages
import os
import sys
import time
import cv2
import numpy as np
import picamera.array
import picamera

sys.path.append(os.path.expanduser("~") + '/Projects/raspbooth/src')
from upload import Upload

class Capture():
    def __init__(self,x,y):
        self.capturing = False

        self.x = x
        self.y = y

        self.dims =  (512,384) #(640, 480) #(1280,960)
        self.x_coef = float(self.x)/float(self.dims[0])
        self.y_coef = float(self.y)/float(self.dims[1])

        self.camera = picamera.PiCamera()
        self.camera.resolution = self.dims
        self.camera.framerate = 12
        self.camera.hflip = True
        self.capArray = picamera.array.PiRGBArray(self.camera, size=self.dims)

    def startCapture(self):
        self.capturing = True
        time.sleep(0.1)

        FONT = cv2.FONT_HERSHEY_COMPLEX # font
        SCALE = 2 # pt size
        THICKNESS = 5 # boldness factor

        DELAY = 6
        FAUX_FLASH = 50
        epoch_time = np.int(time.time())

        snap1 = epoch_time + DELAY + 5
        snap2 = snap1 + DELAY
        snap3 = snap2 + DELAY
        snap4 = snap3 + DELAY
        snap_lst = [snap1, snap2, snap3, snap4]
        take_snap = [True, True, True, True]
        img_paths = []
        snap_count = 0

        STRIP_NAME = "photostrip.png"
        HOME_DIR = os.path.expanduser('~')
        snaps_dir = os.path.join(HOME_DIR,'Desktop/tmp_photos',str(epoch_time))
        strip_path = os.path.join(snaps_dir,STRIP_NAME)
        self.strip_path = strip_path

        for image in self.camera.capture_continuous(self.capArray, format="bgr", use_video_port=True):

            gray = image.array
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY) # converts to gray
            gray_copy = gray # unmanipulated copy for writing to disk
            gray = cv2.resize(gray, (0,0), fx=self.x_coef, fy=self.y_coef)

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

            if remaining_float > -1 and remaining_float < .5 and take_snap[snap_count]: # increase image values to make fake flash

                if not os.path.exists(snaps_dir): # make dir for all 4 pictures if it has not been created yet
                    os.makedirs(snaps_dir)

                file_name = os.path.join(snaps_dir,"test_image{0}.png".format(str(snap_count + 1)))
                img_paths.append(file_name)
                gray_copy = Capture.cropSnap(gray_copy)
                cv2.imwrite(file_name,gray_copy) # write picture to disk
                take_snap[snap_count] = False #indicate that picture has been taken, and another for this snap period not needed

                print("Snap # = {0}".format(str(snap_count + 1)))
                if snap_count == len(snap_lst) - 1: # breaks from while loop if snap count > scheduled snaps

                    self.capArray.truncate(0)
                    Capture.stitchImgs(snaps_dir,strip_path)
                    cv2.destroyAllWindows() # exit from display window
                    self.capturing = False
                    time.sleep(.5)

                    break


            mid_x, mid_y = Capture.findCenter(gray,text,FONT,SCALE,THICKNESS) # find x, y values in image to display text
            cv2.putText(gray,text,(mid_x,mid_y),FONT,SCALE,(255,255,255),THICKNESS) # insert text at x, y
            cv2.imshow("Video Feed", gray) # display image with text

            self.capArray.truncate(0)

            cv2.waitKey(5)

    @staticmethod
    def findCenter(array, text, FONT, SCALE, THICKNESS): # values for x, y such that text is centered
        x = np.shape(array)[1]
        y = np.shape(array)[0]

        half_width = np.int(np.round(cv2.getTextSize(text,FONT,SCALE,THICKNESS)[0][0]/2,0))
        mid_x = np.int(np.round(x/2,0) - half_width)
        mid_y = np.int(np.round(y/2,0))

        return mid_x, mid_y # x value, y value

    @staticmethod
    def cropSnap(array):

        w = np.int(np.shape(array)[1])
        h = np.int(np.shape(array)[0])
        target_w = np.int(h)
        start = np.int((w/2) - (target_w/2))
        end = np.int((w/2) + (target_w/2))

        array = array[:,start:end]

        return array


    @staticmethod
    def stitchImgs(img_dir,strip_path):

        if os.path.exists(strip_path):
            os.remove(strip_path)
        imgs = sorted(["{0}".format(os.path.join(img_dir,img)) for img in os.listdir(img_dir) if img.endswith(".png") and not img.startswith("~")])
        n_pics = len(imgs)

        if n_pics == 0:
            exit(1)

        img_open = cv2.imread(imgs[0])
        img_open = cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY)

        shape = np.shape(img_open)


        if len(shape) == 2:
            snap_rows, snap_cols = np.shape(img_open)
            offset = np.int(np.round(np.multiply(snap_cols,0.05),0))
            half_offset = np.int(np.round(np.multiply(offset,.5),0))
        else:
            exit(1)


        strip_rows, strip_cols = ((snap_rows * n_pics) + (half_offset * n_pics - 2)) + offset, (snap_cols + offset)

        strip = np.multiply(np.ones((strip_rows,strip_cols), np.uint8), 255)

        for i,img_path in enumerate(imgs):
            img_open = cv2.imread(img_path)
            img_open = cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY)
            strip[(half_offset * (i+1) + snap_rows * i) : (half_offset * (i+1) + snap_rows * (i+1)), (half_offset) : (half_offset + snap_cols)] = img_open

        cv2.imwrite(strip_path,strip)



