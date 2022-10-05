#필수 라이브러리 임포트 
import cv2
import mediapipe as mp
import numpy as np
import math
import util
from PIL import ImageTk, Image

class opt():
    def __init__(self, cap):
        self.cap = cap
        self.results = []

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
                    self.results = holistic.process(img)
                    return self.results

    def FacePopints(self):
        face = self.results.face_landmarks

    def BodyPoints(self):
        body = self.results.pose_landmarks

    
    def splitPoint(point):
        return int(point.x, point.y)

    def midpoint(point1_x, point1_y, point2_x, point2_y):
        return int((point1_x + point2_x)/2), int((point1_y + point2_y)/2)

    def euclidean_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def NewEyeTracking(self, results):
        p_corner_left_x, p_corner_left_y = results.landmark[398].x, results.landmark[398].y
        p_corner_right_x, p_corner_right_y = results.landmark[359].x, results.landmark[359].y
        p_bottom = results.landmark[380]
        p_bottom2 = results.landmark[375]
        p_top = results.landmark[385]
        p_top2 = results.landmark[387]

        corner_left = (p_corner_left_x, p_corner_left_y)
        corner_right = (p_corner_right_x, p_corner_right_y)

        center_top = self.midpoint(p_bottom.x,p_bottom.y, p_bottom2.x, p_bottom2.y)
        center_bottom = self.midpoint(p_top.x, p_top.y, p_top2.x, p_top2.y)

        horizontal_length = self.euclidean_distance(corner_left, corner_right)
        vertical_length = self.euclidean_distance(center_top, center_bottom)

        ratio = horizontal_length / vertical_length

        print(ratio)
        return ratio

    def FaceRotaion(self):
        ret, img = self.cap.read()
        size = img.shape
        image_points_2D = np.array([
            (self.results.face_landmark[1].x, self.results.face_landmark[1].y),
            (self.results.face_landmark[152].x, self.results.face_landmark[152].y),
            (self.results.face_landmark[23].x, self.results.face_landmark[23].y),
            (self.results.face_landmark[253].x, self.results.face_landmark[253].y),
            (self.results.face_landmark[61].x, self.results.face_landmark[61].y),
            (self.results.face_landmark[62].x, self.results.face_landmark[62].y)
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

        return Qx, Qy, Qz

    def mouthOpen(self):
        print("제작중")    
    
    def output(self):
        ret, frame = self.cap.read()
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        return imgtk
        