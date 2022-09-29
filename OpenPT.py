#필수 라이브러리 임포트 
from unittest import result
import cv2
import mediapipe as mp
import numpy as np
import math

class opt():
    def __init__(self, cap):
        self. cap = cap

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

    def EyeTracking(self, results):
        #거리 계산을 활용하여 눈 깜박이 감지 개선 버젼 

        #새로운 계산을 위한 더 많은 좌표들 
        #예외 처리 
        try:
            R_condition_a1 = results.landmark[385].x
            R_condition_a2 = results.landmark[385].y
            R_condition_b1 = results.landmark[380].x
            R_condition_b2 = results.landmark[380].y
            R_condition_c1 = results.landmark[359].x
            R_condition_c2 = results.landmark[359].y
            R_condition_d1 = results.landmark[398].x
            R_condition_d2 = results.landmark[398].y
        except:
            print('err')

        R_r1 = (R_condition_a1 - R_condition_b1) ** 2
        R_r2 = (R_condition_a2 - R_condition_b2) ** 2
        R_r3 = R_r1 + R_r2
        R_result = np.sqrt(R_r3) * 100

        #새로운 좌표계산식 
        R_n1 = (R_condition_a2 - R_condition_d2) ** -1


        print("첫번째 계산 값 : {0} | 두번째 계산 값 : {1}".format(R_result, R_n1))
    
    def splitPoint(point):
        return int(point.x, point.y)

    def midpoint(point1, point2):
        return int((point1.x + point2.x)/2), int((point1.y + point2.y)/2)

    def euclidean_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def NewEyeTracking(self, results):
        p_corner_left_x, p_corner_left_y = self.splitPoint(results.landmark[398])
        p_corner_right_x, p_corner_right_y = self.splitPoint(results.landmark[359])
        p_bottom = results.landmark[380]
        p_bottom2 = results.landmark[375]
        p_top = results.landmark[385]
        p_top2 = results.landmark[387]

        corner_left = (p_corner_left_x, p_corner_left_y)
        corner_right = (p_corner_right_x, p_corner_right_y)

        center_top = self.midpoint(p_bottom, p_bottom2)
        center_bottom = self.midpoint(p_top, p_top2)

        horizontal_length = self.euclidean_distance(corner_left, corner_right)
        vertical_length = self.euclidean_distance(center_top, center_bottom)

        ratio = horizontal_length / vertical_length

        print(ratio)
        #return ratio