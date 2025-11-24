"""
VITON-HD Accuracy Improvement Script
This script helps diagnose and improve virtual try-on accuracy
"""

import os
import json
from pathlib import Path
import torch

def check_system():
    """Check system capabilities"""
    print("=" * 60)
    print("SYSTEM DIAGNOSTICS")
    print("=" * 60)
    
    # Check CUDA
    cuda_available = torch.cuda.is_available()
    print(f"✓ CUDA Available: {cuda_available}")
    if cuda_available:
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA Version: {torch.version.cuda}")
    else:
        print("  ⚠ Running on CPU - Results may be slower and less accurate")
        print("  💡 Consider using a GPU for better quality")
    
    print(f"✓ PyTorch Version: {torch.__version__}")
    print()

def check_preprocessing(dataset_dir):
    """Check if all preprocessing files exist"""
    print("=" * 60)
    print("PREPROCESSING DATA CHECK")
    print("=" * 60)
    
    test_dir = Path(dataset_dir) / 'test'
    
    required_dirs = [
        'image',
        'cloth',
        'cloth-mask',
        'image-parse',
        'image-parse-agnostic-v3.2',
        'agnostic-v3.2',
        'openpose-json',
        'openpose-img'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = test_dir / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.glob('*')))
            print(f"✓ {dir_name}: {file_count} files")
        else:
            print(f"✗ {dir_name}: MISSING")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\n⚠ Missing directories: {', '.join(missing_dirs)}")
        print("💡 Run preprocessing scripts to generate missing data")
    else:
        print("\n✓ All preprocessing directories present")
    
    print()
    return len(missing_dirs) == 0

def check_person_preprocessing(dataset_dir, person_file):
    """Check if a specific person has all required preprocessing"""
    print("=" * 60)
    print(f"CHECKING PERSON: {person_file}")
    print("=" * 60)
    
    test_dir = Path(dataset_dir) / 'test'
    person_id = person_file.replace('.jpg', '')
    
    checks = {
        'Original Image': test_dir / 'image' / person_file,
        'Segmentation': test_dir / 'image-parse' / person_file,
        'Agnostic Segmentation': test_dir / 'image-parse-agnostic-v3.2' / person_file,
        'Agnostic Image': test_dir / 'agnostic-v3.2' / person_file,
        'OpenPose JSON': test_dir / 'openpose-json' / f'{person_id}_keypoints.json',
        'OpenPose Image': test_dir / 'openpose-img' / person_file,
    }
    
    all_present = True
    for name, path in checks.items():
        if path.exists():
            print(f"✓ {name}")
        else:
            print(f"✗ {name}: MISSING")
            all_present = False
    
    if not all_present:
        print(f"\n⚠ Person {person_file} is missing preprocessing data")
        print("💡 This will result in poor or failed try-on results")
        print("💡 Run: python generate_keypoints.py to generate missing data")
    else:
        print(f"\n✓ Person {person_file} has complete preprocessing")
    
    print()
    return all_present

def check_cloth_preprocessing(dataset_dir, cloth_file):
    """Check if a specific cloth has all required preprocessing"""
    print("=" * 60)
    print(f"CHECKING CLOTH: {cloth_file}")
    print("=" * 60)
    
    test_dir = Path(dataset_dir) / 'test'
    
    checks = {
        'Cloth Image': test_dir / 'cloth' / cloth_file,
        'Cloth Mask': test_dir / 'cloth-mask' / cloth_file,
    }
    
    all_present = True
    for name, path in checks.items():
        if path.exists():
            print(f"✓ {name}")
        else:
            print(f"✗ {name}: MISSING")
            all_present = False
    
    if not all_present:
        print(f"\n⚠ Cloth {cloth_file} is missing preprocessing data")
        print("💡 Add cloth mask using the 2D Clothing Addition tool")
    else:
        print(f"\n✓ Cloth {cloth_file} has complete preprocessing")
    
    print()
    return all_present

def recommendations():
    """Print recommendations for improving accuracy"""
    print("=" * 60)
    print("RECOMMENDATIONS FOR BETTER ACCURACY")
    print("=" * 60)
    
    print("\n1. HARDWARE:")
    print("   • Use a CUDA-capable GPU for best results")
    print("   • Minimum 8GB RAM recommended")
    print("   • SSD storage for faster data loading")
    
    print("\n2. PREPROCESSING:")
    print("   • Ensure all person images have OpenPose keypoints")
    print("   • Run: python generate_keypoints.py")
    print("   • Verify segmentation masks exist")
    
    print("\n3. IMAGE QUALITY:")
    print("   • Use high-resolution images (1024x768 recommended)")
    print("   • Person should be front-facing with clear pose")
    print("   • Good lighting and minimal background clutter")
    print("   • Clothing items should have clean backgrounds")
    
    print("\n4. MODEL CHECKPOINTS:")
    print("   • Verify all 3 checkpoint files are present:")
    print("     - seg_final.pth (Segmentation)")
    print("     - gmm_final.pth (Geometric Matching)")
    print("     - alias_final.pth (ALIAS Generator)")
    
    print("\n5. DATASET STRUCTURE:")
    print("   • Follow VITON-HD dataset structure exactly")
    print("   • All preprocessing folders must be present")
    print("   • File naming must match across folders")
    
    print("\n6. COMMON ISSUES:")
    print("   • Misaligned clothing → Check pose keypoints")
    print("   • Blurry results → Verify image resolution")
    print("   • Wrong body parts → Check segmentation masks")
    print("   • Artifacts → Ensure clean cloth masks")
    
    print()

def main():
    """Main diagnostic function"""
    workspace = Path(__file__).parent
    dataset_dir = workspace / 'VITON-HD' / 'datasets'
    
    print("\n" + "=" * 60)
    print("VITON-HD ACCURACY DIAGNOSTIC TOOL")
    print("=" * 60 + "\n")
    
    # System check
    check_system()
    
    # Preprocessing check
    preprocessing_ok = check_preprocessing(dataset_dir)
    
    # Check a sample person and cloth
    test_dir = dataset_dir / 'test'
    people = sorted([f for f in os.listdir(test_dir / 'image') if f.endswith('.jpg')])
    clothes = sorted([f for f in os.listdir(test_dir / 'cloth') if f.endswith('.jpg')])
    
    if people:
        check_person_preprocessing(dataset_dir, people[0])
    
    if clothes:
        check_cloth_preprocessing(dataset_dir, clothes[0])
    
    # Recommendations
    recommendations()
    
    print("=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print("\nFor specific person/cloth checks, run:")
    print("  python improve_accuracy.py --person <filename>")
    print("  python improve_accuracy.py --cloth <filename>")
    print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 2:
        workspace = Path(__file__).parent
        dataset_dir = workspace / 'VITON-HD' / 'datasets'
        
        if sys.argv[1] == '--person':
            check_person_preprocessing(dataset_dir, sys.argv[2])
        elif sys.argv[1] == '--cloth':
            check_cloth_preprocessing(dataset_dir, sys.argv[2])
    else:
        main()
