import time
import tkinter 
import threading
import gui
import cv2
import OpenPT

class App(object):
    def __init__(self, master):
        master.geometry("1280x720+100+100")
        master.title("OpenPT")
        label = tkinter.Label(master, text="OpenPT", font=30)
        label.pack()
        cameraLabel = tkinter.Label(master, text="Camera:")
        faceLabel = tkinter.Label(master, text="Face:")
        bodyLabel = tkinter.Label(master, text="Body:")
        cameraLabel.place(x=50, y=50)
        faceLabel.place(x=50, y=100)
        bodyLabel.place(x=50, y=150)
        GUI = gui.Main(master)
        GUI.StateView()
        GUI.NetView()
        GUI.LogView()
        
def InfiniteProcess():
    while not finish:
        print("Infinite Loop")
        time.sleep(3)

finish = False
Process = threading.Thread(target=InfiniteProcess)
Process.start()

mainWindow = tkinter.Tk()
app = App(mainWindow)
'''
GUI = gui.Main(mainWindow)
GUI.StateView()
GUI.NetView()
GUI.LogView()
GUI.ImageView()
'''
mainWindow.mainloop()
finish = True
Process.join()