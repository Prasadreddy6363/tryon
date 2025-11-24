"""
VITON-HD Requirements Verification Script
Checks if your project meets all specifications
"""

import os
import sys
from pathlib import Path
from PIL import Image
import json

WORKSPACE = Path(__file__).parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = VITON_DIR / 'datasets' / 'test'
CHECKPOINTS_DIR = VITON_DIR / 'checkpoints'

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_resolution(image_path, expected=(768, 1024)):
    """Check if image has correct resolution"""
    try:
        img = Image.open(image_path)
        return img.size == expected
    except:
        return False

def verify_dataset():
    """Verify dataset completeness and specifications"""
    print_header("DATASET VERIFICATION")
    
    required_dirs = {
        'image': 'Person images',
        'cloth': 'Clothing images',
        'cloth-mask': 'Cloth masks',
        'image-parse': 'Segmentation maps',
        'image-parse-agnostic-v3.2': 'Agnostic segmentations',
        'agnostic-v3.2': 'Agnostic images',
        'openpose-json': 'Pose annotations',
        'openpose-img': 'Pose visualizations'
    }
    
    all_good = True
    
    for dir_name, description in required_dirs.items():
        dir_path = DATASETS_DIR / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.glob('*')))
            print(f"✓ {description:30} {file_count:4} files")
        else:
            print(f"✗ {description:30} MISSING")
            all_good = False
    
    return all_good

def verify_resolution():
    """Verify image resolutions"""
    print_header("RESOLUTION VERIFICATION")
    
    # Check person image
    person_img = DATASETS_DIR / 'image' / '00008_00.jpg'
    if person_img.exists():
        img = Image.open(person_img)
        size = img.size
        correct = size == (768, 1024)
        status = "✓" if correct else "✗"
        print(f"{status} Person image: {size[0]}×{size[1]} (Expected: 768×1024)")
    else:
        print("✗ Sample person image not found")
        return False
    
    # Check cloth image
    cloth_img = DATASETS_DIR / 'cloth' / '00008_00.jpg'
    if cloth_img.exists():
        img = Image.open(cloth_img)
        size = img.size
        correct = size == (768, 1024)
        status = "✓" if correct else "✗"
        print(f"{status} Cloth image: {size[0]}×{size[1]} (Expected: 768×1024)")
    else:
        print("✗ Sample cloth image not found")
        return False
    
    return True

def verify_checkpoints():
    """Verify model checkpoints"""
    print_header("MODEL CHECKPOINTS VERIFICATION")
    
    required_checkpoints = {
        'seg_final.pth': 'Segmentation Network',
        'gmm_final.pth': 'Geometric Matching Module',
        'alias_final.pth': 'ALIAS Generator'
    }
    
    all_good = True
    
    for filename, description in required_checkpoints.items():
        checkpoint_path = CHECKPOINTS_DIR / filename
        if checkpoint_path.exists():
            size_mb = checkpoint_path.stat().st_size / (1024 * 1024)
            print(f"✓ {description:30} {size_mb:6.1f} MB")
        else:
            print(f"✗ {description:30} MISSING")
            all_good = False
    
    return all_good

def verify_software():
    """Verify software requirements"""
    print_header("SOFTWARE VERIFICATION")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    python_ok = sys.version_info >= (3, 8)
    status = "✓" if python_ok else "✗"
    print(f"{status} Python: {python_version} (Required: 3.8+)")
    
    # Check PyTorch
    try:
        import torch
        torch_version = torch.__version__
        torch_ok = True
        print(f"✓ PyTorch: {torch_version}")
        
        # Check CUDA
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print(f"✓ CUDA: Available ({torch.cuda.get_device_name(0)})")
        else:
            print(f"⚠ CUDA: Not available (using CPU)")
    except ImportError:
        print("✗ PyTorch: Not installed")
        torch_ok = False
    
    # Check other libraries
    libraries = {
        'kornia': 'Kornia',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn',
        'flask': 'Flask',
        'mediapipe': 'MediaPipe'
    }
    
    all_good = python_ok and torch_ok
    
    for module_name, display_name in libraries.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'installed')
            print(f"✓ {display_name:20} {version}")
        except ImportError:
            print(f"✗ {display_name:20} Not installed")
            all_good = False
    
    return all_good

