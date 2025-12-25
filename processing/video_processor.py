
import cv2
from collections import deque
import config
from detection import FightDetector, PersonTracker
from visualization import draw_advanced_dashboard


class VideoProcessor:
    
    def __init__(self, video_paths=None, output_path=None):
        """
        Initialize video processor.
        
        Args:
            video_paths: List of input video paths (defaults to config)
            output_path: Output video path (defaults to config)
        """
        self.video_paths = video_paths or config.VIDEO_PATHS
        self.output_path = output_path or config.OUTPUT_PATH
        
        # Initialize detectors
        self.fight_detector = FightDetector()
        self.person_tracker = PersonTracker()
        
        # Statistics
        self.frame_count = 0
        self.fight_frame_count = 0
        
        # Temporal state
        self.fight_history = deque(maxlen=config.WINDOW)
        self.graph_history = deque(maxlen=config.GRAPH_HISTORY_SIZE)
        
        # Video writer
        self.video_writer = None
        
    def process(self):
       
        # Initialize video writer from first video
        self._initialize_video_writer()
        
        # Process each video
        for video_path in self.video_paths:
            print(f"\n📽️ Processing: {video_path}")
            self._process_video(video_path)
        
        # Cleanup
        self._cleanup()
        
        # Print summary
        self._print_summary()
        
        return {
            'total_frames': self.frame_count,
            'fight_frames': self.fight_frame_count
        }
    
    def _initialize_video_writer(self):
       
        first_video = cv2.VideoCapture(self.video_paths[0])
        
        if not first_video.isOpened():
            raise RuntimeError(f"❌ Error: Could not open first video: {self.video_paths[0]}")
        
        width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = first_video.get(cv2.CAP_PROP_FPS)
        fps = config.DEFAULT_FPS if fps == 0 else fps
        first_video.release()
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*config.FOURCC)
        self.video_writer = cv2.VideoWriter(
            self.output_path, fourcc, fps, (width, height)
        )
        
        print(f"📹 Output video: {width}x{height} @ {fps} FPS")
    
    def _process_video(self, video_path):
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Skipping: {video_path}")
            return
        
        print("✅ Opened successfully")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            
            # Process frame
            self._process_frame(frame)
            
            # Write and display
            self.video_writer.write(frame)
            cv2.imshow("Fight Detection", frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
    
    def _process_frame(self, frame):
        
        # Fight detection
        frame_has_fight, current_fight_found, max_fight_conf, fight_box_coords = \
            self.fight_detector.detect(frame)
        
        # Person tracking
        person_count, fighting_people_ids = \
            self.person_tracker.track(frame, fight_box_coords)
        
        # Update graph history
        current_intensity = 0.0
        if frame_has_fight:
            current_intensity = max_fight_conf if max_fight_conf > 0 else 0.5
        self.graph_history.append(current_intensity)
        
        # Draw dashboard
        draw_advanced_dashboard(
            frame, person_count, frame_has_fight, max_fight_conf,
            fighting_people_ids, self.graph_history
        )
        
        # Temporal logic for fight confirmation
        self.fight_history.append(frame_has_fight)
        if sum(self.fight_history) >= config.FIGHT_TRIGGER:
            self.fight_frame_count += 1
    
    def _cleanup(self):
        
        if self.video_writer:
            self.video_writer.release()
        cv2.destroyAllWindows()
    
    def _print_summary(self):
        
        print("\n✅ Done - All Videos Merged")
        print(f"Total Frames: {self.frame_count}")
        print(f"Fight confirmed frames: {self.fight_frame_count}")
        print(f"Saved merged video to: {self.output_path}")
