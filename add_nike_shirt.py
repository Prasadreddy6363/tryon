"""
Add Nike Athletic Shirt to VITON-HD Dataset
This script downloads and adds the Nike shirt image to the dataset.
"""

import os
import requests
from PIL import Image
import io

# Configuration
DATASET_DIR = "VITON-HD/datasets/test"
CLOTH_DIR = os.path.join(DATASET_DIR, "cloth")

def get_next_cloth_id():
    """Find the next available cloth ID based on existing files."""
    existing_files = [f for f in os.listdir(CLOTH_DIR) if f.endswith('.jpg')]
    existing_ids = []
    
    for filename in existing_files:
        try:
            # Extract numeric ID from filename like "00006_00.jpg"
            id_part = filename.split('_')[0]
            if id_part.isdigit():
                existing_ids.append(int(id_part))
        except:
            continue
    
    if existing_ids:
        max_id = max(existing_ids)
        next_id = max_id + 1
    else:
        next_id = 1
    
    # Format as 5-digit with _00 suffix
    return f"{next_id:05d}_00"

def add_nike_shirt_from_file(image_path):
    """
    Add Nike shirt from a local image file.
    
    Args:
        image_path: Path to the Nike shirt image
    """
    # Get next available ID
    cloth_id = get_next_cloth_id()
    filename = f"{cloth_id}.jpg"
    output_path = os.path.join(CLOTH_DIR, filename)
    
    print(f"📥 Loading image from: {image_path}")
    
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to standard dimensions (similar to other cloth items)
        # VITON-HD typically uses 768x1024 for clothing images
        target_size = (768, 1024)
        
        # Maintain aspect ratio
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create a white background and paste the image centered
        final_img = Image.new('RGB', target_size, (255, 255, 255))
        
        # Center the image
        x_offset = (target_size[0] - img.width) // 2
        y_offset = (target_size[1] - img.height) // 2
        final_img.paste(img, (x_offset, y_offset))
        
        # Save to dataset
        final_img.save(output_path, 'JPEG', quality=95)
        
        print(f"✅ Successfully added Nike shirt!")
        print(f"   Cloth ID: {cloth_id}")
        print(f"   Filename: {filename}")
        print(f"   Location: {output_path}")
        print(f"   Size: {final_img.size}")
        
        return cloth_id, filename
        
    except Exception as e:
        print(f"❌ Error adding shirt: {e}")
        return None, None

def create_simple_mask(cloth_id):
    """
    Create a simple white mask for the cloth (optional but recommended).
    This is needed for the full VITON-HD pipeline.
    """
    mask_dir = os.path.join(DATASET_DIR, "cloth-mask")
    cloth_path = os.path.join(CLOTH_DIR, f"{cloth_id}.jpg")
    mask_path = os.path.join(mask_dir, f"{cloth_id}.jpg")
    
    try:
        # Load the cloth image
        cloth_img = Image.open(cloth_path)
        
        # Create a simple mask (white where cloth exists, black for background)
        # For now, create a full white mask - you can refine this later
        mask = Image.new('L', cloth_img.size, 255)  # White mask
        
        mask.save(mask_path, 'JPEG', quality=95)
        print(f"✅ Created cloth mask: {mask_path}")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not create mask: {e}")
        return False

def main():
    print("=" * 60)
    print("🎽 Nike Athletic Shirt - Dataset Addition Tool")
    print("=" * 60)
    print()
    
    # Check if dataset directory exists
    if not os.path.exists(CLOTH_DIR):
        print(f"❌ Error: Cloth directory not found: {CLOTH_DIR}")
        print("   Please ensure VITON-HD dataset is set up correctly.")
        return
    
    print("📁 Dataset directory found!")
    print(f"   Location: {CLOTH_DIR}")
    print()
    
    # Prompt for image path
    print("Please provide the Nike shirt image:")
    print("1. Drag and drop the image file here, OR")
    print("2. Enter the full path to the image file")
    print()
    
    image_path = input("Image path: ").strip().strip('"').strip("'")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return
    
    # Add the shirt
    print()
    print("🔄 Processing Nike shirt...")
    print()
    
    cloth_id, filename = add_nike_shirt_from_file(image_path)
    
    if cloth_id:
        print()
        print("🎨 Creating cloth mask...")
        create_simple_mask(cloth_id)
        
        print()
        print("=" * 60)
        print("✨ SUCCESS! Nike shirt added to dataset")
        print("=" * 60)
        print()
        print("📋 Next Steps:")
        print("   1. The shirt is now available in the web interface")
        print("   2. Refresh your browser to see it in the clothing selection")
        print(f"   3. Look for: {filename}")
        print()
        print("🎯 For AR Try-On:")
        print("   - The shirt will appear in the AR clothing selector")
        print("   - Use the 'Men's Shirt Preset' button for best alignment")
        print()
        print("💡 Tips:")
        print("   - If the shirt doesn't align well, adjust using sliders")
        print("   - The lime-green shoulders make it easy to see alignment")
        print("   - Try it with different person images for best results")
        print()

if __name__ == "__main__":
    main()
