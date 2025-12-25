
import cv2
import time
import config


def draw_advanced_dashboard(frame, person_count, fight_active, fight_conf, 
                           fighting_people_ids, graph_history):
  
    h, w = frame.shape[:2]
    
    # Scale based on resolution (use width as reference)
    scale = min(w / 1000, config.DASHBOARD_SCALE_MAX)
    
    # Common Settings - all scaled
    bg_color = config.COLOR_BG
    alpha = config.DASHBOARD_ALPHA
    font = cv2.FONT_HERSHEY_SIMPLEX
    border_color = config.COLOR_BORDER
    border_thickness = max(1, int(2 * scale))
    
    # Font sizes scaled
    font_large = 0.8 * scale
    font_medium = 0.7 * scale
    font_small = 0.6 * scale
    text_thickness = max(2, int(3 * scale))
    
    # Animation frame counter (using time for smooth animation)
    anim_phase = int(time.time() * 3) % 20  # 0-19 cycle
    pulse = abs(anim_phase - 10) / 10.0  # 0.0 to 1.0 pulse
    
    # BOTTOM PANEL LAYOUT - Three sections side by side
    panel_h = int(120 * scale)  # Height of bottom panel
    panel_y = h - panel_h - int(20 * scale)  # Y position (bottom with margin)
    
    # Calculate widths for three sections
    margin = int(20 * scale)
    spacing = int(15 * scale)
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
    _draw_status_section(frame, s1_x, panel_y, s1_w, panel_h, bg_color, alpha,
                        border_color, border_thickness, fight_active, pulse,
                        person_count, font, font_medium, text_thickness, 
                        padding, scale)
    
    # --- SECTION 2: FIGHTING PEOPLE & INTENSITY (Bottom Middle) ---
    _draw_fighting_section(frame, s2_x, panel_y, s2_w, panel_h, bg_color, alpha,
                          border_color, border_thickness, fighting_people_ids,
                          fight_active, fight_conf, pulse, font, font_small,
                          font_medium, text_thickness, padding, scale)
    
    # --- SECTION 3: FREQUENCY GRAPH (Bottom Right) ---
    _draw_graph_section(frame, s3_x, panel_y, s3_w, panel_h, bg_color, alpha,
                       border_color, border_thickness, graph_history, scale)


def _draw_status_section(frame, x, y, w, h, bg_color, alpha, border_color,
                        border_thickness, fight_active, pulse, person_count,
                        font, font_medium, text_thickness, padding, scale):
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    # Pulsing border if fight active
    if fight_active:
        pulse_color = (int(255 * pulse), int(100 * pulse), int(100 * pulse))
        cv2.rectangle(frame, (x, y), (x + w, y + h), pulse_color, border_thickness + 1)
    else:
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, border_thickness)
    
    status_text = "STATUS: FIGHT ACTIVE" if fight_active else "STATUS: SAFE"
    status_color = config.COLOR_FIGHT if fight_active else config.COLOR_SAFE
    
    # Add glow effect to status text when fight active
    if fight_active:
        # Draw glow layers
        for i in range(3, 0, -1):
            glow_alpha = 0.3 * (4 - i) / 3
            glow_color = tuple(int(c * glow_alpha) for c in status_color)
            cv2.putText(frame, status_text, (x + padding - i, y + int(40 * scale) - i), 
                       font, font_medium, glow_color, text_thickness)
    
    # Status text
    cv2.putText(frame, status_text, (x + padding, y + int(40 * scale)), 
               font, font_medium, status_color, max(2, text_thickness - 1))
    # Total people in WHITE color
    cv2.putText(frame, f"TOTAL PEOPLE: {person_count}", 
               (x + padding, y + int(80 * scale)), 
               font, font_medium, (255, 255, 255), text_thickness)


def _draw_fighting_section(frame, x, y, w, h, bg_color, alpha, border_color,
                          border_thickness, fighting_people_ids, fight_active,
                          fight_conf, pulse, font, font_small, font_medium,
                          text_thickness, padding, scale):
    """Draw fighting people and intensity section."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, border_thickness)
    
    cv2.putText(frame, "FIGHTING PEOPLE:", (x + padding, y + int(30 * scale)), 
               font, font_small, (255, 255, 255), max(1, int(1 * scale)))
    
    # List people with animation
    y_offset = y + int(55 * scale)
    if not fighting_people_ids:
        cv2.putText(frame, "None", (x + padding, y_offset), 
                   font, font_small, (200, 200, 200), max(1, int(1 * scale)))
    else:
        ids_str = ", ".join([f"P{pid}" for pid in fighting_people_ids[:4]])
        # Pulsing effect on fighting people
        pulse_red = int(255 - 55 * pulse)
        cv2.putText(frame, ids_str, (x + padding, y_offset), 
                   font, font_medium, (pulse_red, 0, 255), text_thickness)
        
    # Intensity Bar with gradient
    cv2.putText(frame, "INTENSITY:", (x + padding, y + int(95 * scale)), 
               font, font_small, (255, 255, 255), max(1, int(1 * scale)))
    
    bar_x = x + int(150 * scale)
    bar_y = y + int(83 * scale)
    bar_w = int(150 * scale)
    bar_h = int(12 * scale)
    
    # Draw bar background
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), 
                 (50, 50, 50), -1)
    
    if fight_active:
        fill_ratio = min(max((fight_conf - 0.15) / (0.85), 0), 1)
        fill_w = int(bar_w * fill_ratio)
        
        # Create gradient effect
        for i in range(fill_w):
            ratio = i / bar_w
            if ratio > 0.6:
                color = (0, int(100 * (1 - ratio)), 255)  # Red
            else:
                color = (0, int(255 * (1 - ratio)), int(255 * ratio))  # Yellow to Orange
            cv2.line(frame, (bar_x + i, bar_y), (bar_x + i, bar_y + bar_h), color, 1)


def _draw_graph_section(frame, x, y, w, h, bg_color, alpha, border_color,
                       border_thickness, graph_history, scale):
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, border_thickness)
    
    # Draw Graph with glow effect
    if len(graph_history) > 1:
        points = []
        graph_padding = int(10 * scale)
        graph_w = w - (2 * graph_padding)
        graph_h = h - (2 * graph_padding)
        
        for i, val in enumerate(graph_history):
            px = int(x + graph_padding + (i / 100) * graph_w)
            py = int((y + h - graph_padding) - (val * graph_h))
            points.append((px, py))
        
        # Draw glow layers
        for thickness in [6, 4, 2]:
            glow_alpha = 0.3 if thickness == 6 else (0.5 if thickness == 4 else 1.0)
            glow_color = tuple(int(c * glow_alpha) for c in (0, 255, 0))
            for i in range(1, len(points)):
                cv2.line(frame, points[i-1], points[i], glow_color, 
                        max(1, int(thickness * scale)))
        
        # Main line
        for i in range(1, len(points)):
            cv2.line(frame, points[i-1], points[i], (0, 255, 0), 
                    max(1, int(2 * scale)))
