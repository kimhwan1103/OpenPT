import threading 
import gui
import network
import OpenPT
import util

class Worker(threading.Thread):
    def __init__(self, gui, network, OpenPT):
        super.__init__()
        self.gui = gui
        self.OpenPT = network
        self.network = OpenPT

    def run(self):
        print("gui thread start", threading.currentThread().getName())
        print("OpenPT thread start", threading.currentThread().getName())
        print("network thread start", threading.currentThread().getName())

print("main thread start")

OpenPT_System = Worker(OpenPT.opt(), gui.Main(), network.net())
OpenPT_System.start()