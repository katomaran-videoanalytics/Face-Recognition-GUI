#AUTHOR : J SAI SUBRAMANI

import tkinter
import cv2 
from PIL import Image,ImageTk
import time
from tkinter import filedialog
from tkinter import END
import imutils
import mxnet as mx
import align.detect_face
import time

from mtcnn_detector import MtcnnDetector

count = 0

class App:
    def __init__(self, window, window_title):
        self.path=None
        self.window = window
        self.window.geometry('1000x1000')
        self.window.title(window_title)
        #self.window.state("-zoomed",True)
        #self.window.attributes('-fullscreen', True)
        
         
       # Create a canvas that can fit the above video source size
        self.label=tkinter.Label(window, text="PROJECT : FACE RECOGNITION")
        self.label.place(x=0,y=0)

        self.tit=tkinter.Label(window, text="CHOOSE A MP4 FILE :")
        self.tit.place(x=0,y=30)

        self.btn_browse=tkinter.Button(window,text="BROWSE",width=20,command=self.browse_button)
        self.btn_browse.place(x=150,y=30)

        self.labelor=tkinter.Label(window,text="OR")
        self.labelor.place(x=350,y=30)

        self.btn_live=tkinter.Button(window,text="LIVE",width=20,command=self.live)
        self.btn_live.place(x=400,y=30)

        self.label1=tkinter.Entry(window, text="", width=80)
        self.label1.place(x=0,y=70)

        self.canvas = tkinter.Canvas(window, width = 650, height = 500)
        self.canvas.place(x=0,y=100)

   
        self.label2=tkinter.Label(window,text="S.NO")
        self.label2.place(x=700,y=500)

        self.sno=tkinter.Entry(window,text="",width=10)
        self.sno.place(x=700,y=520)

        self.label3=tkinter.Label(window,text="TIME")
        self.label3.place(x=750,y=500)

        self.time=tkinter.Entry(window,text="",width =20)
        self.time.place(x=750,y=520)


        self.label4=tkinter.Label(window,text="FACES")
        self.label4.place(x=920,y=500)

        self.no_face=tkinter.Entry(window,text="",width =20)
        self.no_face.place(x=920,y=520)

        
        

        

        
        
       # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        
 
        self.window.mainloop()
    def browse_button(self):
       self.path = filedialog.askopenfilename(initialdir="/",filetypes =(("Text File", "*.txt"),("Video File",".mp4"),("All Files","*.*")),title = "Choose a file.")
       self.vid = MyVideoCapture(str(self.path))
       self.sno.insert(0,str("1."))
       self.update()
       print(self.path)
       self.label1.delete(0,END) #remove current text in entry 
       self.label1.insert(0,self.path) #insert the path

    def live(self):
      self.vid = MyVideoCapture("rtsp://admin:admin0864@103.60.63.138:8081/cam/realmonitor?channel=1&subtype=0")
      self.update()

    
    def update(self):
       # Get a frame from the video source
       global count

       self.no_face.delete(0,END)
       self.no_face.insert(0,count)
       #self.sno.delete(0,END)
       #self.sno.insert(0,self.sno)
       self.time.delete(0,END)
       self.time1 =time.strftime('%H:%M:%S%p')
       self.time.insert(0,str(self.time1))
       print(str(self.time1))

       
       ret, frame = self.vid.get_frame()
 
       if ret:
           self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
           self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
       self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.detector = MtcnnDetector(model_folder='model', ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            img = cv2.resize(frame, (650,500))
            (h, w) = img.shape[:2]


            results = self.detector.detect_face(img)
    
            
            
            if results != None:
              total_boxes = results[0]
              points = results[1]
              global count
              count = 0

      
              draw = img.copy()
              for b in total_boxes:
                cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 255, 255))
                x1 = int(b[0])
                y1 = int(b[1])
                x2 = int(b[2])
                y2 = int(b[3])

                centroid = (int((x1+x2)/2),int((y1+y2)/2))
              
                if centroid[0]>=60 and centroid[0]<=w-60:
                  
                
                  count += 1
                  cv2.circle(draw, centroid, 4, (0, 255, 0), -1)
                  print("no_face:",count)
                  cv2.putText(draw, "count = "+str(count), (0, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                  img = draw
                
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
# Create a window and pass it to the Application object
App(tkinter.Tk(), "KATOMARAN ROBOTICS AND BUSSINESS SOLUTION")
