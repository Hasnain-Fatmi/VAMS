
import cv2
import numpy as np
import config


def draw_rounded_rectangle(img, pt1, pt2, color, thickness=-1, radius=15, alpha=1.0):
    """
    Draw a rectangle with rounded corners.

    Args:
        img: Image to draw on
        pt1: Top-left corner (x, y)
        pt2: Bottom-right corner (x, y)
        color: Color in BGR
        thickness: Line thickness (-1 for filled)
        radius: Corner radius
        alpha: Transparency (0-1)
    """
    x1, y1 = pt1
    x2, y2 = pt2

    # Create overlay for transparency
    if alpha < 1.0:
        overlay = img.copy()
    else:
        overlay = img

    # Draw rectangles and circles for rounded corners
    if thickness == -1:  # Filled
        # Main rectangles
        cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)

        # Corner circles
        cv2.circle(overlay, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(overlay, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(overlay, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(overlay, (x2 - radius, y2 - radius), radius, color, -1)
    else:  # Outline
        # Draw lines
        cv2.line(overlay, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(overlay, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(overlay, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(overlay, (x2, y1 + radius), (x2, y2 - radius), color, thickness)

        # Corner arcs
        cv2.ellipse(overlay, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(overlay, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(overlay, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(overlay, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)

    # Apply transparency
    if alpha < 1.0:
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


def draw_shadow_rectangle(img, pt1, pt2, color, shadow_offset=5, radius=15, alpha=0.85):
    """
    Draw a rectangle with drop shadow effect.

    Args:
        img: Image to draw on
        pt1: Top-left corner (x, y)
        pt2: Bottom-right corner (x, y)
        color: Color in BGR
        shadow_offset: Shadow offset in pixels
        radius: Corner radius
        alpha: Transparency
    """
    x1, y1 = pt1
    x2, y2 = pt2

    # Draw shadow (darker, offset)
    shadow_color = tuple(int(c * 0.3) for c in color)
    draw_rounded_rectangle(
        img,
        (x1 + shadow_offset, y1 + shadow_offset),
        (x2 + shadow_offset, y2 + shadow_offset),
        shadow_color,
        -1,
        radius,
        alpha * 0.4
    )

    # Draw main rectangle
    draw_rounded_rectangle(img, pt1, pt2, color, -1, radius, alpha)


def draw_text_with_outline(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX,
                           font_scale=0.6, text_color=(255, 255, 255),
                           outline_color=(0, 0, 0), thickness=1, outline_thickness=3):
    """
    Draw text with an outline for better visibility.

    Args:
        img: Image to draw on
        text: Text string
        pos: Position (x, y)
        font: OpenCV font
        font_scale: Font scale
        text_color: Text color in BGR
        outline_color: Outline color in BGR
        thickness: Text thickness
        outline_thickness: Outline thickness
    """
    x, y = pos

    # Draw outline
    cv2.putText(img, text, (x, y), font, font_scale, outline_color, thickness + outline_thickness, cv2.LINE_AA)

    # Draw text
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness, cv2.LINE_AA)


def draw_text_with_background(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX,
                              font_scale=0.6, text_color=(255, 255, 255),
                              bg_color=(45, 45, 45), thickness=2,
                              padding=10, radius=8, alpha=0.9):
    """
    Enhanced text drawing with rounded background and padding.

    Args:
        img: Image to draw on
        text: Text string
        pos: Position (x, y)
        font: OpenCV font
        font_scale: Font scale
        text_color: Text color in BGR
        bg_color: Background color in BGR
        thickness: Text thickness
        padding: Padding around text
        radius: Corner radius
        alpha: Background transparency
    """
    x, y = pos
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Draw rounded background with shadow
    bg_x1 = x - padding
    bg_y1 = y - text_h - padding
    bg_x2 = x + text_w + padding
    bg_y2 = y + padding

    if config.SHADOW_ENABLED:
        draw_shadow_rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color,
                            shadow_offset=config.PANEL_SHADOW_OFFSET,
                            radius=radius, alpha=alpha)
    else:
        draw_rounded_rectangle(img, (bg_x1, bg_y1), (bg_x2, bg_y2), bg_color, -1, radius, alpha)

    # Draw text with outline for better visibility
    draw_text_with_outline(img, text, (x, y), font, font_scale, text_color,
                          outline_color=(0, 0, 0), thickness=thickness, outline_thickness=1)


def draw_glow_effect(img, pt1, pt2, color, intensity=20, radius=15):
    """
    Draw a glow effect around a rectangle.

    Args:
        img: Image to draw on
        pt1: Top-left corner (x, y)
        pt2: Bottom-right corner (x, y)
        color: Glow color in BGR
        intensity: Glow intensity (thickness)
        radius: Corner radius
    """
    x1, y1 = pt1
    x2, y2 = pt2

    # Draw multiple layers with decreasing opacity
    for i in range(intensity, 0, -2):
        alpha = 0.05 * (intensity - i) / intensity
        glow_color = tuple(int(c * 0.8) for c in color)
        draw_rounded_rectangle(
            img,
            (x1 - i, y1 - i),
            (x2 + i, y2 + i),
            glow_color,
            2,
            radius + i,
            alpha
        )


def draw_watermark(img, text="VAMS", position="bottom-right", alpha=0.3):
    """
    Draw a watermark on the image.

    Args:
        img: Image to draw on
        text: Watermark text
        position: Position (top-left, top-right, bottom-left, bottom-right)
        alpha: Transparency
    """
    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    thickness = 3

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)

    # Calculate position
    margin = 20
    if position == "top-left":
        pos = (margin, margin + text_h)
    elif position == "top-right":
        pos = (w - text_w - margin, margin + text_h)
    elif position == "bottom-left":
        pos = (margin, h - margin)
    else:  # bottom-right
        pos = (w - text_w - margin, h - margin)

    # Draw watermark with transparency
    overlay = img.copy()
    cv2.putText(overlay, text, pos, font, font_scale, (200, 200, 200), thickness, cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
