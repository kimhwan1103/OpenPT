import socket
import util

#UDP를 활용하여 진행 
class net():
    def __init__(self):
        self.points = {}
        self.ip = "127.0.0.1"
        self.prot = 9999
        self.bytesize = 2048
        self.byteToSend = str.encode(self.points)
    def connect(self, ):
        UDPclinetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        UDPclinetSocket.sendto(self.byteToSend, (self.ip, self.prot))

        util.util.GetLog("sucess")