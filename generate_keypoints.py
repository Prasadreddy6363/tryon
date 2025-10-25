#!/usr/bin/env python3
"""
Generate OpenPose-format keypoints for VITON-HD using MediaPipe.
This script processes person images and creates compatible JSON keypoint files.
"""

import cv2
import json
import os
from pathlib import Path
import mediapipe as mp
import numpy as np

def setup_mediapipe():
    """Initialize MediaPipe Pose detector."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=False,
        min_detection_confidence=0.5
    )
    return pose, mp_pose

def mediapipe_to_openpose(landmarks, image_width, image_height):
    """
    Convert MediaPipe landmarks (33 points) to OpenPose format (25 points).
    
    MediaPipe → OpenPose mapping:
    0 (Nose) → 0 (Nose)
    11 (L.Shoulder) → 5 (L.Shoulder)
    12 (R.Shoulder) → 2 (R.Shoulder)
    13 (L.Elbow) → 6 (L.Elbow)
    14 (R.Elbow) → 3 (R.Elbow)
    15 (L.Wrist) → 7 (L.Wrist)
    16 (R.Wrist) → 4 (R.Wrist)
    23 (L.Hip) → 12 (L.Hip)
    24 (R.Hip) → 9 (R.Hip)
    25 (L.Knee) → 13 (L.Knee)
    26 (R.Knee) → 10 (R.Knee)
    27 (L.Ankle) → 14 (L.Ankle)
    28 (R.Ankle) → 11 (R.Ankle)
    """
    
    # OpenPose format: 25 keypoints × 3 values (x, y, confidence)
    openpose_keypoints = [0.0] * 75  # 25 × 3
    
    # Mapping from MediaPipe indices to OpenPose indices
    mapping = {
        0: 0,    # Nose
        # 1 is Neck (calculated as midpoint of shoulders)
        12: 2,   # R.Shoulder
        14: 3,   # R.Elbow
        16: 4,   # R.Wrist
        11: 5,   # L.Shoulder
        13: 6,   # L.Elbow
        15: 7,   # L.Wrist
        # 8 is MidHip (calculated as midpoint)
        24: 9,   # R.Hip
        26: 10,  # R.Knee
        28: 11,  # R.Ankle
        23: 12,  # L.Hip
        25: 13,  # L.Knee
        27: 14,  # L.Ankle
    }
    
    # Convert MediaPipe landmarks
    for mp_idx, op_idx in mapping.items():
        if mp_idx < len(landmarks):
            landmark = landmarks[mp_idx]
            x = landmark.x * image_width
            y = landmark.y * image_height
            confidence = landmark.visibility
            
            openpose_keypoints[op_idx * 3] = x
            openpose_keypoints[op_idx * 3 + 1] = y
            openpose_keypoints[op_idx * 3 + 2] = confidence
    
    # Calculate Neck (OpenPose index 1) as midpoint of shoulders
    if landmarks[11].visibility > 0.5 and landmarks[12].visibility > 0.5:
        neck_x = (landmarks[11].x + landmarks[12].x) / 2 * image_width
        neck_y = (landmarks[11].y + landmarks[12].y) / 2 * image_height
        neck_conf = (landmarks[11].visibility + landmarks[12].visibility) / 2
        
        openpose_keypoints[1 * 3] = neck_x
        openpose_keypoints[1 * 3 + 1] = neck_y
        openpose_keypoints[1 * 3 + 2] = neck_conf
    
    # Calculate MidHip (OpenPose index 8) as midpoint of hips
    if landmarks[23].visibility > 0.5 and landmarks[24].visibility > 0.5:
        midhip_x = (landmarks[23].x + landmarks[24].x) / 2 * image_width
        midhip_y = (landmarks[23].y + landmarks[24].y) / 2 * image_height
        midhip_conf = (landmarks[23].visibility + landmarks[24].visibility) / 2
        
        openpose_keypoints[8 * 3] = midhip_x
        openpose_keypoints[8 * 3 + 1] = midhip_y
        openpose_keypoints[8 * 3 + 2] = midhip_conf
    
    return openpose_keypoints

def generate_keypoints_for_image(image_path, pose, mp_pose):
    """Process a single image and return OpenPose-format keypoints."""
    # Read image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]
    
    # Process image
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        print(f"Warning: No pose detected in {image_path}")
        return None
    
    # Convert to OpenPose format
    openpose_keypoints = mediapipe_to_openpose(
        results.pose_landmarks.landmark,
        width,
        height
    )
    
    # Create OpenPose JSON structure
    openpose_data = {
        "version": 1.3,
        "people": [
            {
                "person_id": [-1],
                "pose_keypoints_2d": openpose_keypoints,
                "face_keypoints_2d": [],
                "hand_left_keypoints_2d": [],
                "hand_right_keypoints_2d": [],
                "pose_keypoints_3d": [],
                "face_keypoints_3d": [],
                "hand_left_keypoints_3d": [],
                "hand_right_keypoints_3d": []
            }
        ]
    }
    
    return openpose_data

def generate_rendered_image(image_path, openpose_data, output_path):
    """Create a visualization of the keypoints (like OpenPose rendered images)."""
    image = cv2.imread(str(image_path))
    if image is None:
        return
    
    if not openpose_data or not openpose_data['people']:
        return
    
    keypoints = openpose_data['people'][0]['pose_keypoints_2d']
    
    # Draw keypoints
    for i in range(0, len(keypoints), 3):
        x, y, conf = keypoints[i], keypoints[i+1], keypoints[i+2]
        if conf > 0.5:
            cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    
    # Draw connections (OpenPose skeleton)
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),  # Head to R.Arm
        (1, 5), (5, 6), (6, 7),           # L.Arm
        (1, 8), (8, 9), (9, 10), (10, 11), # R.Leg
        (8, 12), (12, 13), (13, 14)       # L.Leg
    ]
    
    for start_idx, end_idx in connections:
        start_x, start_y, start_conf = keypoints[start_idx*3:start_idx*3+3]
        end_x, end_y, end_conf = keypoints[end_idx*3:end_idx*3+3]
        
        if start_conf > 0.5 and end_conf > 0.5:
            cv2.line(image, (int(start_x), int(start_y)), 
                    (int(end_x), int(end_y)), (0, 255, 0), 2)
    
    cv2.imwrite(str(output_path), image)

def process_directory(input_dir, output_json_dir, output_img_dir):
    """Process all images in a directory and generate keypoint files."""
    input_path = Path(input_dir)
    output_json_path = Path(output_json_dir)
    output_img_path = Path(output_img_dir)
    
    # Create output directories
    output_json_path.mkdir(parents=True, exist_ok=True)
    output_img_path.mkdir(parents=True, exist_ok=True)
    
    # Setup MediaPipe
    print("Initializing MediaPipe Pose detector...")
    pose, mp_pose = setup_mediapipe()
    
    # Get all image files
    image_files = list(input_path.glob('*.jpg')) + list(input_path.glob('*.png'))
    
    if not image_files:
        print(f"No images found in {input_dir}")
        return
    
    print(f"Found {len(image_files)} images to process...")
    
    success_count = 0
    failed_count = 0
    
    for idx, image_file in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] Processing {image_file.name}...", end=' ')
        
        # Generate keypoints
        openpose_data = generate_keypoints_for_image(image_file, pose, mp_pose)
        
        if openpose_data:
            # Save JSON file
            json_filename = image_file.stem + '_keypoints.json'
            json_output = output_json_path / json_filename
            with open(json_output, 'w') as f:
                json.dump(openpose_data, f, indent=2)
            
            # Generate rendered visualization
            img_filename = image_file.stem + '_rendered.png'
            img_output = output_img_path / img_filename
            generate_rendered_image(image_file, openpose_data, img_output)
            
            print("✓ Success")
            success_count += 1
        else:
            print("✗ Failed")
            failed_count += 1
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"✓ Success: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"{'='*50}")
    print(f"\nOutput saved to:")
    print(f"  JSON: {output_json_path}")
    print(f"  Images: {output_img_path}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate OpenPose keypoints for VITON-HD')
    parser.add_argument('--input', '-i', required=True, help='Input directory with person images')
    parser.add_argument('--output-json', '-j', default='output/openpose-json', 
                       help='Output directory for JSON keypoints')
    parser.add_argument('--output-img', '-r', default='output/openpose-img',
                       help='Output directory for rendered images')
    
    args = parser.parse_args()
    
    process_directory(args.input, args.output_json, args.output_img)

if __name__ == '__main__':
    # Example usage if run without arguments
    import sys
    
    if len(sys.argv) == 1:
        print("=" * 60)
        print("VITON-HD Keypoint Generator")
        print("=" * 60)
        print("\nUsage:")
        print("  python generate_keypoints.py -i <input_dir> [-j <json_dir>] [-r <render_dir>]")
        print("\nExample:")
        print("  python generate_keypoints.py -i VITON-HD/datasets/test/image")
        print("\nThis will create:")
        print("  - output/openpose-json/*.json  (keypoint data)")
        print("  - output/openpose-img/*.png    (visualization)")
        print("\nOr edit this script to set default paths and run directly!")
        print("=" * 60)
        
        # Auto-process if default paths exist
        default_input = 'VITON-HD/datasets/test/image'
        if Path(default_input).exists():
            print(f"\nFound default input directory: {default_input}")
            response = input("Process with default settings? (y/n): ")
            if response.lower() == 'y':
                process_directory(
                    default_input,
                    'VITON-HD/datasets/test/openpose-json',
                    'VITON-HD/datasets/test/openpose-img'
                )
        sys.exit(0)
    
    main()
