"""
Test script to verify VAMS setup without processing videos.
Tests imports, model loading, and basic functionality.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("\n" + "=" * 60)
    print("Testing Imports...")
    print("=" * 60)

    try:
        import cv2
        print(f"[OK] OpenCV imported successfully (version: {cv2.__version__})")
    except ImportError as e:
        print(f"[FAIL] Failed to import OpenCV: {e}")
        return False

    try:
        import ultralytics
        print(f"[OK] Ultralytics imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import Ultralytics: {e}")
        return False

    try:
        import config
        print(f"[OK] Config module imported successfully")
        print(f"  - Fight model path: {config.FIGHT_MODEL_PATH}")
        print(f"  - Person model path: {config.PERSON_MODEL_PATH}")
        print(f"  - Output path: {config.OUTPUT_PATH}")
    except ImportError as e:
        print(f"[FAIL] Failed to import config: {e}")
        return False

    try:
        from detection.fight_detector import FightDetector
        print(f"[OK] FightDetector imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import FightDetector: {e}")
        return False

    try:
        from detection.person_tracker import PersonTracker
        print(f"[OK] PersonTracker imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import PersonTracker: {e}")
        return False

    try:
        from visualization.dashboard import draw_advanced_dashboard
        print(f"[OK] Dashboard module imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import Dashboard module: {e}")
        return False

    try:
        from processing.video_processor import VideoProcessor
        print(f"[OK] VideoProcessor imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import VideoProcessor: {e}")
        return False

    return True


def test_model_files():
    """Test that required model files exist."""
    print("\n" + "=" * 60)
    print("Testing Model Files...")
    print("=" * 60)

    import config

    # Check fight detection model
    if os.path.exists(config.FIGHT_MODEL_PATH):
        size_mb = os.path.getsize(config.FIGHT_MODEL_PATH) / (1024 * 1024)
        print(f"[OK] Fight detection model found: {config.FIGHT_MODEL_PATH}")
        print(f"  Size: {size_mb:.2f} MB")
    else:
        print(f"[FAIL] Fight detection model not found: {config.FIGHT_MODEL_PATH}")
        return False

    # Person model will be auto-downloaded by Ultralytics if needed
    print(f"[OK] Person model will be auto-downloaded if needed: {config.PERSON_MODEL_PATH}")

    return True


def test_model_loading():
    """Test that models can be loaded."""
    print("\n" + "=" * 60)
    print("Testing Model Loading...")
    print("=" * 60)

    try:
        print("Loading fight detection model...")
        from detection.fight_detector import FightDetector
        fight_detector = FightDetector()
        print("[OK] Fight detection model loaded successfully")
    except Exception as e:
        print(f"[FAIL] Failed to load fight detection model: {e}")
        return False

    try:
        print("Loading person tracking model...")
        from detection.person_tracker import PersonTracker
        person_tracker = PersonTracker()
        print("[OK] Person tracking model loaded successfully")
        print("  (YOLOv11x may have been downloaded automatically)")
    except Exception as e:
        print(f"[FAIL] Failed to load person tracking model: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("\n" * 2)
    print("=" * 60)
    print("VAMS Setup Verification")
    print("=" * 60)

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False
        print("\n[WARNING] Import test failed!")

    # Test model files
    if not test_model_files():
        all_passed = False
        print("\n[WARNING] Model file test failed!")

    # Test model loading
    if not test_model_loading():
        all_passed = False
        print("\n[WARNING] Model loading test failed!")

    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed! VAMS is ready to use.")
        print("=" * 60)
        print("\nTo process videos:")
        print("1. Add video paths to config.py VIDEO_PATHS list")
        print("2. Run: python main.py")
        print("=" * 60)
    else:
        print("[ERROR] Some tests failed. Please fix the issues above.")
        print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
