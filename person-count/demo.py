#AUTHOR : J SAI SUBRAMANI

import tkinter
import cv2 
from PIL import Image,ImageTk
import time
from tkinter import filedialog
from tkinter import END

from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib

count = 0
count1 =0

class App:
    def __init__(self, window, window_title):
        self.path=None
        self.window = window
        self.window.geometry('1000x1000')
        self.window.title(window_title)
        
         
       # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = 500, height = 500)
        self.canvas.grid(column =0, row =10)

         
        self.img = Image.open("per.jpg")
        self.img = self.img.resize((200,200),Image.ANTIALIAS)

        
        self.canvas1 = tkinter.Canvas(window,width=200,height=200)
        self.canvas1.grid(column=1,row=10)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas1.create_image(0,0,image=self.photo,anchor=tkinter.NW)
        
 
       
        self.label=tkinter.Label(window, text="choose MP4 file")
        self.label.grid(column = 0, row=0)

        self.label1=tkinter.Entry(window, text="", width=70)
        self.label1.grid(column=0,row=8)

        self.label2=tkinter.Label(window,text="number of person IN ")
        self.label2.grid(column=1,row=20)

        self.label3=tkinter.Label(window,text="number of person out ")
        self.label3.grid(column=1,row=25)



        self.no_face=tkinter.Entry(window,text="",width =20)
        self.no_face.grid(column=2,row=20)

        self.no_face_out=tkinter.Entry(window,text="",width =20)
        self.no_face_out.grid(column=2,row=25)

        self.btn_live=tkinter.Button(window,text="LIVE",width=20,command=self.live)
        self.btn_live.grid(column =1, row =10)
        
        self.btn_browse=tkinter.Button(window,text="BROWSE",width=20,command=self.browse_button)
        self.btn_browse.grid(column =0, row =5)
       # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        
 
        self.window.mainloop()
    def browse_button(self):
       self.path = filedialog.askopenfilename(initialdir="/",filetypes =(("Text File", "*.txt"),("Video File",".mp4"),("All Files","*.*")),title = "Choose a file.")
       self.vid = MyVideoCapture(str(self.path))
       self.update()
       print(self.path)
       self.label1.delete(0,END) #remove current text in entry 
       self.label1.insert(0,self.path) #insert the path
       

    def live(self):
      self.vid = MyVideoCapture("rtsp://admin:admin0864@192.168.0.200:554/cam/realmonitor?channel=1&subtype=0")

    
    def update(self):
       # Get a frame from the video source
       global count
       global couont1
       self.no_face.delete(0,END)
       self.no_face.insert(0,count)
       self.no_face_out.delete(0,END)
       self.no_face_out.insert(0,count1)
       ret, frame = self.vid.get_frame()
 
       if ret:
           self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
           self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
       self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe("mobilenet_ssd/MobileNetSSD_deploy.prototxt", "mobilenet_ssd/MobileNetSSD_deploy.caffemodel")
        print("[INFO] opening video file...")
        #"rtsp://admin:admin0864@192.168.0.200:554/cam/realmonitor?channel=1&subtype=0"
        self.vs = cv2.VideoCapture(video_source)
        self.W = None
        self.H = None
        self.ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        self.trackers = []
        self.trackableObjects = {}
        self.totalFrames = 0
        self.totalDown = 0
        self.totalUp = 0
        self.fps = FPS().start()
        if not self.vs.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        
 
    def get_frame(self):
        if self.vs.isOpened():
            ret,frame = self.vs.read()
            frame = imutils.resize(frame, width=900)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.H, self.W = frame.shape[:2]

            status = "Waiting"
            rects = []
            if self.totalFrames % 5 == 0:
              status = "Detecting"

              self.trackers = []
              blob = cv2.dnn.blobFromImage(frame, 0.007843, (self.W, self.H), 127.5)
              self.net.setInput(blob)
              detections = self.net.forward()
              for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.4:
                  idx = int(detections[0, 0, i, 1])
                  if idx == 15:
                    box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY),(0,255,255), 2)
                    #centroid=(int((startX+endX)/2),int((startY+endY)/2))
                    #person detection
                    #if centroid[1]<= self.H-230 and centroid[1]>= self.H-320:
                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
                    self.trackers.append(tracker)
            else:
              for tracker in self.trackers:
                status = "Tracking"
                tracker.update(rgb)
                pos = tracker.get_position()
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())
                rects.append((startX, startY, endX, endY))

            #cv2.line(frame, (0, self.H-320), (self.W, self.H-320), (255, 0, 0), 2)
            cv2.line(frame, (0, self.H // 2), (self.W, self.H // 2), (0, 255, 255), 2)
            #cv2.line(frame, (0, self.H-230), (self.W, self.H-230), (255, 0, 0), 2)
            objects = self.ct.update(rects)
            for (objectID, centroid) in objects.items():
              to = self.trackableObjects.get(objectID, None)
              if to is None:
                to = TrackableObject(objectID, centroid)

              else:
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)
                if not to.counted:
                  if direction < 0 and centroid[1] < self.H // 2:
                    self.totalDown += 1
                    to.counted = True
                  if direction > 0 and centroid[1] > self.H // 2:
                    self.totalUp += 1
                    to.counted = True
              self.trackableObjects[objectID] = to
            self.totalFrames += 1
            info = [("IN", self.totalUp),("Status", status),]
            for (i, (k, v)) in enumerate(info):
              text = "{}: {}".format(k, v)
              #cv2.putText(frame, text, (10, self.H - ((i * 20) + 20)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
              frame = cv2.resize(frame,(500,500),interpolation = cv2.INTER_AREA)
            global count
            global count1
            count1=self.totalUp
            count=self.totalDown
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vs.isOpened():
            self.fps.stop()
            self.vs.release()
 
# Create a window and pass it to the Application object
App(tkinter.Tk(), "FACE-RECOGNITION-GUI")
