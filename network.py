import socket
import pickle
import util

'''
작업 리스트 
1. 네트워크 예외처리 
2. 네트워크 발신 데이터 처리 
3. 추후 버그 수정 
'''

#UDP를 활용하여 진행 
class net():
    def __init__(self):
        self.points = {}
        self.bytesize = 2048
        #self.byteToSend = str.encode(self.points)

    def connect(self, ip, port):
        UDPclinetSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        util.util.GetLog("server connecting...")
        try: 
            UDPclinetSocket.connect((ip, int(port)))
            util.util.GetLog("sucess")
            self.send(self.points, UDPclinetSocket)
        except:
            util.util.GetLog("Error server missing.. \n plese server start or restart")


    def send(self, data, server):
        data = pickle.dumps(data) #직렬화 
        server.sendall(data)