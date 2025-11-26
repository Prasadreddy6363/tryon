"""
Improve Generated Image Quality
Enhances clarity and sharpness of VITON-HD output images
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import shutil

def enhance_image(input_path, output_path=None, settings=None):
    """
    Enhance image quality with various improvements
    
    Args:
        input_path: Path to input image
        output_path: Path to save enhanced image (optional)
        settings: Dict with enhancement settings (optional)
    """
    if output_path is None:
        output_path = input_path
    
    # Default settings for maximum quality
    default_settings = {
        'sharpness': 1.5,      # Increase sharpness (1.0 = original, >1.0 = sharper)
        'contrast': 1.1,       # Slight contrast boost
        'color': 1.05,         # Slight color saturation
        'brightness': 1.0,     # Keep original brightness
        'denoise': True,       # Apply denoising
        'unsharp_mask': True,  # Apply unsharp mask for clarity
        'save_quality': 95     # JPEG quality (0-100)
    }
    
    if settings:
        default_settings.update(settings)
    
    # Load image
    img = Image.open(input_path)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Apply enhancements
    if default_settings['denoise']:
        # Reduce noise while preserving edges
        img = img.filter(ImageFilter.MedianFilter(size=3))
    
    if default_settings['sharpness'] != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(default_settings['sharpness'])
    
    if default_settings['contrast'] != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(default_settings['contrast'])
    
    if default_settings['color'] != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(default_settings['color'])
    
    if default_settings['brightness'] != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(default_settings['brightness'])
    
    if default_settings['unsharp_mask']:
        # Apply unsharp mask for extra clarity
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Save with maximum quality
    img.save(output_path, 
             format='JPEG', 
             quality=default_settings['save_quality'],
             optimize=True,
             subsampling=0)  # No chroma subsampling for best quality
    
    return output_path


def batch_enhance_directory(directory, backup=True, settings=None):
    """
    Enhance all images in a directory
    
    Args:
        directory: Path to directory containing images
        backup: Create backup before enhancing
        settings: Enhancement settings dict
    """
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    # Find all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
        image_files.extend(directory.glob(ext))
    
    if not image_files:
        print(f"❌ No images found in {directory}")
        return
    
    print(f"\n🔍 Found {len(image_files)} images to enhance")
    
    # Create backup if requested
    if backup:
        backup_dir = directory / 'backup_original'
        backup_dir.mkdir(exist_ok=True)
        print(f"📦 Creating backup in: {backup_dir}")
    
    # Process each image
    enhanced_count = 0
    for img_path in image_files:
        try:
            # Backup original
            if backup:
                backup_path = backup_dir / img_path.name
                if not backup_path.exists():
                    shutil.copy2(img_path, backup_path)
            
            # Enhance image
            enhance_image(img_path, settings=settings)
            enhanced_count += 1
            print(f"✅ Enhanced: {img_path.name}")
            
        except Exception as e:
            print(f"❌ Failed to enhance {img_path.name}: {e}")
    
    print(f"\n🎉 Enhanced {enhanced_count}/{len(image_files)} images")
    
    if backup:
        print(f"📦 Original images backed up to: {backup_dir}")


def enhance_latest_result():
    """Enhance the most recently generated result"""
    results_dir = Path('VITON-HD/results')
    
    if not results_dir.exists():
        print("❌ Results directory not found")
        return
    
    # Find latest result directory
    result_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
    if not result_dirs:
        print("❌ No result directories found")
        return
    
    latest_dir = max(result_dirs, key=lambda d: d.stat().st_mtime)
    
    print(f"\n🔍 Processing latest results from: {latest_dir.name}")
    batch_enhance_directory(latest_dir, backup=True)


def show_quality_comparison(original_path, enhanced_path):
    """Show file size comparison"""
    original_size = Path(original_path).stat().st_size
    enhanced_size = Path(enhanced_path).stat().st_size
    
    print(f"\n📊 Quality Comparison:")
    print(f"   Original: {original_size:,} bytes")
    print(f"   Enhanced: {enhanced_size:,} bytes")
    print(f"   Difference: {enhanced_size - original_size:+,} bytes")


def main():
    print("\n" + "="*60)
    print("IMAGE QUALITY ENHANCEMENT TOOL")
    print("="*60)
    
    print("\nWhat would you like to do?")
    print("1. Enhance latest generated results")
    print("2. Enhance all results in a specific directory")
    print("3. Enhance a single image")
    print("4. Apply custom settings")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        print("\n🚀 Enhancing latest results...")
        enhance_latest_result()
        
    elif choice == '2':
        directory = input("\nEnter directory path: ").strip()
        if directory:
            batch_enhance_directory(directory, backup=True)
        else:
            print("❌ No directory specified")
    
    elif choice == '3':
        image_path = input("\nEnter image path: ").strip()
        if image_path and Path(image_path).exists():
            output_path = input("Enter output path (press Enter for same): ").strip()
            if not output_path:
                output_path = image_path
            
            print(f"\n🚀 Enhancing {image_path}...")
            enhance_image(image_path, output_path)
            print(f"✅ Enhanced image saved to: {output_path}")
        else:
            print("❌ Image not found")
    
    elif choice == '4':
        print("\n⚙️ Custom Settings")
        print("Enter values (press Enter for default):")
        
        settings = {}
        
        sharpness = input("Sharpness (1.0-2.0, default 1.5): ").strip()
        if sharpness:
            settings['sharpness'] = float(sharpness)
        
        contrast = input("Contrast (1.0-1.3, default 1.1): ").strip()
        if contrast:
            settings['contrast'] = float(contrast)
        
        quality = input("JPEG Quality (80-100, default 95): ").strip()
        if quality:
            settings['save_quality'] = int(quality)
        
        directory = input("\nEnter directory to process: ").strip()
        if directory:
            batch_enhance_directory(directory, backup=True, settings=settings)
    
    else:
        print("❌ Invalid choice")
    
    print("\n" + "="*60)
    print("✅ DONE!")
    print("="*60)
    
    print("\n💡 TIPS FOR BEST QUALITY:")
    print("   • Use high-quality input images (1024x1024+)")
    print("   • Ensure good lighting in source photos")
    print("   • Use plain backgrounds")
    print("   • Avoid over-compression")
    
    print("\n📚 RELATED FILES:")
    print("   • MAXIMUM_ACCURACY_GUIDE.md - Complete quality guide")
    print("   • improve_accuracy.py - AR accuracy improvements")
    print("   • apply_maximum_accuracy.py - Maximum settings")


if __name__ == "__main__":
    main()
