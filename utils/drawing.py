
import cv2


def draw_text_with_background(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, 
                              font_scale=0.6, text_color=(0, 0, 0), 
                              bg_color=(255, 255, 255), thickness=1):
    
    x, y = pos
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle
    cv2.rectangle(img, (x, y - text_h - 5), (x + text_w, y + 5), bg_color, -1)
    
    # Draw text
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)
