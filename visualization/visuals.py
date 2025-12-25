
import cv2
import time
import config
from utils.drawing import draw_rounded_rectangle, draw_shadow_rectangle, draw_text_with_outline, draw_glow_effect, draw_watermark


def draw_advanced_dashboard(frame, person_count, fight_active, fight_conf,
                           fighting_people_ids, graph_history):

    h, w = frame.shape[:2]

    # Scale based on resolution (use width as reference)
    scale = min(w / 1000, config.DASHBOARD_SCALE_MAX)

    # Common Settings - all scaled
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Font sizes scaled using config
    font_large = config.FONT_SCALE_LARGE * scale
    font_medium = config.FONT_SCALE_MEDIUM * scale
    font_small = config.FONT_SCALE_SMALL * scale
    text_thickness = config.FONT_THICKNESS

    # Animation frame counter (using time for smooth animation)
    anim_phase = int(time.time() * 3) % 20  # 0-19 cycle
    pulse = abs(anim_phase - 10) / 10.0  # 0.0 to 1.0 pulse

    # BOTTOM PANEL LAYOUT - Three sections side by side
    panel_h = int(130 * scale)  # Height of bottom panel (slightly taller for rounded corners)
    panel_y = h - panel_h - int(25 * scale)  # Y position (bottom with margin)

    # Calculate widths for three sections
    margin = int(25 * scale)
    spacing = int(20 * scale)
    total_width = w - (2 * margin) - (2 * spacing)  # Total available width

    # Section widths
    s1_w = int(total_width * 0.30)  # Status & People: 30%
    s2_w = int(total_width * 0.35)  # Fighting Info: 35%
    s3_w = int(total_width * 0.35)  # Graph: 35%

    # Section X positions
    s1_x = margin
    s2_x = s1_x + s1_w + spacing
    s3_x = s2_x + s2_w + spacing

    padding = int(15 * scale)

    # --- SECTION 1: STATUS & TOTAL PEOPLE (Bottom Left) ---
    _draw_status_section(frame, s1_x, panel_y, s1_w, panel_h,
                        fight_active, pulse, person_count, font, font_medium,
                        text_thickness, padding, scale)

    # --- SECTION 2: FIGHTING PEOPLE & INTENSITY (Bottom Middle) ---
    _draw_fighting_section(frame, s2_x, panel_y, s2_w, panel_h,
                          fighting_people_ids, fight_active, fight_conf, pulse,
                          font, font_small, font_medium, text_thickness, padding, scale)

    # --- SECTION 3: FREQUENCY GRAPH (Bottom Right) ---
    _draw_graph_section(frame, s3_x, panel_y, s3_w, panel_h, graph_history, scale)

    # Add watermark if enabled
    if config.ENABLE_WATERMARK:
        draw_watermark(frame, config.WATERMARK_TEXT, config.WATERMARK_POSITION, config.WATERMARK_ALPHA)


def _draw_status_section(frame, x, y, w, h, fight_active, pulse, person_count,
                        font, font_medium, text_thickness, padding, scale):
    """Draw status and total people section with unique rounded style."""

    # Draw panel with shadow
    radius = int(config.PANEL_CORNER_RADIUS * scale)
    draw_shadow_rectangle(
        frame, (x, y), (x + w, y + h),
        config.COLOR_PANEL_BG,
        shadow_offset=config.PANEL_SHADOW_OFFSET,
        radius=radius,
        alpha=config.DASHBOARD_ALPHA
    )

    # Pulsing border/glow if fight active
    if fight_active and config.GLOW_ENABLED:
        glow_color = config.COLOR_FIGHT
        draw_glow_effect(frame, (x, y), (x + w, y + h), glow_color,
                        intensity=int(15 * pulse), radius=radius)

    # Draw border
    border_color = config.COLOR_FIGHT if fight_active else config.COLOR_BORDER
    border_thickness = max(2, int(3 * scale)) if fight_active else max(1, int(2 * scale))
    draw_rounded_rectangle(frame, (x, y), (x + w, y + h), border_color,
                          thickness=border_thickness, radius=radius, alpha=1.0)

    status_text = "FIGHT ACTIVE" if fight_active else "SAFE"
    status_color = config.COLOR_FIGHT if fight_active else config.COLOR_SUCCESS

    # Status text with outline
    draw_text_with_outline(
        frame, status_text, (x + padding, y + int(45 * scale)),
        font, font_medium, status_color,
        outline_color=(0, 0, 0), thickness=text_thickness, outline_thickness=2
    )

    # Total people in white color
    draw_text_with_outline(
        frame, f"PEOPLE: {person_count}",
        (x + padding, y + int(85 * scale)),
        font, font_medium, config.COLOR_TEXT_PRIMARY,
        outline_color=(0, 0, 0), thickness=text_thickness - 1, outline_thickness=1
    )


