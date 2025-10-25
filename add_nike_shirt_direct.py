"""
Direct Nike Shirt Addition - Saves the uploaded image to dataset
"""

import os
from PIL import Image

# Configuration
DATASET_DIR = "VITON-HD/datasets/test"
CLOTH_DIR = os.path.join(DATASET_DIR, "cloth")
MASK_DIR = os.path.join(DATASET_DIR, "cloth-mask")

# The next ID based on the highest existing ID (14679)
CLOTH_ID = "14680_00"
FILENAME = f"{CLOTH_ID}.jpg"

def process_and_save_shirt(input_image_path):
    """Process and save the Nike shirt to the dataset."""
    
    output_path = os.path.join(CLOTH_DIR, FILENAME)
    mask_path = os.path.join(MASK_DIR, FILENAME)
    
    try:
        print(f"📥 Loading Nike shirt image...")
        
        # Open the image
        img = Image.open(input_image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"   Original size: {img.size}")
        
        # Resize to match VITON-HD cloth dimensions (768x1024)
        target_size = (768, 1024)
        
        # Resize while maintaining aspect ratio
        img_copy = img.copy()
        img_copy.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create white background
        final_img = Image.new('RGB', target_size, (255, 255, 255))
        
        # Center the image
        x_offset = (target_size[0] - img_copy.width) // 2
        y_offset = (target_size[1] - img_copy.height) // 2
        final_img.paste(img_copy, (x_offset, y_offset))
        
        # Save cloth image
        final_img.save(output_path, 'JPEG', quality=95)
        print(f"✅ Saved cloth image: {output_path}")
        print(f"   Size: {final_img.size}")
        
        # Create simple white mask
        mask = Image.new('L', target_size, 255)
        mask.save(mask_path, 'JPEG', quality=95)
        print(f"✅ Created mask: {mask_path}")
        
        print()
        print("=" * 70)
        print("🎉 Nike Athletic Shirt Successfully Added!")
        print("=" * 70)
        print()
        print(f"📝 Details:")
        print(f"   Cloth ID: {CLOTH_ID}")
        print(f"   Filename: {FILENAME}")
        print(f"   Location: {output_path}")
        print()
        print(f"🚀 Next Steps:")
        print(f"   1. Restart the Flask web server if it's running")
        print(f"   2. Refresh your browser")
        print(f"   3. The Nike shirt will appear in the clothing selection")
        print(f"   4. For AR Try-On, click the AR Live Try-On tab")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🎽 Adding Nike Athletic Shirt to VITON-HD Dataset")
    print("=" * 70)
    print()
    
    # Ask for the image path
    print("Please enter the path to the Nike shirt image:")
    print("(You can drag and drop the file here)")
    print()
    
    image_path = input("Path: ").strip().strip('"').strip("'")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        print()
        print("Please make sure:")
        print("  1. The file path is correct")
        print("  2. The file exists")
        print("  3. You have permission to read the file")
    else:
        print()
        process_and_save_shirt(image_path)
