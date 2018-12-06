from tkinter import *
from tkinter import filedialog



global path 
def browse_button():
	path = filedialog.askopenfilename(initialdir="/",filetypes =(("Text File", "*.txt"),("Video File",".mp4"),("All Files","*.*")),title = "Choose a file.")
	print(path)
	E1.delete(0,END) #remove current text in entry
	E1.insert(0,path) #insert the path
	
	
	


window = Tk()
window.title("FACE-RECOGNITION-GUI")
window.geometry("600x600")
lbl = Label(window,text="choose a MP4 file")
lbl.grid(column = 5, row=5)
btn = Button(window,text="BROWSE",command=browse_button)
btn.grid(column =10, row =5)
E1 = Entry(window,text="",width=40)
E1.grid(column=10,row = 7)



window.mainloop()