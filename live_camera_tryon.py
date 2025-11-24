"""
Live Camera Virtual Try-On
Capture stable image from camera and apply virtual try-on with selected clothing
"""

import cv2
import numpy as np
import time
import os
import sys
import subprocess
from pathlib import Path
from PIL import Image

WORKSPACE = Path(__file__).parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = VITON_DIR / 'datasets'
TEST_DIR = DATASETS_DIR / 'test'
IMG_DIR = TEST_DIR / 'image'
CLOTH_DIR = TEST_DIR / 'cloth'
RESULTS_DIR = VITON_DIR / 'results'
CHECKPOINTS_DIR = VITON_DIR / 'checkpoints'
CAPTURE_DIR = WORKSPACE / 'camera_captures'

# Create capture directory
CAPTURE_DIR.mkdir(exist_ok=True)

class StableFrameCapture:
    """Capture stable frame from camera using motion detection"""
    
    def __init__(self, stability_threshold=0.02, stable_frames_required=10):
        self.stability_threshold = stability_threshold
        self.stable_frames_required = stable_frames_required
        self.prev_frame = None
        self.stable_count = 0
        
    def is_stable(self, frame):
        """Check if frame is stable (person not moving)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.prev_frame is None:
            self.prev_frame = gray
            return False
        
        # Calculate frame difference
        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        # Calculate motion percentage
        motion_pixels = np.sum(thresh == 255)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        motion_percentage = motion_pixels / total_pixels
        
        self.prev_frame = gray
        
        # Check if stable
        if motion_percentage < self.stability_threshold:
            self.stable_count += 1
        else:
            self.stable_count = 0
        
        return self.stable_count >= self.stable_frames_required
    
    def reset(self):
        """Reset stability counter"""
        self.stable_count = 0
        self.prev_frame = None

def list_available_clothes():
    """List available clothing items"""
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.endswith('.jpg')])
    return clothes

def select_clothing():
    """Let user select clothing item"""
    clothes = list_available_clothes()
    
    print("\n" + "="*60)
    print("AVAILABLE CLOTHING ITEMS")
    print("="*60)
    
    # Show first 20 items
    for i, cloth in enumerate(clothes[:20], 1):
        print(f"{i}. {cloth}")
    
    if len(clothes) > 20:
        print(f"... and {len(clothes) - 20} more")
    
    print("\nRecommended items:")
    recommended = [
        '00008_00.jpg',
        '00013_00.jpg',
        '00034_00.jpg',
        '00055_00.jpg',
        '00067_00.jpg'
    ]
    
    for i, cloth in enumerate(recommended, 1):
        if cloth in clothes:
            print(f"  {i}. {cloth}")
    
    print("\n" + "-"*60)
    choice = input("Enter clothing filename (or number 1-5 for recommended): ").strip()
    
    # Check if number
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(recommended) and recommended[idx] in clothes:
            return recommended[idx]
    
    # Check if filename
    if choice in clothes:
        return choice
    
    # Default to first recommended
    print(f"Using default: {recommended[0]}")
    return recommended[0]

def preprocess_captured_image(image_path, output_path):
    """Preprocess captured image for VITON-HD"""
    print("\n" + "="*60)
    print("PREPROCESSING CAPTURED IMAGE")
    print("="*60)
    
    # Load and resize image
    img = Image.open(image_path)
    
    # Resize to VITON-HD standard size (768x1024)
    target_size = (768, 1024)
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # Save preprocessed image
    img_resized.save(output_path, 'JPEG', quality=95)
    print(f"✓ Image resized to {target_size[0]}x{target_size[1]}")
    
    # Generate pose keypoints
    print("\n⚠ Note: For best results, captured image needs:")
    print("  • OpenPose keypoints")
    print("  • Segmentation mask")
    print("  • Agnostic representation")
    print("\nRun: python generate_keypoints.py to generate these")
    print("For now, using simplified processing...")
    
    return output_path

def run_virtual_tryon(person_image, cloth_name):
    """Run virtual try-on on captured image"""
    print("\n" + "="*60)
    print("RUNNING VIRTUAL TRY-ON")
    print("="*60)
    
    job_name = f"camera_{int(time.time())}"
    
    # Create pairs file
    pairs_path = DATASETS_DIR / 'test_pairs.txt'
    with open(pairs_path, 'w', encoding='utf-8') as f:
        f.write(f"{person_image} {cloth_name}\n")
    
    # Ensure result directory exists
    result_dir = RESULTS_DIR / job_name
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # Run test.py
    cmd = [
        sys.executable,
        str(VITON_DIR / 'test.py'),
        '--name', job_name,
        '--dataset_dir', str(DATASETS_DIR),
        '--checkpoint_dir', str(CHECKPOINTS_DIR),
        '--save_dir', str(RESULTS_DIR)
    ]
    
    print("Processing virtual try-on...")
    print("This will take ~30 seconds...")
    
    start_time = time.time()
    proc = subprocess.run(cmd, cwd=str(VITON_DIR), capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    if proc.returncode != 0:
        print(f"❌ Try-on failed")
        print(f"Error: {proc.stderr}")
        return None
    
    # Find result
    results = list(result_dir.glob('*.jpg'))
    if results:
        result_file = results[0]
        print(f"✅ SUCCESS (took {elapsed:.1f}s)")
        print(f"Result saved: {result_file}")
        return result_file
    else:
        print("❌ No result generated")
        return None

def capture_and_tryon():
    """Main function: capture stable frame and apply virtual try-on"""
    print("\n" + "="*60)
    print("LIVE CAMERA VIRTUAL TRY-ON")
    print("="*60)
    print("\nThis will:")
    print("1. Open your camera")
    print("2. Detect when you're standing still")
    print("3. Capture a stable image")
    print("4. Apply virtual try-on with selected clothing")
    print("\n" + "="*60)
    
    # Select clothing first
    cloth_name = select_clothing()
    print(f"\n✓ Selected clothing: {cloth_name}")
    
    # Initialize camera
    print("\nInitializing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("✓ Camera opened successfully")
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("• Stand in front of camera")
    print("• Face the camera directly")
    print("• Keep arms slightly away from body")
    print("• Stand still for stable capture")
    print("• Press 'c' to force capture")
    print("• Press 'q' to quit")
    print("="*60)
    
    stable_capture = StableFrameCapture(stability_threshold=0.02, stable_frames_required=15)
    countdown = 0
    captured = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        # Create display frame
        display_frame = frame.copy()
        
        # Check stability
        is_stable = stable_capture.is_stable(frame)
        
        # Draw status
        if is_stable:
            countdown += 1
            status_text = f"STABLE - Capturing in {3 - countdown//10}..."
            color = (0, 255, 0)  # Green
            
            if countdown >= 30:  # 1 second at 30fps
                # Capture frame
                timestamp = int(time.time())
                capture_path = CAPTURE_DIR / f"capture_{timestamp}.jpg"
                cv2.imwrite(str(capture_path), frame)
                print(f"\n✓ Stable frame captured: {capture_path}")
                captured = True
                break
        else:
            countdown = 0
            status_text = "Move less - waiting for stability..."
            color = (0, 0, 255)  # Red
        
        # Draw overlay
        cv2.putText(display_frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(display_frame, f"Clothing: {cloth_name}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(display_frame, "Press 'c' to capture | 'q' to quit", (10, display_frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw stability indicator
        stability_bar_width = int(stable_capture.stable_count / stable_capture.stable_frames_required * 200)
        cv2.rectangle(display_frame, (10, 80), (210, 100), (50, 50, 50), -1)
        cv2.rectangle(display_frame, (10, 80), (10 + stability_bar_width, 100), color, -1)
        
        # Show frame
        cv2.imshow('Live Camera Virtual Try-On', display_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n❌ Cancelled by user")
            break
        elif key == ord('c'):
            # Force capture
            timestamp = int(time.time())
            capture_path = CAPTURE_DIR / f"capture_{timestamp}.jpg"
            cv2.imwrite(str(capture_path), frame)
            print(f"\n✓ Frame captured manually: {capture_path}")
            captured = True
            break
    
    # Release camera
    cap.release()
    cv2.destroyAllWindows()
    
    if not captured:
        print("\n❌ No frame captured")
        return
    
    # Preprocess captured image
    person_filename = f"camera_{int(time.time())}.jpg"
    person_path = IMG_DIR / person_filename
    
    # Copy to dataset directory
    preprocessed = preprocess_captured_image(capture_path, person_path)
    
    print("\n⚠ IMPORTANT:")
    print("The captured image needs preprocessing for best results.")
    print("Current limitation: Using simplified processing.")
    print("\nFor production use, you should:")
    print("1. Generate OpenPose keypoints")
    print("2. Create segmentation masks")
    print("3. Generate agnostic representation")
    print("\nProceeding with available data...")
    
    # Ask if user wants to continue
    response = input("\nContinue with try-on? (y/n): ").strip().lower()
    if response != 'y':
        print("❌ Try-on cancelled")
        return
    
    # Run virtual try-on
    result = run_virtual_tryon(person_filename, cloth_name)
    
    if result:
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print(f"✓ Original capture: {capture_path}")
        print(f"✓ Try-on result: {result}")
        print(f"\nView result at: http://127.0.0.1:5000")
        
        # Display result
        try:
            result_img = cv2.imread(str(result))
            if result_img is not None:
                cv2.imshow('Virtual Try-On Result', result_img)
                print("\nPress any key to close...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        except Exception as e:
            print(f"Could not display result: {e}")

def main():
    """Main entry point"""
    try:
        capture_and_tryon()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
