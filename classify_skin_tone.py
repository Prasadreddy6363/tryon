"""
Skin Tone Classification for VITON-HD Person Images

Classifies person images based on skin tone using computer vision algorithms:
- Face detection using OpenCV Haar Cascades
- Skin tone extraction from face region
- Classification into standard skin tone categories
- Organizes images by skin tone for better dataset management

Technologies used:
- OpenCV: Face detection, color space conversion
- NumPy: Numerical computations
- Pillow: Image loading
- ITA° (Individual Typology Angle): Standard dermatological classification
"""

import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path
import json
import shutil
from collections import defaultdict

# Paths
WORKSPACE = Path(__file__).resolve().parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = VITON_DIR / 'datasets'
TEST_DIR = DATASETS_DIR / 'test'
IMG_DIR = TEST_DIR / 'image'

# Output directory for classification results
OUTPUT_DIR = WORKSPACE / 'skin_tone_classification'
OUTPUT_DIR.mkdir(exist_ok=True)

# Skin tone categories based on ITA° (Individual Typology Angle)
# This is a standard dermatological classification system
SKIN_TONE_CATEGORIES = {
    'very_light': {'min': 55, 'max': 90, 'name': 'Very Light', 'description': 'Very fair skin'},
    'light': {'min': 41, 'max': 55, 'name': 'Light', 'description': 'Fair skin'},
    'intermediate': {'min': 28, 'max': 41, 'name': 'Intermediate', 'description': 'Light brown skin'},
    'tan': {'min': 10, 'max': 28, 'name': 'Tan', 'description': 'Medium brown skin'},
    'brown': {'min': -30, 'max': 10, 'name': 'Brown', 'description': 'Dark brown skin'},
    'dark': {'min': -90, 'max': -30, 'name': 'Dark', 'description': 'Very dark skin'}
}

def calculate_ita_angle(L, b):
    """
    Calculate ITA° (Individual Typology Angle) for skin tone classification.
    
    ITA° = [arctan((L* - 50)/b*)] × (180/π)
    
    Where:
    - L* = Lightness in Lab color space (0-100)
    - b* = Blue-Yellow axis in Lab color space
    
    Reference: "Colorimetric Analysis and Quantification of Human Skin Pigmentation"
    (Chardon et al., 1991)
    
    Args:
        L: Lightness value (0-100)
        b: Blue-yellow value
    
    Returns:
        ITA angle in degrees
    """
    if b == 0:
        b = 0.001  # Avoid division by zero
    
    angle_rad = np.arctan((L - 50) / b)
    angle_deg = angle_rad * (180 / np.pi)
    
    return angle_deg

def classify_skin_tone(ita_angle):
    """
    Classify skin tone based on ITA° angle.
    
    Args:
        ita_angle: ITA° value in degrees
    
    Returns:
        Category key (e.g., 'light', 'tan', etc.)
    """
    for category, bounds in SKIN_TONE_CATEGORIES.items():
        if bounds['min'] <= ita_angle < bounds['max']:
            return category
    
    # Fallback for edge cases
    if ita_angle >= 55:
        return 'very_light'
    else:
        return 'dark'

def detect_face_region(image_path):
    """
    Detect face region in image using Haar Cascade.
    
    Algorithm:
    1. Load image and convert to grayscale
    2. Apply Haar Cascade face detection
    3. Return largest detected face region
    
    Args:
        image_path: Path to image file
    
    Returns:
        Face region as numpy array (BGR) or None if no face detected
    """
    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Failed to load image: {image_path}")
        return None
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load Haar Cascade classifier (built-in with OpenCV)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Detect faces
    # Parameters:
    # - scaleFactor: Image pyramid scale (1.1 = 10% reduction per layer)
    # - minNeighbors: Minimum neighbors for valid detection (higher = fewer false positives)
    # - minSize: Minimum face size in pixels
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )
    
    if len(faces) == 0:
        print(f"No face detected in {image_path.name}")
        return None
    
    # Get largest face (most likely the main subject)
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    
    # Extract face region with some padding
    padding = int(0.1 * min(w, h))  # 10% padding
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(img.shape[1], x + w + padding)
    y2 = min(img.shape[0], y + h + padding)
    
    face_region = img[y1:y2, x1:x2]
    
    return face_region

