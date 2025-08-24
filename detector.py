import cv2
import numpy as np

class Subject:
    def __init__(self, x, y, area, brightness, contour):
        self.x = x
        self.y = y
        self.area = area
        self.brightness = brightness
        self.contour = contour

class Detector:
    def __init__(self, config):
        self.threshold = config['threshold']
        self.min_area = config['min_area']
        self.max_area = config['max_area']
        self.max_subjects = config.get('max_subjects', 30)
    
    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        subjects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area or area > self.max_area:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                x = M["m10"] / M["m00"]
                y = M["m01"] / M["m00"]
            else:
                continue
            
            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            brightness = cv2.mean(gray, mask=mask)[0]
            
            subjects.append(Subject(x, y, area, brightness, contour))
        
        subjects.sort(key=lambda s: s.brightness, reverse=True)
        return subjects[:self.max_subjects]
