
import cv2
from ultralytics import YOLO
import config
from utils.drawing import draw_text_with_background
from utils.geometry import point_in_box


class PersonTracker:


    def __init__(self, model_path=None):

        model_path = model_path or config.PERSON_MODEL_PATH
        self.model = YOLO(model_path)

    def track(self, frame, fight_box_coords=None):

        person_results = self.model.track(
            source=frame,
            classes=[0],  # 0 is person class
            conf=config.PERSON_CONF_THRESHOLD,
            persist=True,
            verbose=False
        )

        person_count = 0
        fighting_people_ids = []

        for r in person_results:
            if r.boxes is None:
                continue

            person_count += len(r.boxes)

            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                # Get ID if available
                p_id = int(box.id[0]) if box.id is not None else -1

                # Calculate center of person
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Check if person's CENTER is inside fight box (stricter check)
                is_fighting = False
                if fight_box_coords:
                    if point_in_box((cx, cy), fight_box_coords):
                        if p_id != -1:
                            fighting_people_ids.append(p_id)
                        is_fighting = True

                # Draw person label with unique styling
                label = f"P{p_id}" if p_id != -1 else f"P?"
                self._draw_person_label(frame, cx, cy, label, is_fighting)

        return person_count, fighting_people_ids

    def _draw_person_label(self, frame, cx, cy, label, is_fighting=False):
        """Draw person label with unique rounded styling."""

        # Use different colors for fighting vs non-fighting people
        if is_fighting:
            text_color = config.COLOR_TEXT_PRIMARY
            bg_color = config.COLOR_DANGER
        else:
            text_color = config.COLOR_TEXT_PRIMARY
            bg_color = config.COLOR_PERSON

        draw_text_with_background(
            frame,
            label,
            (cx - 15, cy + 5),
            font_scale=config.FONT_SCALE_SMALL,
            text_color=text_color,
            bg_color=bg_color,
            thickness=config.FONT_THICKNESS,
            padding=8,
            radius=config.BOX_CORNER_RADIUS // 2,
            alpha=0.9
        )
