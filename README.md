# VAMS - Violence Analysis & Monitoring System

A real-time video processing system that detects fights and tracks people using advanced YOLO deep learning models. VAMS provides comprehensive violence detection with visual analytics through an intelligent dashboard overlay.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-v11-orange.svg)

## Features

### Core Capabilities
- **Fight Detection**: Custom-trained YOLOv11 model for accurate fight detection in video footage
- **Person Tracking**: Real-time person detection and tracking with unique ID assignment
- **Temporal Confirmation**: Smart windowing algorithm reduces false positives by requiring multiple frame confirmations
- **Ghost Box Persistence**: Smooths detection output by maintaining bounding boxes for several frames
- **Multi-Video Processing**: Process and merge multiple video files into a single analyzed output

### Advanced Dashboard Visualization
Real-time overlay with three analytical sections:
- **Status Panel**: Fight status indicator with animated pulsing effects + total people count
- **Activity Panel**: List of fighting person IDs + intensity bar with color gradient
- **Analytics Panel**: Real-time frequency graph showing fight intensity over time

### Technical Features
- Configurable confidence thresholds and detection parameters
- Responsive dashboard scaling based on video resolution
- XVID codec video output with customizable FPS
- Frame-by-frame processing with temporal windowing
- Alpha-blended dashboard with smooth animations

---

## Project Structure

```
VAMS/
├── config.py                    # Centralized configuration
├── main.py                      # Application entry point
├── test_setup.py                # Installation verification script
├── requirements.txt             # Python dependencies
├── weights/                     # YOLO model weights
│   ├── best.pt
│   └── last.pt
├── videos/                      # Input videos (create this folder)
├── detection/                   # Detection modules
│   ├── fight_detector.py        # Fight detection with ghost boxes
│   └── person_tracker.py        # Person tracking with YOLO
├── processing/                  # Video processing pipeline
│   └── video_processor.py       # Main orchestrator
├── visualization/               # Dashboard rendering
│   └── dashboard.py             # Advanced overlay graphics
└── utils/                       # Helper utilities
    ├── drawing.py               # Text rendering functions
    └── geometry.py              # Geometric calculations
```

---

## Requirements

- Python 3.8+
- OpenCV (`cv2`)
- Ultralytics YOLO (`ultralytics`)
---

## Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd VAMS
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python test_setup.py
```

You should see:
```
[SUCCESS] All tests passed! VAMS is ready to use.
```

---

## Quick Start

### 1. Prepare Your Video
Place your video file in the `videos/` folder:
```bash
mkdir videos
# Copy your video file to videos/
```

### 2. Update Configuration
Edit `config.py` and update the video path:

```python
VIDEO_PATHS = [
    r"./VAMS/videos/your_video.avi",
]
```

### 3. Run VAMS
```bash
python main.py
```

### 4. Check Output
The processed video will be saved to:
```
G:\Github\VAMS\output_fight_detection.mp4
```

---

## Configuration

All settings are centralized in `config.py`:

### Model Paths
```python
FIGHT_MODEL_PATH = r"./VAMS/weights/last.pt"
PERSON_MODEL_PATH = "yolo11x.pt"
```

### Input/Output
```python
VIDEO_PATHS = [
    r"./VAMS/videos/video1.avi",
    r"./VAMS/videos/video2.avi",
]
OUTPUT_PATH = r"./VAMS/output_fight_detection.mp4"
```

### Detection Parameters
```python
CONF_THRESHOLD = 0.15           # Fight detection confidence (0-1)
                                # Lower = more sensitive, higher = stricter
PERSON_CONF_THRESHOLD = 0.3     # Person detection confidence
IMG_SIZE = 960                  # YOLO input image size
```

### Temporal Logic
```python
WINDOW = 15                     # Temporal window size (frames)
FIGHT_TRIGGER = 6               # Min detections in window to confirm fight
MAX_PATIENCE = 10               # Ghost box persistence (frames)
```

### Dashboard Settings
```python
DASHBOARD_ALPHA = 0.8           # Transparency (0-1)
GRAPH_HISTORY_SIZE = 100        # Intensity graph data points
```

### Colors (BGR Format)
```python
COLOR_FIGHT = (0, 0, 255)       # Red
COLOR_SAFE = (0, 255, 0)        # Green
COLOR_PERSON = (255, 0, 0)      # Blue
```

---

## How It Works

### Fight Detection Pipeline

```
Video Frame
    ↓
[Fight Detector]
    ├─ YOLO inference
    ├─ Confidence filtering (CONF_THRESHOLD)
    ├─ Ghost box persistence (MAX_PATIENCE)
    └─ Bounding box extraction
    ↓
[Person Tracker]
    ├─ YOLO person detection
    ├─ Unique ID assignment
    ├─ Track persistence
    └─ Fight zone overlap check
    ↓
[Temporal Confirmation]
    ├─ Sliding window (WINDOW frames)
    ├─ Count detections in window
    └─ Confirm if >= FIGHT_TRIGGER
    ↓
[Dashboard Visualization]
    ├─ Status indicator (SAFE/ACTIVE)
    ├─ Person count & fighting IDs
    ├─ Intensity bar gradient
    └─ Real-time frequency graph
    ↓
Processed Frame → Output Video
```

### Key Algorithms

**Ghost Box Persistence**: Maintains fight detection boxes for 10 frames after detection disappears, reducing visual flickering.

**Temporal Windowing**: Uses a 15-frame sliding window requiring 6+ detections to confirm a fight, dramatically reducing false positives.

**Point-in-Box Detection**: People are marked as "fighting" only if their center point falls within the fight bounding box.

---

## Usage Examples

### Process Single Video
```python
# config.py
VIDEO_PATHS = [r"videos\fight_scene.avi"]
```

### Process Multiple Videos (Merged Output)
```python
# config.py
VIDEO_PATHS = [
    r"videos\scene1.avi",
    r"videos\scene2.avi",
    r"videos\scene3.avi",
]
```

### Adjust Detection Sensitivity
```python
# More sensitive (more detections, more false positives)
CONF_THRESHOLD = 0.10
FIGHT_TRIGGER = 4

# Stricter (fewer detections, fewer false positives)
CONF_THRESHOLD = 0.25
FIGHT_TRIGGER = 8
```

---

## Output

### Console Output
```
The system generates:
- A merged video file with all detections and dashboard overlay
- Console output showing processing progress
- Final statistics including:
  - Total frames processed
  - Frames with confirmed fights
  - Fight percentage

### Video Output
- **Format**: MP4 (H.264)
- **Codec**: XVID with fallback to mp4v
- **Resolution**: Same as input video
- **FPS**: Same as input video
- **Overlay**: Advanced dashboard with real-time analytics

---

