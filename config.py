"""
Configuration module for fight detection system.
Contains all settings, paths, and constants.
"""

# ========================
# MODEL PATHS
# ========================
FIGHT_MODEL_PATH = r"G:\Github\VAMS\weights\last.pt"
PERSON_MODEL_PATH = "yolo11x.pt"  # Ultralytics will auto-download if not found

# ========================
# VIDEO PATHS
# ========================
VIDEO_PATHS = [
    r"G:\Github\VAMS\videos\newfi37.avi",
]

OUTPUT_PATH = r"G:\Github\VAMS\output_fight_detection.mp4"

# ========================
# DETECTION PARAMETERS
# ========================
CONF_THRESHOLD = 0.15
IMG_SIZE = 960
PERSON_CONF_THRESHOLD = 0.3

# ========================
# TEMPORAL WINDOW SETTINGS
# ========================
WINDOW = 15          # frames
FIGHT_TRIGGER = 6    # minimum frames in window to confirm fight

# ========================
# PERSISTENCE SETTINGS
# ========================
MAX_PATIENCE = 10    # frames to keep ghost box after fight disappears

# ========================
# GRAPH SETTINGS
# ========================
GRAPH_HISTORY_SIZE = 100  # number of intensity values to store

# ========================
# VIDEO OUTPUT SETTINGS
# ========================
FOURCC = 'XVID'  # Video codec
DEFAULT_FPS = 25  # Default FPS if video metadata is unavailable

# ========================
# VISUAL THEME - UNIQUE PROFESSIONAL STYLE
# ========================

# Primary Colors (BGR format) - Professional Dark Theme
COLOR_PRIMARY = (220, 140, 30)      # Orange/Gold accent
COLOR_SECONDARY = (180, 90, 200)    # Purple accent
COLOR_SUCCESS = (100, 200, 50)      # Bright green
COLOR_DANGER = (50, 50, 255)        # Bright red
COLOR_WARNING = (0, 200, 255)       # Yellow/Orange

# Background Colors
COLOR_BG = (30, 30, 30)            # Dark gray background
COLOR_PANEL_BG = (45, 45, 45)      # Panel background
COLOR_BORDER = (100, 100, 100)     # Gray border

# Detection Colors
COLOR_FIGHT = (50, 50, 255)        # Bright red for fight
COLOR_SAFE = (100, 200, 50)        # Bright green for safe
COLOR_PERSON = (220, 140, 30)      # Orange for person labels

# Text Colors
COLOR_TEXT_PRIMARY = (255, 255, 255)   # White text
COLOR_TEXT_SECONDARY = (200, 200, 200) # Light gray text
COLOR_TEXT_BG = (45, 45, 45)           # Dark background for text

# Visual Effects
BOX_THICKNESS = 3                  # Thickness of bounding boxes
BOX_CORNER_RADIUS = 12             # Rounded corner radius
LABEL_PADDING = 10                 # Padding inside labels
SHADOW_ENABLED = True              # Enable drop shadows
GLOW_ENABLED = True                # Enable glow effects

# Dashboard Design
DASHBOARD_ALPHA = 0.85             # Transparency for dashboard panels
DASHBOARD_SCALE_MAX = 1.2          # Maximum scale factor for large videos
PANEL_CORNER_RADIUS = 15           # Rounded corners for panels
PANEL_SHADOW_OFFSET = 5            # Shadow offset in pixels

# Typography
FONT_SCALE_LARGE = 1.0             # Large text
FONT_SCALE_MEDIUM = 0.8            # Medium text
FONT_SCALE_SMALL = 0.6             # Small text
FONT_THICKNESS = 2                 # Font thickness

# Branding (Optional)
ENABLE_WATERMARK = False           # Show watermark (disabled by default)
WATERMARK_TEXT = "VAMS"            # Watermark text
WATERMARK_POSITION = "bottom-right" # Position: top-left, top-right, bottom-left, bottom-right
WATERMARK_ALPHA = 0.3              # Watermark transparency
