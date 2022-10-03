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