def extract_skin_tone(face_region):
    """
    Extract average skin tone from face region.
    
    Algorithm:
    1. Convert to HSV color space for skin detection
    2. Create skin mask using HSV thresholds
    3. Apply mask to get skin pixels only
    4. Convert to Lab color space
    5. Calculate average L* and b* values
    6. Compute ITA° angle
    
    Args:
        face_region: Face region image (BGR format)
    
    Returns:
        Tuple of (ITA_angle, Lab_L, Lab_b, average_skin_color_BGR)
    """
    if face_region is None or face_region.size == 0:
        return None
    
    # Convert to HSV for skin detection
    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
    
    # Define skin color range in HSV
    # These ranges work well for various skin tones
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create mask for skin pixels
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply morphological operations to clean up mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
    
    # Extract skin pixels
    skin_pixels = cv2.bitwise_and(face_region, face_region, mask=skin_mask)
    
    # Get non-zero pixels (actual skin)
    skin_points = skin_pixels[skin_mask > 0]
    
    if len(skin_points) == 0:
        print("No skin pixels detected")
        return None
    
    # Calculate average skin color
    avg_skin_bgr = np.mean(skin_points, axis=0)
    
    # Convert average color to Lab color space
    avg_color_rgb = cv2.cvtColor(
        np.uint8([[avg_skin_bgr]]), 
        cv2.COLOR_BGR2Lab
    )[0][0]
    
    L = avg_color_rgb[0]  # Lightness (0-100)
    a = avg_color_rgb[1]  # Green-Red axis
    b = avg_color_rgb[2]  # Blue-Yellow axis
    
    # Calculate ITA° angle
    ita_angle = calculate_ita_angle(L, b)
    
    return ita_angle, L, b, avg_skin_bgr