def _draw_fighting_section(frame, x, y, w, h, fighting_people_ids, fight_active,
                          fight_conf, pulse, font, font_small, font_medium,
                          text_thickness, padding, scale):
    """Draw fighting people and intensity section with unique style."""

    # Draw panel with shadow
    radius = int(config.PANEL_CORNER_RADIUS * scale)
    draw_shadow_rectangle(
        frame, (x, y), (x + w, y + h),
        config.COLOR_PANEL_BG,
        shadow_offset=config.PANEL_SHADOW_OFFSET,
        radius=radius,
        alpha=config.DASHBOARD_ALPHA
    )

    # Border
    draw_rounded_rectangle(frame, (x, y), (x + w, y + h), config.COLOR_BORDER,
                          thickness=max(1, int(2 * scale)), radius=radius, alpha=1.0)

    # Header
    draw_text_with_outline(
        frame, "FIGHTING:",
        (x + padding, y + int(30 * scale)),
        font, font_small, config.COLOR_TEXT_SECONDARY,
        outline_color=(0, 0, 0), thickness=max(1, int(1 * scale)), outline_thickness=1
    )

    # List people with animation
    y_offset = y + int(60 * scale)
    if not fighting_people_ids:
        draw_text_with_outline(
            frame, "None",
            (x + padding, y_offset),
            font, font_medium, config.COLOR_TEXT_SECONDARY,
            outline_color=(0, 0, 0), thickness=text_thickness - 1, outline_thickness=1
        )
    else:
        ids_str = ", ".join([f"P{pid}" for pid in fighting_people_ids[:4]])
        # Pulsing effect on fighting people
        pulse_intensity = 0.7 + 0.3 * pulse
        fighting_color = tuple(int(c * pulse_intensity) for c in config.COLOR_DANGER)
        draw_text_with_outline(
            frame, ids_str,
            (x + padding, y_offset),
            font, font_medium, fighting_color,
            outline_color=(0, 0, 0), thickness=text_thickness, outline_thickness=1
        )

    # Intensity Bar with gradient
    draw_text_with_outline(
        frame, "INTENSITY:",
        (x + padding, y + int(100 * scale)),
        font, font_small, config.COLOR_TEXT_SECONDARY,
        outline_color=(0, 0, 0), thickness=max(1, int(1 * scale)), outline_thickness=1
    )

    bar_x = x + int(140 * scale)
    bar_y = y + int(88 * scale)
    bar_w = int(150 * scale)
    bar_h = int(15 * scale)
    bar_radius = int(8 * scale)

    # Draw bar background with rounded corners
    draw_rounded_rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h),
                          (30, 30, 30), -1, bar_radius, 1.0)

    if fight_active:
        fill_ratio = min(max((fight_conf - 0.15) / (0.85), 0), 1)
        fill_w = int(bar_w * fill_ratio)

        # Create gradient effect
        for i in range(fill_w):
            ratio = i / bar_w
            if ratio > 0.7:
                color = config.COLOR_DANGER  # Red
            elif ratio > 0.4:
                color = config.COLOR_WARNING  # Orange
            else:
                color = (0, int(200 * (1 - ratio)), int(200 * ratio))  # Green to yellow
            cv2.line(frame, (bar_x + i, bar_y + 2), (bar_x + i, bar_y + bar_h - 2), color, 1)


def _draw_graph_section(frame, x, y, w, h, graph_history, scale):
    """Draw frequency graph section with unique style."""

    # Draw panel with shadow
    radius = int(config.PANEL_CORNER_RADIUS * scale)
    draw_shadow_rectangle(
        frame, (x, y), (x + w, y + h),
        config.COLOR_PANEL_BG,
        shadow_offset=config.PANEL_SHADOW_OFFSET,
        radius=radius,
        alpha=config.DASHBOARD_ALPHA
    )

    # Border
    draw_rounded_rectangle(frame, (x, y), (x + w, y + h), config.COLOR_BORDER,
                          thickness=max(1, int(2 * scale)), radius=radius, alpha=1.0)

    # Draw Graph with glow effect
    if len(graph_history) > 1:
        points = []
        graph_padding = int(15 * scale)
        graph_w = w - (2 * graph_padding)
        graph_h = h - (2 * graph_padding)

        for i, val in enumerate(graph_history):
            px = int(x + graph_padding + (i / 100) * graph_w)
            py = int((y + h - graph_padding) - (val * graph_h))
            points.append((px, py))

        # Draw glow layers for unique effect
        if config.GLOW_ENABLED:
            for thickness_mult in [3, 2, 1]:
                glow_alpha = 0.2 if thickness_mult == 3 else (0.4 if thickness_mult == 2 else 0.7)
                glow_color = tuple(int(c * glow_alpha) for c in config.COLOR_SUCCESS)
                for i in range(1, len(points)):
                    cv2.line(frame, points[i-1], points[i], glow_color,
                            max(1, int(thickness_mult * 2 * scale)), cv2.LINE_AA)

        # Main line with unique color
        for i in range(1, len(points)):
            cv2.line(frame, points[i-1], points[i], config.COLOR_SUCCESS,
                    max(2, int(2 * scale)), cv2.LINE_AA)
