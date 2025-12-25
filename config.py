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
# DASHBOARD COLORS (BGR)
# ========================
COLOR_BG = (0, 0, 0)           # Black background
COLOR_BORDER = (255, 255, 255) # White border
COLOR_FIGHT = (0, 0, 255)      # Red for fight
COLOR_SAFE = (0, 255, 0)       # Green for safe
COLOR_PERSON = (255, 0, 0)     # Blue for person labels
COLOR_TEXT_BG = (255, 255, 255) # White background for text

# ========================
# DASHBOARD SETTINGS
# ========================
DASHBOARD_ALPHA = 0.8  # Transparency for dashboard panels
DASHBOARD_SCALE_MAX = 1.2  # Maximum scale factor for large videos
