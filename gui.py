from sre_parse import State
import tkinter
import OpenPT
import cv2


#OpenPT에서 데이터 처리값을 불러오는 클래스
class DtoG():
    def __init__(self):
        self.results = []

    def getState(self):
        self.results = opt.points()
        return self.results
    
    def getEye(self):
        ratio = opt.NewEyeTracking(self.results)      
        return ratio

#GUI및 전체적인 서비스 관리 클래스 
class Main():
    def __init__(self):
        self.window = tkinter.Tk()
        #self.opt = OpenPT.opt(cap)
        self.window.title("OpenPT Beta")
        self.window.geometry("640x400+100+100")
        self.window.resizable(False, False) 
        self.results = DtoG().getState()  
        self.engineState = False
    
    def StateView(self):
        #좌표들 불러오기 
        if not self.results:
            Onlinelabel = tkinter.Label(self.window, text=": OFFLINE", fg="FF0000")
            Onlinelabel.place(x=100, y=50)
        else:
            Offlinelabel = tkinter.Label(self.window, text=": ONLINE", fg="#008000")
            Offlinelabel.place(x=100, y=50)
        
        if self.engineState == True:
            engineOnlinelabel = tkinter.Label(self.window, text=": ONLINE", fg="#00800")
            engineOnlinelabel.place(x=150, y=260)
        else:
            engineOFFlinelabel = tkinter.Label(self.window, text=": OFFLINE")
            engineOFFlinelabel.place(x=150, y=260)
        
    def Errbox(self, text):
        messagebox.showinfo("error", text)

    def NetView(self):
        hostlabel = tkinter.Label(self.window, text="Host IP")
        hostlabel.place(x=50, y=200)
        ip = tkinter.StringVar()
        ipbox = tkinter.Entry(self.window, width=20, textvariable=ip)
        ipbox.place(x=100, y=200)
        portlabel = tkinter.Label(self.window, text="Port")
        portlabel.place(x=290, y=200)
        port = tkinter.StringVar()
        portbox = tkinter.Entry(self.window, width=20, textvariable=port)
        portbox.place(x=320, y=200)
        button = tkinter.Button(self.window, text="sbumit")
        button.place(x=50, y=230)
        
        #connect 부분
        connectlabel = tkinter.Label(self.window, text="Connect Engine")
        connectlabel.place(x=50, y=260)

        connectIPlabel = tkinter.Label(self.window, text="IP: {0} | PORT: {1}".format(ip.get(), port.get()))
        connectIPlabel.place(x=50, y=280)
        

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
        self.window.mainloop()
#메인 클래스 실행 
cap = cv2.VideoCapture(0)
opt = OpenPT.opt(cap)
Main().MainView()