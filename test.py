import OpenPT
import cv2

cap = cv2.VideoCapture(1)

opt = OpenPT.opt(cap)

while True:
    points = opt.points()
    #print(points.pose_landmarks)
    #print(points.face_landmarks)
    opt.NewEyeTracking(points.face_landmarks)
