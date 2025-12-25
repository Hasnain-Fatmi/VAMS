
import cv2
from ultralytics import YOLO
import config
from utils.drawing import draw_text_with_background


class FightDetector:
    
    
    def __init__(self, model_path=None):
        
        model_path = model_path or config.FIGHT_MODEL_PATH
        self.model = YOLO(model_path)
        self.names = self.model.names
        
        # Persistence variables
        self.last_fight_box = None
        self.fight_patience = 0
        
    def detect(self, frame):
        
        results = self.model.track(
            source=frame,
            conf=config.CONF_THRESHOLD,
            imgsz=config.IMG_SIZE,
            persist=True,
            verbose=False
        )
        
        frame_has_fight = 0
        current_fight_found = False
        max_fight_conf = 0.0
        current_fight_box_coords = None
        
        # Process fight detections
        for r in results:
            if r.boxes is None:
                continue
            
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                
                class_name = self.names[cls_id]
                
                if class_name == "fight":
                    label = f"{class_name} {conf:.2f}"
                    frame_has_fight = 1
                    current_fight_found = True
                    max_fight_conf = max(max_fight_conf, conf)
                    current_fight_box_coords = [x1, y1, x2, y2]
                    
                    # Update persistence
                    self.last_fight_box = (x1, y1, x2, y2, label)
                    self.fight_patience = 0
                    
                    # Draw fight box
                    self._draw_fight_box(frame, x1, y1, x2, y2, label)
        
        # Apply Ghost Box if no fight detected but we have patience
        if not current_fight_found and self.last_fight_box is not None \
           and self.fight_patience < config.MAX_PATIENCE:
            self.fight_patience += 1
            frame_has_fight = 1  # Treat as fight frame
            
            x1, y1, x2, y2, label = self.last_fight_box
            current_fight_box_coords = [x1, y1, x2, y2]
            
            # Draw ghost box (same style)
            self._draw_fight_box(frame, x1, y1, x2, y2, label)
        
        return frame_has_fight, current_fight_found, max_fight_conf, current_fight_box_coords
    
    def _draw_fight_box(self, frame, x1, y1, x2, y2, label):
        
        color = config.COLOR_FIGHT
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw label with white background
        draw_text_with_background(
            frame,
            label,
            (x1, y1 - 8),
            font_scale=0.6,
            text_color=config.COLOR_FIGHT,
            bg_color=config.COLOR_TEXT_BG,
            thickness=2
        )
