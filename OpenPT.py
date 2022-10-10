#필수 라이브러리 임포트 
from unittest import result
import cv2
import mediapipe as mp
import numpy as np
import math
import util
from PIL import ImageTk, Image

class opt():
    def __init__(self, cap):
        self.cap = cap
        #self.results = self.points()

    def points(self):
        mp_holistic = mp.solutions.holistic

        with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
                while self.cap.isOpened():
                    success, img = self.cap.read()
                    if not success:
                        print("No Camera")
                        continue
                    
                    img.flags.writeable = False
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = holistic.process(img)
                    return results
                    #print(self.results.face_landmarks.landmark[398])

    def FacePopints(self):
        face = self.results.face_landmarks

    def BodyPoints(self):
        body = self.results.pose_landmarks

    
    def splitPoint(self, point):
        return int(point.x, point.y)

    def midpoint(self, point1_x, point1_y, point2_x, point2_y):
        return float((point1_x + point2_x)/2), float((point1_y + point2_y)/2)

    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def NewEyeTracking(self):
        #print("눈 감지 함수 작동시작...")
        #right eye points
        results = self.points()
        p_corner_left_x, p_corner_left_y = results.face_landmarks.landmark[362].x, results.face_landmarks.landmark[362].y
        p_corner_right_x, p_corner_right_y = results.face_landmarks.landmark[359].x, results.face_landmarks.landmark[359].y
        p_bottom = results.face_landmarks.landmark[380]
        p_bottom2 = results.face_landmarks.landmark[373]
        p_top = results.face_landmarks.landmark[385]
        p_top2 = results.face_landmarks.landmark[387]
        #print("landmark 성공")
        
        #left eye points
        p_corner_left_x_L, p_corner_left_y_L = results.face_landmarks.landmark[33].x, results.face_landmarks.landmark[33].y
        p_corner_right_x_L, p_corner_right_y_L = results.face_landmarks.landmark[133].x, results.face_landmarks.landmark[133].y
        p_bottom_L = results.face_landmarks.landmark[163]
        p_bottom_L2 = results.face_landmarks.landmark[154]
        p_top_L = results.face_landmarks.landmark[161]
        p_top_L2 = results.face_landmarks.landmark[157]

        #print(p_bottom, p_bottom2)
        #right eye 
        corner_left = (p_corner_left_x, p_corner_left_y)
        corner_right = (p_corner_right_x, p_corner_right_y)

        center_top = self.midpoint(p_bottom.x,p_bottom.y, p_bottom2.x, p_bottom2.y)
        center_bottom = self.midpoint(p_top.x, p_top.y, p_top2.x, p_top2.y)

        horizontal_length = self.euclidean_distance(corner_left, corner_right)
        vertical_length = self.euclidean_distance(center_top, center_bottom)
        #print("top {0} | bottom {1}".format(center_top, center_bottom))
        #print("hor {0} | ver {1}".format(horizontal_length, vertical_length))

        ratio = horizontal_length / vertical_length

        #lift eye 
        corner_left_L = (p_corner_left_x_L, p_corner_left_y_L)
        corner_right_L = (p_corner_right_x_L, p_corner_right_y_L)

        center_top_L = self.midpoint(p_bottom_L.x,p_bottom_L.y, p_bottom_L2.x, p_bottom_L2.y)
        center_bottom_L = self.midpoint(p_top_L.x, p_top_L.y, p_top_L2.x, p_top_L2.y)

        horizontal_length_L = self.euclidean_distance(corner_left_L, corner_right_L)
        vertical_length_L = self.euclidean_distance(center_top_L, center_bottom_L)
        
        L_ratio = horizontal_length_L / vertical_length_L   

        #눈값 조절 추천 값 왼쪽 3.5 오른쪽 3.0 

        if L_ratio > 3.5:
            print("value : {0} blank".format(L_ratio))
        else:
            print("value : {0} Not blank".format(L_ratio))
        #return ratio

    def FaceRotaion(self):
        results = self.points()
        ret, img = self.cap.read()
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        size = image.shape
        image_points_2D = np.array([
            (results.face_landmarks.landmark[1].x, results.face_landmarks.landmark[1].y),
            (results.face_landmarks.landmark[152].x, results.face_landmarks.landmark[152].y),
            (results.face_landmarks.landmark[23].x, results.face_landmarks.landmark[23].y),
            (results.face_landmarks.landmark[253].x, results.face_landmarks.landmark[253].y),
            (results.face_landmarks.landmark[61].x, results.face_landmarks.landmark[61].y),
            (results.face_landmarks.landmark[62].x, results.face_landmarks.landmark[62].y)
        ], dtype="double")

        figure_points_3D = np.array([
            (0.0, 0.0, 0.0),
            (0.0, -330.0, -65.0),
            (-225.0, 170.0, -135.0),
            (225.0, 170.0, -135.0),
            (-150.0, -150.0, -125.0),
            (150.0, -150.0, -125.0)
        ])

        distortion_coeffs = np.zeros((4,1))
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)
        matrix_cmara = np.array(
            [[focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]], dtype = "double"
        )

        sucess, vector_rotation, vector_translation = cv2.solvePnP(figure_points_3D, image_points_2D, matrix_cmara, distortion_coeffs, flags=0)
        nose_end_point2D, jacobian = cv2.projectPoints(np.array([0.0, 0.0, 1000.0]), vector_rotation, vector_translation, matrix_cmara, distortion_coeffs)
        
        rmat, jac = cv2.Rodrigues(vector_rotation)
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

        #print("x : {0} | y : {1} | z : {2}".format(Qx, Qy, Qz))
        print("angles : {0}".format(angles))
        #return Qx, Qy, Qz

    def mouthOpen(self):
        print("제작중")    
    
    def output(self):
        ret, frame = self.cap.read()
        #img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image= Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        
        return imgtk
        