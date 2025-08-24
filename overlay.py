import cv2
import numpy as np
import random
import math

class SimpleOverlay:
    def __init__(self, config):
        self.enabled = config['enabled']
        self.ring_size = config['ring_size']
        self.colors = config['colors']
    
    def draw(self, frame, subjects):
        if not self.enabled:
            return frame
        
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        for subject in subjects:
            cv2.drawContours(mask, [subject.contour], -1, 255, -1)
        
        overlay_color = np.array([0, 0, 0], dtype=np.uint8)
        overlay = np.full_like(frame, overlay_color)
        
        mask_3d = np.stack([mask, mask, mask], axis=2) / 255.0
        alpha = 0.5
        frame = frame * (1 - alpha * mask_3d) + overlay * (alpha * mask_3d)
        frame = frame.astype(np.uint8)
        
        for i, subject in enumerate(subjects):
            x, y = int(subject.x), int(subject.y)
            color = self.colors[i % len(self.colors)]
            
            cv2.circle(frame, (x, y), self.ring_size, color, 2)
            cv2.putText(frame, str(i), (x + 20, y - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def toggle(self):
        self.enabled = not self.enabled

class GlitchOverlay:
    def __init__(self, config):
        self.enabled = config['enabled']
        self.ring_size = config['ring_size']
        self.colors = config['colors']
        self.frame_count = 0
        self.glitch_data = {}
    
    def draw(self, frame, subjects):
        if not self.enabled:
            return frame
        
        self.frame_count += 1
        
        for i, subject in enumerate(subjects):
            if i not in self.glitch_data:
                self.glitch_data[i] = self._init_glitch_data()
            
            glitch = self.glitch_data[i]
            x, y = int(subject.x), int(subject.y)
            
            self._draw_chaotic_overlay(frame, x, y, i, glitch)
        
        return frame
    
    def _init_glitch_data(self):
        return {
            'offset_x': random.uniform(-3, 3),
            'offset_y': random.uniform(-3, 3),
            'rotation': random.uniform(0, 2 * math.pi),
            'scale': random.uniform(0.6, 1.0),
            'glitch_timer': random.randint(0, 20),
            'flicker_timer': random.randint(0, 5),
            'data_stream': [random.randint(0, 9999) for _ in range(30)],
            'line_points': [(random.randint(-15, 15), random.randint(-15, 15)) for _ in range(12)],
            'fragment_points': [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(15)]
        }
    
    def _draw_chaotic_overlay(self, frame, x, y, subject_id, glitch):
        text_color = (255, 255, 255)
        
        glitch['glitch_timer'] += 1
        glitch['flicker_timer'] += 1
        
        if glitch['glitch_timer'] > 20:
            glitch['offset_x'] = random.uniform(-3, 3)
            glitch['offset_y'] = random.uniform(-3, 3)
            glitch['glitch_timer'] = 0
        
        if glitch['flicker_timer'] > 5:
            glitch['data_stream'] = [random.randint(0, 9999) for _ in range(30)]
            glitch['flicker_timer'] = 0
        
        offset_x = int(glitch['offset_x'])
        offset_y = int(glitch['offset_y'])
        
        # Small data numbers close to the bright spot
        for j in range(3):
            data_x = x + random.randint(-15, 15) + offset_x
            data_y = y + random.randint(-15, 15) + offset_y
            data_text = f"{glitch['data_stream'][j]:04d}"
            cv2.putText(frame, data_text, (data_x, data_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.2, text_color, 1)
        
        # Small ID close to the bright spot
        id_x = x + 10 + offset_x
        id_y = y - 10 + offset_y
        if random.random() > 0.5:
            id_text = f"ID:{subject_id:02d}"
        else:
            id_text = f"ERR:{random.randint(0, 99):02d}"
        cv2.putText(frame, id_text, (id_x, id_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.2, text_color, 1)
    
    def toggle(self):
        self.enabled = not self.enabled

class OverlayManager:
    def __init__(self, config):
        self.simple_overlay = SimpleOverlay(config)
        self.glitch_overlay = GlitchOverlay(config)
        self.current_style = 'simple'
    
    def draw(self, frame, subjects):
        if self.current_style == 'simple':
            return self.simple_overlay.draw(frame, subjects)
        else:
            return self.glitch_overlay.draw(frame, subjects)
    
    def switch_style(self):
        if self.current_style == 'simple':
            self.current_style = 'glitch'
            print("Switched to glitch overlay")
        else:
            self.current_style = 'simple'
            print("Switched to simple overlay")
    
    def toggle(self):
        if self.current_style == 'simple':
            self.simple_overlay.toggle()
        else:
            self.glitch_overlay.toggle()
