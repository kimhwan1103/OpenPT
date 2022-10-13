import tkinter
import OpenPT
import cv2
import threading
import TOpenPT
import network

#OpenPT에서 데이터 처리값을 불러오는 클래스
class DtoG:
    def __init__(self):
        self.results = []

    def getState(self):
        self.results = opt.points()
        return self.results
    
    def getEye(self):
        ratio = opt.NewEyeTracking(self.results)      
        return ratio

#GUI및 전체적인 서비스 관리 클래스 
class Main(object):
    def __init__(self, master):
        #threading.Thread.__init__(self)
        #self.window = tkinter.Tk()
        #self.opt = OpenPT.opt(cap)
        #self.window.title("OpenPT Beta")
        #self.window.geometry("1280x720+100+100")
        #self.window.resizable(False, False)
        self.master = master
        self.results = DtoG().getState()
        self.engineState = False
        self.LogStr = ""
    
    def StateView(self):
        #좌표들 불러오기 
        if not self.results:
            Onlinelabel = tkinter.Label(self.master, text=": OFFLINE", fg="red")
            Onlinelabel.place(x=100, y=50)
        else:
            Offlinelabel = tkinter.Label(self.master, text=": ONLINE", fg="#008000")
            Offlinelabel.place(x=100, y=50)
        
        if self.engineState == True:
            engineOnlinelabel = tkinter.Label(self.master, text=": ONLINE", fg="#00800")
            engineOnlinelabel.place(x=150, y=260)
        else:
            engineOFFlinelabel = tkinter.Label(self.master, text=": OFFLINE")
            engineOFFlinelabel.place(x=150, y=260)
        
    def Errbox(self, text):
        messagebox.showinfo("error", text)

    def NetView(self):
        hostlabel = tkinter.Label(self.master, text="Host IP")
        hostlabel.place(x=50, y=200)
        ip = tkinter.StringVar()
        ipbox = tkinter.Entry(self.master, width=20, textvariable=ip)
        ipbox.place(x=100, y=200)
        portlabel = tkinter.Label(self.master, text="Port")
        portlabel.place(x=290, y=200)
        port = tkinter.StringVar()
        portbox = tkinter.Entry(self.master, width=20, textvariable=port)
        portbox.place(x=320, y=200)
        button = tkinter.Button(self.master, text="sbumit")
        button.place(x=50, y=230)
        #self.NetButton(ip, port)
        
        #connect 부분
        connectlabel = tkinter.Label(self.master, text="Connect Engine")
        connectlabel.place(x=50, y=260)

        connectIPlabel = tkinter.Label(self.master, text="IP: {0} | PORT: {1}".format(ip.get(), port.get()))
        connectIPlabel.place(x=50, y=280)
        
    def LogView(self):
        logLabel = tkinter.Label(self.master, text="Log", fg="red")
        logLabel.place(x=50, y=310)
        logEntryset = tkinter.Entry(self.master, state='readonly', readonlybackground="white", width=100)
        logEntryset.insert(0, self.LogStr)
        logEntryset.place(x=50, y=330)

    def ImageView(self):
        imageLabel = tkinter.Label(self.master, text="OutPut")
        imageLabel.place(x=650, y=50)
        camera = opt.output()
        #imageLabel2 = tkinter.Label(self.master, image=camera)
        #imageLaTclErrorbel2.image = camera
        image = tkinter.Canvas(self.master, width=640, height=480)
        image.create_image(0, 0, image=camera, anchor= tkinter.NW)
        image.place(x=650, y=100)

    def NetButton(self, ip, port):
        #network.net()
        network.net().connect(ip, port)

    '''
    #메인뷰
    def MainView(self):
        label = tkinter.Label(self.window, text="OpenPT", font="30")
        cameraLabel = tkinter.Label(self.window, text="Camera:")
        faceLabel = tkinter.Label(self.window, text="Face:")
        bodyLabel = tkinter.Label(self.window, text="Body:  ")
        label.pack()
        cameraLabel.place(x=50, y=50)
        faceLabel.place(x=50, y=100)
        bodyLabel.place(x=50, y=150)
        self.StateView()
        self.NetView()
        self.LogView()
        self.ImageView()
        self.window.mainloop()
    '''

cap = cv2.VideoCapture(1)
opt = OpenPT.opt(cap)