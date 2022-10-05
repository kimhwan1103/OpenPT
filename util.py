from asyncio import subprocess
import os
import numpy as np 
import math 

class util():
    def __init__(self):
        self.point_x
        self.point_y
    
    def pointSplit(self, point):
        self.point_x = point.x
        self.point_y = point.y
        return int(self.point_x, self.point_y)
    
    def midpoint(self, point1, point2):
        point1_x, point1_y = self.pointSplit(point1)
        point2_x, point2_y = self.pointSplit(point2)
        return int((point1_x + point2_x)/2), int((point1_y + point2_y)/2)

    def euclidean_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def GetLog(self, LogText):
        return LogText

    def LogCommand(self, Command):
        print("만드는 중")

    def rot_matrix_to_euler(self, R):
        y_rot = math.asin(R[2][0])
        x_rot = math.acos(R[2][0]/math.cos(y_rot))
        z_rot = math.acos(R[0][0]/math.cos(y_rot))
        y_rot_angle = y_rot *(180/math.pi)
        x_rot_angle = x_rot *(180/math.pi)
        z_rot_angle = z_rot *(180/math.pi)

        return x_rot_angle, y_rot_angle, z_rot_angle

    def get_camera_serial(self, cam_id):
        p = subprocess.Popen('udevadm info --name=/dev/video{} | grep ID_Serial= | cut -d "=" -f 2'.format(cam_id), stdout = subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.stastus = p.wait()
        response = output.decode('utf-8')
        return response.replace('\n', '')