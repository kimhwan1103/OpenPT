import OpenPT
import network
import util 
import cv2

#테스트를 위한 코드

cap = cv2.VideoCapture(1)

opt = OpenPT.opt(cap)

#opt.points()

while True:
    #opt.NewEyeTracking()
    opt.FaceRotaion()
#Qx, Qy, Qz = opt.FaceRotaion()

#print("x : {0} | y : {1} | z : {2}".format(Qx, Qy, Qz))
#ratio = opt.NewEyeTracking()

#print(ratio) 