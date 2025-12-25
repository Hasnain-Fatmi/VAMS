
from processing import VideoProcessor


def main():
    
    print("=" * 60)
    print("Fight Detection System")
    print("=" * 60)
    
    # Create and run video processor
    processor = VideoProcessor()
    
    try:
        stats = processor.process()
        
        # Display final statistics
        print("\n" + "=" * 60)
        print("Processing Complete!")
        print("=" * 60)
        print(f"Total frames processed: {stats['total_frames']}")
        print(f"Frames with confirmed fights: {stats['fight_frames']}")
        
        if stats['total_frames'] > 0:
            fight_percentage = (stats['fight_frames'] / stats['total_frames']) * 100
            print(f"Fight percentage: {fight_percentage:.2f}%")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Processing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during processing: {e}")
        raise


if __name__ == "__main__":
    main()
