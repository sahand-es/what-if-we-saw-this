#!/usr/bin/env python3
import cv2
import numpy as np
from config import DETECTION, OVERLAY, WEBCAM
from detector import Detector
from overlay import OverlayManager

class DetectorApp:
    def __init__(self):
        self.detector = Detector(DETECTION)
        self.overlay = OverlayManager(OVERLAY)
        self.running = False
    
    def run(self):
        print("Starting bright spot detector...")
        print("Q: Quit, T: Toggle overlays, S: Switch style, +/-: Threshold")
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM['width'])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM['height'])
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        self.running = True
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            
            subjects = self.detector.detect(frame)
            result = self.overlay.draw(frame.copy(), subjects)
            
            cv2.putText(result, f"Bright spots: {len(subjects)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(result, f"Threshold: {self.detector.threshold}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Bright Spot Detector', result)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                self.overlay.toggle()
                print("Toggled overlays")
            elif key == ord('s'):
                self.overlay.switch_style()
            elif key == ord('+') or key == ord('='):
                self.detector.threshold = min(255, self.detector.threshold + 10)
            elif key == ord('-'):
                self.detector.threshold = max(0, self.detector.threshold - 10)
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    app = DetectorApp()
    app.run()

if __name__ == "__main__":
    main()
