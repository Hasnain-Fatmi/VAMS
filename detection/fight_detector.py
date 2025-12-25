
import cv2
from ultralytics import YOLO
import config
from utils.drawing import draw_text_with_background, draw_rounded_rectangle, draw_glow_effect


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
                    label = f"FIGHT {conf:.2f}"
                    frame_has_fight = 1
                    current_fight_found = True
                    max_fight_conf = max(max_fight_conf, conf)
                    current_fight_box_coords = [x1, y1, x2, y2]

                    # Update persistence
                    self.last_fight_box = (x1, y1, x2, y2, label, conf)
                    self.fight_patience = 0

                    # Draw fight box
                    self._draw_fight_box(frame, x1, y1, x2, y2, label, conf)

        # Apply Ghost Box if no fight detected but we have patience
        if not current_fight_found and self.last_fight_box is not None \
           and self.fight_patience < config.MAX_PATIENCE:
            self.fight_patience += 1
            frame_has_fight = 1  # Treat as fight frame

            x1, y1, x2, y2, label, conf = self.last_fight_box
            current_fight_box_coords = [x1, y1, x2, y2]

            # Draw ghost box (slightly transparent)
            self._draw_fight_box(frame, x1, y1, x2, y2, label, conf, is_ghost=True)

        return frame_has_fight, current_fight_found, max_fight_conf, current_fight_box_coords

    def _draw_fight_box(self, frame, x1, y1, x2, y2, label, conf, is_ghost=False):
        """Draw fight bounding box with unique styling."""

        color = config.COLOR_FIGHT

        # Add glow effect for high confidence fights
        if config.GLOW_ENABLED and conf > 0.3 and not is_ghost:
            draw_glow_effect(frame, (x1, y1), (x2, y2), color,
                           intensity=int(15 * min(conf / 0.3, 1.0)),
                           radius=config.BOX_CORNER_RADIUS)

        # Draw rounded rectangle box
        alpha = 0.6 if is_ghost else 1.0
        draw_rounded_rectangle(
            frame, (x1, y1), (x2, y2), color,
            thickness=config.BOX_THICKNESS,
            radius=config.BOX_CORNER_RADIUS,
            alpha=alpha
        )

        # Draw label with enhanced style
        draw_text_with_background(
            frame,
            label,
            (x1 + 5, y1 - 10),
            font_scale=config.FONT_SCALE_SMALL,
            text_color=config.COLOR_TEXT_PRIMARY,
            bg_color=config.COLOR_FIGHT,
            thickness=config.FONT_THICKNESS,
            padding=config.LABEL_PADDING,
            radius=config.BOX_CORNER_RADIUS // 2,
            alpha=0.9 if not is_ghost else 0.7
        )
