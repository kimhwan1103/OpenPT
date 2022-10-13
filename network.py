import socket
import pickle
import util
import json 

'''
작업 리스트 
1. 네트워크 예외처리 
2. 네트워크 발신 데이터 처리 
3. 추후 버그 수정 
'''

#UDP를 활용하여 진행 
class net():
    def __init__(self, ip, port):
        self.result = []
        self.bytesize = 2048
        self.addr_port = (str(ip), int(port))
        #self.byteToSend = str.encode(self.points)

    def inputData(self, results):
        self.result = results
        

    def connect(self, data):
        UDPclinetSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        test_msg = "hello"
        bytes_to_send = str.encode(test_msg)

        #util.util.GetLog("server connecting...")
        try: 
            #UDPclinetSocket.connect((str(ip), int(port)))
            #UDPclinetSocket.sendto(bytes_to_send, self.server_addr_port)
            #util.util.GetLog("sucess")
            #self.send(self.points, UDPclinetSocket)
            UDPclinetSocket.sendto(data, self.addr_port)
        except:
            #util.util.GetLog("Error server missing.. \n plese server start or restart")
            print("Error server missing.. \nplese server start or restart")

    def send(self, server):
        send_data = json.dumps(self.data).encode('UTF-8')#직렬화 
        server.sendto(send_data)