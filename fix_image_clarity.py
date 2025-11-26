"""
Quick Fix: Improve Clarity of All Generated Images
Automatically enhances all images in VITON-HD results directory
"""

import os
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import shutil

def quick_enhance(image_path):
    """Quick enhancement for maximum clarity"""
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply enhancements for clarity
        # 1. Sharpen
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        # 2. Slight contrast boost
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 3. Unsharp mask for extra clarity
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        # Save with maximum quality
        img.save(image_path, format='JPEG', quality=95, optimize=True, subsampling=0)
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("QUICK FIX: IMPROVE IMAGE CLARITY")
    print("="*70)
    
    results_dir = Path('VITON-HD/results')
    
    if not results_dir.exists():
        print("\n❌ Results directory not found: VITON-HD/results")
        print("   Make sure you have generated some try-on results first.")
        return
    
    # Find all result directories
    result_dirs = [d for d in results_dir.iterdir() if d.is_dir() and d.name != 'backup_original']
    
    if not result_dirs:
        print("\n❌ No result directories found")
        return
    
    print(f"\n🔍 Found {len(result_dirs)} result directories")
    
    # Process each directory
    total_enhanced = 0
    total_images = 0
    
    for result_dir in result_dirs:
        # Find images
        images = list(result_dir.glob('*.jpg')) + list(result_dir.glob('*.jpeg'))
        
        if not images:
            continue
        
        print(f"\n📁 Processing: {result_dir.name}")
        print(f"   Found {len(images)} images")
        
        # Create backup
        backup_dir = result_dir / 'backup_original'
        if not backup_dir.exists():
            backup_dir.mkdir()
            print(f"   📦 Creating backup...")
        
        # Enhance each image
        for img_path in images:
            # Backup if not already backed up
            backup_path = backup_dir / img_path.name
            if not backup_path.exists():
                shutil.copy2(img_path, backup_path)
            
            # Enhance
            if quick_enhance(img_path):
                total_enhanced += 1
                print(f"   ✅ Enhanced: {img_path.name}")
            else:
                print(f"   ❌ Failed: {img_path.name}")
            
            total_images += 1
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✅ Enhanced: {total_enhanced}/{total_images} images")
    print(f"📦 Originals backed up in: backup_original/ folders")
    
    print("\n💡 IMPROVEMENTS APPLIED:")
    print("   • Sharpness increased by 50%")
    print("   • Contrast enhanced by 10%")
    print("   • Unsharp mask applied for clarity")
    print("   • JPEG quality set to 95 (maximum)")
    print("   • No chroma subsampling (best color)")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Refresh your browser")
    print("   2. View the enhanced results")
    print("   3. Compare with backup_original/ if needed")
    
    print("\n📚 FOR FUTURE GENERATIONS:")
    print("   The quality fix is now permanent in VITON-HD/utils.py")
    print("   All new results will have maximum quality automatically!")
    
    print("\n" + "="*70)
    print("✅ DONE! Your images now have better clarity!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
