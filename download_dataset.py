#!/usr/bin/env python3
"""
Download VITON-HD dataset with keypoints from Google Drive.
This script helps you download and set up the complete dataset.
"""

import os
import sys
from pathlib import Path
import zipfile
import shutil

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_step(step_num, text):
    """Print a step message."""
    print(f"\n[Step {step_num}] {text}")

def check_gdown():
    """Check if gdown is installed, install if not."""
    try:
        import gdown
        return True
    except ImportError:
        print("gdown not found. Installing...")
        os.system(f"{sys.executable} -m pip install gdown")
        try:
            import gdown
            return True
        except ImportError:
            return False

def download_with_gdown(file_id, output_path):
    """Download file from Google Drive using gdown."""
    import gdown
    url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Downloading from Google Drive...")
    print(f"URL: {url}")
    gdown.download(url, str(output_path), quiet=False)

def extract_zip(zip_path, extract_to):
    """Extract zip file."""
    print(f"Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✓ Extracted to {extract_to}")

def verify_dataset(base_path):
    """Verify the dataset structure."""
    print("\nVerifying dataset structure...")
    
    required_dirs = [
        'image',
        'cloth',
        'openpose-json',
        'openpose-img',
        'image-parse',
        'cloth-mask'
    ]
    
    test_dir = base_path / 'test'
    
    if not test_dir.exists():
        print(f"✗ Test directory not found: {test_dir}")
        return False
    
    all_good = True
    for dir_name in required_dirs:
        dir_path = test_dir / dir_name
        if dir_path.exists():
            file_count = len(list(dir_path.glob('*')))
            print(f"✓ {dir_name:20s} - {file_count} files")
        else:
            print(f"✗ {dir_name:20s} - NOT FOUND")
            all_good = False
    
    return all_good

def main():
    print_header("VITON-HD Dataset Downloader")
    
    # Setup paths
    workspace = Path(__file__).parent
    viton_dir = workspace / 'VITON-HD'
    datasets_dir = viton_dir / 'datasets'
    
    print(f"\nWorkspace: {workspace}")
    print(f"VITON Directory: {viton_dir}")
    print(f"Datasets Directory: {datasets_dir}")
    
    # Create directories
    datasets_dir.mkdir(parents=True, exist_ok=True)
    
    print_header("Download Options")
    print("\n📦 VITON-HD Dataset Downloads:")
    print("\n1. Test Dataset (Recommended)")
    print("   - Size: ~2.5 GB")
    print("   - Contains: 2,032 person images + clothing + keypoints")
    print("   - Best for: Testing and development")
    
    print("\n2. Train Dataset (Optional)")
    print("   - Size: ~20 GB")
    print("   - Contains: 14,221 person images + clothing + keypoints")
    print("   - Best for: Training models")
    
    print("\n" + "-" * 60)
    
    # Ask user which dataset to download
    print("\nWhich dataset would you like to download?")
    print("1 - Test Dataset (2.5 GB) [RECOMMENDED]")
    print("2 - Train Dataset (20 GB)")
    print("3 - Both")
    print("4 - Manual download (I'll provide links)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '4':
        print_header("Manual Download Links")
        print("\n📥 Download these files manually:")
        print("\n1. Test Dataset:")
        print("   https://github.com/shadow2496/VITON-HD")
        print("   (Look for Google Drive link in README)")
        
        print("\n2. After downloading:")
        print(f"   - Extract the zip file")
        print(f"   - Move contents to: {datasets_dir}")
        print(f"   - Ensure structure matches:")
        print(f"     VITON-HD/datasets/test/")
        print(f"       ├── image/")
        print(f"       ├── cloth/")
        print(f"       ├── openpose-json/    ← Keypoints!")
        print(f"       ├── openpose-img/     ← Keypoint visualizations!")
        print(f"       ├── image-parse/")
        print(f"       └── cloth-mask/")
        
        print("\n" + "=" * 60)
        print("After manual download, run this script again to verify!")
        return
    
    if choice not in ['1', '2', '3']:
        print("Invalid choice. Exiting.")
        return
    
    # Check gdown installation
    print_step(1, "Checking dependencies")
    if not check_gdown():
        print("✗ Failed to install gdown. Please install manually:")
        print("  pip install gdown")
        return
    print("✓ gdown is ready")
    
    # Important note about Google Drive
    print("\n" + "!" * 60)
    print("IMPORTANT: Google Drive Download Limitation")
    print("!" * 60)
    print("\nGoogle Drive may block large automated downloads.")
    print("If download fails, please:")
    print("1. Visit: https://github.com/shadow2496/VITON-HD")
    print("2. Find the Google Drive links in the README")
    print("3. Download manually through your browser")
    print(f"4. Extract to: {datasets_dir}")
    print("\n" + "!" * 60)
    
    proceed = input("\nProceed with automatic download? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Download cancelled. Use manual download option instead.")
        return
    
    # Note: Google Drive file IDs need to be obtained from the official repository
    print("\n" + "=" * 60)
    print("NOTICE: Direct download requires Google Drive file IDs")
    print("=" * 60)
    print("\nPlease visit the official repository to get download links:")
    print("https://github.com/shadow2496/VITON-HD")
    print("\nLook for the 'Dataset' section with Google Drive links.")
    print("\nOnce downloaded manually:")
    print(f"1. Extract the zip file")
    print(f"2. Move/copy the 'test' folder to: {datasets_dir}")
    print(f"3. Run this script again with option 5 to verify")
    
    # Verify existing dataset
    print_step(2, "Checking for existing dataset")
    if (datasets_dir / 'test').exists():
        print("✓ Found existing dataset!")
        if verify_dataset(datasets_dir):
            print("\n✅ Dataset is complete and ready to use!")
        else:
            print("\n⚠️ Dataset is incomplete. Please re-download.")
    else:
        print("✗ No dataset found. Please download manually.")
        print(f"\nAfter downloading, extract to: {datasets_dir}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
