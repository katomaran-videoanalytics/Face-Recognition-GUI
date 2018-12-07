import tkinter
import cv2 
from PIL import Image,ImageTk
import time
from tkinter import filedialog
from tkinter import END
import imutils

class App:
    def __init__(self, window, window_title, video_source="Intelligent Video Analysis - BOSCH.mp4"):
        self.path=None
        self.window = window
        self.window.title(window_title)
        #self.window.geometry("900x900")
        self.video_source = video_source
 
       # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
         
       # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack(fill="both",expand=True)
 
       
        self.label=tkinter.Entry(window, text="choose MP4 file", width=70)
        self.label.pack(anchor=tkinter.CENTER, expand=True)
        
        self.btn_browse=tkinter.Button(window,text="BROWSE",width=70,command=self.browse_button)
        self.btn_browse.pack(anchor=tkinter.CENTER, expand=True)
       # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
 
        self.window.mainloop()
    def browse_button(self):
       self.path = filedialog.askopenfilename(initialdir="/",filetypes =(("Text File", "*.txt"),("Video File",".mp4"),("All Files","*.*")),title = "Choose a file.")
       self.vid = MyVideoCapture(str(self.path))
       print(self.path)
       self.label.delete(0,END) #remove current text in entry 
       self.label.insert(0,self.path) #insert the path

    
    def update(self):
       # Get a frame from the video source
       ret, frame = self.vid.get_frame()
 
       if ret:

           self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
           #self.img = frame.resize(int(self.vid.width),int(self.vid.height),Image.ANTIALIAS)
           self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
       self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source="Intelligent Video Analysis - BOSCH.mp4"):
        # Open the video source
        
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            #frame = imutils.resize(frame,int(self.width),int(self.height))
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