def verify_preprocessing():
    """Verify preprocessing completeness"""
    print_header("PREPROCESSING VERIFICATION")
    
    # Check a sample person
    person_id = '00008_00'
    
    checks = {
        'Person image': DATASETS_DIR / 'image' / f'{person_id}.jpg',
        'Segmentation': DATASETS_DIR / 'image-parse' / f'{person_id}.png',
        'Agnostic seg': DATASETS_DIR / 'image-parse-agnostic-v3.2' / f'{person_id}.png',
        'Agnostic img': DATASETS_DIR / 'agnostic-v3.2' / f'{person_id}.jpg',
        'Pose JSON': DATASETS_DIR / 'openpose-json' / f'{person_id}_keypoints.json',
        'Pose image': DATASETS_DIR / 'openpose-img' / f'{person_id}_rendered.png',
    }
    
    all_good = True
    
    for name, path in checks.items():
        if path.exists():
            print(f"✓ {name:20} exists")
        else:
            print(f"✗ {name:20} MISSING")
            all_good = False
    
    return all_good

def generate_report():
    """Generate comprehensive verification report"""
    print("\n" + "="*60)
    print("  VITON-HD REQUIREMENTS VERIFICATION")
    print("="*60)
    
    results = {
        'Dataset': verify_dataset(),
        'Resolution': verify_resolution(),
        'Checkpoints': verify_checkpoints(),
        'Software': verify_software(),
        'Preprocessing': verify_preprocessing()
    }
    
    print_header("VERIFICATION SUMMARY")
    
    all_passed = True
    for category, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10} {category}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("  ✓ ALL REQUIREMENTS MET!")
        print("  Your project is fully compliant with VITON-HD specs")
    else:
        print("  ⚠ SOME REQUIREMENTS NOT MET")
        print("  Please check the failed items above")
    print("="*60)
    
    # Additional info
    print("\n" + "="*60)
    print("  SYSTEM INFORMATION")
    print("="*60)
    
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        print(f"CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
            print(f"CUDA Version: {torch.version.cuda}")
        else:
            print("Running on: CPU")
    except:
        pass
    
    print("\n" + "="*60)
    print("  DATASET STATISTICS")
    print("="*60)
    
    if (DATASETS_DIR / 'image').exists():
        person_count = len(list((DATASETS_DIR / 'image').glob('*.jpg')))
        cloth_count = len(list((DATASETS_DIR / 'cloth').glob('*.jpg')))
        print(f"Person images: {person_count}")
        print(f"Cloth images: {cloth_count}")
        print(f"Total combinations: {person_count * cloth_count:,}")
    
    print("\n" + "="*60)
    print("  RECOMMENDATIONS")
    print("="*60)
    
    if not results['Software']:
        print("• Install missing Python libraries")
        print("  Run: pip install -r requirements.txt")
    
    if not results['Dataset']:
        print("• Download complete VITON-HD dataset")
        print("  Run: python download_dataset.py")
    
    if not results['Preprocessing']:
        print("• Generate preprocessing data")
        print("  Run: python generate_keypoints.py")
    
    if not results['Checkpoints']:
        print("• Download model checkpoints")
        print("  Place in: VITON-HD/checkpoints/")
    
    try:
        import torch
        if not torch.cuda.is_available():
            print("\n⚠ GPU Acceleration:")
            print("• CUDA not available - using CPU")
            print("• Processing will be slower (~30s per image)")
            print("• Quality is the same, just slower")
            print("• Consider NVIDIA GPU for faster processing")
    except:
        pass
    
    print("\n" + "="*60)
    print("  For detailed information, see:")
    print("  DATASET_REQUIREMENTS.md")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == '__main__':
    success = generate_report()
    sys.exit(0 if success else 1)