def classify_dataset():
    """
    Classify all person images in dataset by skin tone.
    
    Returns:
        Dictionary mapping categories to lists of filenames
    """
    print("=" * 70)
    print("SKIN TONE CLASSIFICATION - VITON-HD Dataset")
    print("=" * 70)
    print()
    
    if not IMG_DIR.exists():
        print(f"Error: Image directory not found: {IMG_DIR}")
        return {}
    
    # Get all person images
    image_files = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.jpg')])
    
    print(f"Found {len(image_files)} person images")
    print()
    print("Processing images...")
    print("-" * 70)
    
    # Classification results
    classification = defaultdict(list)
    detailed_results = []
    
    # Statistics
    successful = 0
    failed = 0
    
    for idx, filename in enumerate(image_files, 1):
        image_path = IMG_DIR / filename
        
        print(f"[{idx}/{len(image_files)}] Processing: {filename}...", end=" ")
        
        # Detect face
        face_region = detect_face_region(image_path)
        
        if face_region is None:
            print("❌ Failed (no face detected)")
            classification['unknown'].append(filename)
            failed += 1
            continue
        
        # Extract skin tone
        result = extract_skin_tone(face_region)
        
        if result is None:
            print("❌ Failed (no skin detected)")
            classification['unknown'].append(filename)
            failed += 1
            continue
        
        ita_angle, L, b, avg_color = result
        
        # Classify
        category = classify_skin_tone(ita_angle)
        classification[category].append(filename)
        
        # Store detailed results
        detailed_results.append({
            'filename': filename,
            'category': category,
            'category_name': SKIN_TONE_CATEGORIES[category]['name'],
            'ita_angle': float(ita_angle),
            'L': float(L),
            'b': float(b),
            'avg_color_bgr': avg_color.tolist()
        })
        
        print(f"✓ {SKIN_TONE_CATEGORIES[category]['name']} (ITA°={ita_angle:.1f}°)")
        successful += 1
    
    print("-" * 70)
    print()
    print("Classification Summary:")
    print("=" * 70)
    
    # Print statistics by category
    for category in ['very_light', 'light', 'intermediate', 'tan', 'brown', 'dark', 'unknown']:
        count = len(classification[category])
        if count > 0:
            if category == 'unknown':
                print(f"  Unknown/Failed: {count} images")
            else:
                cat_info = SKIN_TONE_CATEGORIES[category]
                print(f"  {cat_info['name']:15} ({cat_info['description']:20}): {count:4} images")
    
    print()
    print(f"Total processed: {len(image_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    # Save detailed results
    results_file = OUTPUT_DIR / 'skin_tone_classification.json'
    with open(results_file, 'w') as f:
        json.dump({
            'total_images': len(image_files),
            'successful': successful,
            'failed': failed,
            'classification': {k: v for k, v in classification.items()},
            'detailed_results': detailed_results
        }, f, indent=2)
    
    print(f"Detailed results saved to: {results_file}")
    
    # Create category directories and copy images
    print()
    print("Organizing images by skin tone...")
    
    for category, files in classification.items():
        if len(files) == 0:
            continue
        
        if category == 'unknown':
            category_dir = OUTPUT_DIR / 'unknown'
        else:
            cat_name = SKIN_TONE_CATEGORIES[category]['name'].replace(' ', '_').lower()
            category_dir = OUTPUT_DIR / cat_name
        
        category_dir.mkdir(exist_ok=True)
        
        # Copy images
        for filename in files:
            src = IMG_DIR / filename
            dst = category_dir / filename
            shutil.copy2(src, dst)
        
        print(f"  ✓ {category_dir.name}: {len(files)} images")
    
    print()
    print(f"Images organized in: {OUTPUT_DIR}")
    print()
    
    return classification

def create_visualization():
    """
    Create a visual summary of skin tone distribution.
    """
    results_file = OUTPUT_DIR / 'skin_tone_classification.json'
    
    if not results_file.exists():
        print("No classification results found. Run classification first.")
        return
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    print("=" * 70)
    print("SKIN TONE DISTRIBUTION")
    print("=" * 70)
    print()
    
    classification = data['classification']
    total = data['successful']
    
    # Create bar chart (text-based)
    max_count = max(len(files) for files in classification.values())
    
    for category in ['very_light', 'light', 'intermediate', 'tan', 'brown', 'dark']:
        if category not in classification:
            continue
        
        count = len(classification[category])
        if count == 0:
            continue
        
        cat_info = SKIN_TONE_CATEGORIES[category]
        percentage = (count / total * 100) if total > 0 else 0
        
        # Create bar
        bar_length = int((count / max_count) * 40)
        bar = '█' * bar_length
        
        print(f"{cat_info['name']:15} │{bar:40} │ {count:3} ({percentage:5.1f}%)")
    
    print()

def generate_report():
    """
    Generate a comprehensive markdown report.
    """
    results_file = OUTPUT_DIR / 'skin_tone_classification.json'
    
    if not results_file.exists():
        print("No classification results found. Run classification first.")
        return
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    report_file = OUTPUT_DIR / 'SKIN_TONE_REPORT.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Skin Tone Classification Report\n\n")
        f.write("## Overview\n\n")
        f.write(f"- **Total Images**: {data['total_images']}\n")
        f.write(f"- **Successfully Classified**: {data['successful']}\n")
        f.write(f"- **Failed**: {data['failed']}\n\n")
        
        f.write("## Classification Method\n\n")
        f.write("**Algorithm**: ITA° (Individual Typology Angle)\n\n")
        f.write("**Formula**: `ITA° = [arctan((L* - 50)/b*)] × (180/π)`\n\n")
        f.write("Where:\n")
        f.write("- `L*` = Lightness in Lab color space (0-100)\n")
        f.write("- `b*` = Blue-Yellow axis in Lab color space\n\n")
        
        f.write("**Reference**: Chardon et al., 1991 - Standard dermatological classification\n\n")
        
        f.write("## Skin Tone Categories\n\n")
        f.write("| Category | ITA° Range | Description | Count | Percentage |\n")
        f.write("|----------|-----------|-------------|-------|------------|\n")
        
        total = data['successful']
        for category in ['very_light', 'light', 'intermediate', 'tan', 'brown', 'dark']:
            if category not in data['classification']:
                continue
            
            count = len(data['classification'][category])
            percentage = (count / total * 100) if total > 0 else 0
            cat_info = SKIN_TONE_CATEGORIES[category]
            
            f.write(f"| {cat_info['name']} | {cat_info['min']}° to {cat_info['max']}° | "
                   f"{cat_info['description']} | {count} | {percentage:.1f}% |\n")
        
        f.write("\n## File Organization\n\n")
        f.write("Images have been organized into directories by skin tone:\n\n")
        
        for category in ['very_light', 'light', 'intermediate', 'tan', 'brown', 'dark', 'unknown']:
            if category not in data['classification']:
                continue
            
            count = len(data['classification'][category])
            if count == 0:
                continue
            
            if category == 'unknown':
                f.write(f"- `unknown/`: {count} images (face/skin not detected)\n")
            else:
                cat_name = SKIN_TONE_CATEGORIES[category]['name'].replace(' ', '_').lower()
                f.write(f"- `{cat_name}/`: {count} images\n")
        
        f.write("\n## Technical Details\n\n")
        f.write("### Face Detection\n")
        f.write("- **Algorithm**: Haar Cascade (OpenCV)\n")
        f.write("- **Classifier**: Frontal Face Default\n")
        f.write("- **Parameters**: scaleFactor=1.1, minNeighbors=5\n\n")
        
        f.write("### Skin Detection\n")
        f.write("- **Color Space**: HSV\n")
        f.write("- **Skin Range**: H[0-20], S[20-255], V[70-255]\n")
        f.write("- **Morphology**: Closing + Opening with 5x5 elliptical kernel\n\n")
        
        f.write("### Color Analysis\n")
        f.write("- **Color Space**: CIE Lab (perceptually uniform)\n")
        f.write("- **Measurement**: Average L* and b* from skin pixels\n")
        f.write("- **Classification**: ITA° angle-based categorization\n\n")
    
    print(f"Report generated: {report_file}")

def main():
    """Main execution function."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SKIN TONE CLASSIFICATION SYSTEM" + " " * 21 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Run classification
    classification = classify_dataset()
    
    if classification:
        # Create visualization
        create_visualization()
        
        # Generate report
        generate_report()
        
        print("=" * 70)
        print("COMPLETE!")
        print("=" * 70)
        print()
        print("Results:")
        print(f"  • Classification data: {OUTPUT_DIR / 'skin_tone_classification.json'}")
        print(f"  • Detailed report: {OUTPUT_DIR / 'SKIN_TONE_REPORT.md'}")
        print(f"  • Organized images: {OUTPUT_DIR / '<category_name>/'}")
        print()

if __name__ == "__main__":
    main()
