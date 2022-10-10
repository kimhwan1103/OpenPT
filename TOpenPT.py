import argparse
from datetime import datetime
import cv2
import mediapipe as mp
import numpy as np
import math 
import util
from PIL import ImageTk, Image
from threading import Thread
import tkinter

class CountsPerSec:
    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0
    
    def start(self):
        self._start_time = datetime.now()
        return self
    
    def increment(self):
        self._num_occurrences += 1
    def countsPerSec(self):
        elapse_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapse_time

class CamGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
        
    def stop(self):
        self.stopped = True
    
def putIterationPerSec(frame, iterations_per_sec):
    cv2.putText(frame, "{:0f} iterations/sec".format(iterations_per_sec),
    (10, 450), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def threadVideGet(source=0):
    video_getter = CamGet(source).start()
    cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord('q')) or video_getter.stopped:
            video_getter.stop()
            break
        
        frame = video_getter.frame
        frame = putIterationPerSec(frame, cps.countsPerSec())
        frame2array = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=frame2array)
        cps.increment()
        
        return imgtk