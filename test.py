from matplotlib.font_manager import json_dump
import OpenPT
import network
import util 
import cv2
import json

#테스트를 위한 코드

cap = cv2.VideoCapture(0)

opt = OpenPT.opt(cap)
net = network.net("127.0.0.1", 9999)
#opt.points()

while True:
    L_state, R_state = opt.NewEyeTracking()
    angles = opt.FaceRotaion()

    data = {"L_state" : L_state, "R_state" : R_state, "angles" : angles}
    json_data = json.dumps(data).encode('UTF-8')
    net.connect(json_data)

#Qx, Qy, Qz = opt.FaceRotaion()

#print("x : {0} | y : {1} | z : {2}".format(Qx, Qy, Qz))
#ratio = opt.NewEyeTracking()

#print(ratio) 