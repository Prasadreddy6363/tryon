# 📊 VITON-HD Dataset Management Guide

## Current Dataset Statistics

### Test Dataset Contents:
- **People:** 2,032 images
- **Clothes:** 2,038 items (after adding Nike shirt: 2,039)
- **Cloth Masks:** 2,032 masks
- **OpenPose JSON:** 2,032 keypoint files
- **OpenPose Images:** 2,032 rendered poses

---

## Adding New Clothing Items

### Method 1: Single Item Addition (Automated)

```bash
# For the Nike shirt specifically
python add_nike_shirt_direct.py

# For any clothing item
python add_nike_shirt.py
```

**What it does:**
- Auto-detects next available ID
- Resizes to 768x1024 (VITON-HD standard)
- Creates cloth mask
- Saves to correct directories

---

### Method 2: Manual Batch Addition

If you have multiple clothing items:

1. **Prepare Images:**
   - Format: JPG or PNG
   - Recommended: Clean background (white/transparent)
   - Any size (will be auto-resized)

2. **Naming Convention:**
   ```
   XXXXX_00.jpg
   
   Examples:
   14680_00.jpg  ← Nike shirt (lime green)
   14681_00.jpg  ← Next item
   14682_00.jpg  ← Next item
   ```

3. **Copy to Dataset:**
   ```bash
   copy your_clothes\*.jpg VITON-HD\datasets\test\cloth\
   copy your_clothes\*.jpg VITON-HD\datasets\test\cloth-mask\
   ```

---

## File Naming Rules ⚠️

### CRITICAL: Follow VITON-HD Convention

✅ **CORRECT:**
- `00006_00.jpg` - 5 digits + _00 suffix
- `14680_00.jpg` - Leading zeros preserved
- `99999_00.jpg` - Max ID supported

❌ **WRONG:**
- `6_00.jpg` - Missing leading zeros
- `14680.jpg` - Missing _00 suffix
- `shirt_nike.jpg` - Descriptive names not supported
- `14680_01.jpg` - Use _00 only (not _01, _02, etc.)

### Why This Matters:
The VITON-HD DataLoader expects this exact format. Incorrect naming = file won't be loaded!

---

## Clothing Image Requirements

### Optimal Format:
- **Dimensions:** 768 x 1024 pixels (W x H)
- **Aspect Ratio:** 3:4 (same as 768:1024)
- **Background:** White or transparent
- **Position:** Centered, flat lay or mannequin
- **Format:** JPEG (quality 85-95%)

### What Works Best:
✅ Flat lay photography (item laid flat)
✅ Mannequin/ghost mannequin photography
✅ Product photography on white background
✅ Clean cutout with transparent background

### Avoid:
❌ Person wearing the item (use those for 'image' folder)
❌ Wrinkled or folded clothing
❌ Busy/patterned backgrounds
❌ Very small or very large images (quality loss)

---

## Creating Cloth Masks

### What is a Cloth Mask?
A binary mask showing where the clothing is in the image:
- **White (255):** Clothing pixels
- **Black (0):** Background pixels

### Quick Method:
For most cases, a simple white mask works:
```python
from PIL import Image
mask = Image.new('L', (768, 1024), 255)  # All white
mask.save('14680_00.jpg')
```

### Advanced Method (Better Results):
Use background removal tools:
1. **Online:** remove.bg, photoscissors.com
2. **Python:** rembg library
3. **Manual:** Photoshop magic wand + export mask

---

## Dataset Organization Tips

### Directory Structure:
```
VITON-HD/datasets/test/
│
├── cloth/                    ← Clothing images
│   ├── 00006_00.jpg         (2,038 existing)
│   ├── ...
│   └── 14680_00.jpg         ← Your Nike shirt
│
├── cloth-mask/              ← Binary masks for clothes
│   ├── 00006_00.jpg
│   └── 14680_00.jpg
│
├── image/                   ← Person photos
│   └── (2,032 files)
│
├── openpose-json/           ← Body keypoints
│   └── (2,032 .json files)
│
├── openpose-img/            ← Pose visualizations
│   └── (2,032 _rendered.png files)
│
├── image-parse/             ← Segmentation maps
├── image-densepose/         ← Dense pose maps
├── agnostic-v3.2/          ← Person without clothes
└── image-parse-agnostic-v3.2/
```

---

## Checking Dataset Integrity

### Verify New Item Added:
```bash
# Windows
dir VITON-HD\datasets\test\cloth\14680_00.jpg
dir VITON-HD\datasets\test\cloth-mask\14680_00.jpg

# Linux/Mac
ls -lh VITON-HD/datasets/test/cloth/14680_00.jpg
ls -lh VITON-HD/datasets/test/cloth-mask/14680_00.jpg
```

### Count Items:
```python
import os

cloth_dir = "VITON-HD/datasets/test/cloth"
count = len([f for f in os.listdir(cloth_dir) if f.endswith('.jpg')])
print(f"Total clothing items: {count}")
# Should show: 2039 (after adding Nike shirt)
```

---

## Recommended Workflow for Multiple Items

### Step-by-step:

1. **Collect Images**
   - Download product photos
   - Or photograph your own clothes
   - Save to a temporary folder

2. **Batch Process**
   ```python
   # Create a simple batch script:
   from PIL import Image
   import os
   
   input_folder = "new_clothes/"
   start_id = 14680
   
   for i, filename in enumerate(os.listdir(input_folder)):
       img = Image.open(os.path.join(input_folder, filename))
       img = img.convert('RGB')
       
       # Resize
       img.thumbnail((768, 1024), Image.Resampling.LANCZOS)
       
       # Save with proper ID
       new_id = f"{start_id + i:05d}_00"
       img.save(f"VITON-HD/datasets/test/cloth/{new_id}.jpg")
   ```

3. **Create Masks**
   - Use same process for masks
   - Or copy cloth images as masks (simple approach)

4. **Test in Web Interface**
   - Restart Flask server
   - Refresh browser
   - Verify all items appear

---

## Nike Shirt Specific Info

### Added Item Details:
- **Cloth ID:** 14680_00
- **Type:** Athletic t-shirt
- **Brand:** Nike Running
- **Colors:** White body + Lime green sleeves
- **Style:** Women's raglan sleeve athletic wear

### Perfect For Testing:
- The bright lime-green color makes alignment very visible
- Clean design shows clothing deformation clearly
- Athletic fit works well with various body types

---

## Future Additions

### Next Available IDs:
```
14681_00  ← Next item
14682_00  ← Next item
14683_00  ← Next item
...
```

### Recommended Items to Add:
- Plain t-shirts (various colors)
- Button-up shirts
- Polo shirts
- Tank tops
- Long-sleeve shirts

**Tip:** Start with simple, solid-color items for best results!

---

## Common Issues & Solutions

### Issue: "Item doesn't show in web interface"
```bash
# Check file exists
dir VITON-HD\datasets\test\cloth\14680_00.jpg

# Restart Flask server
# Press Ctrl+C in server terminal
python web/app.py

# Hard refresh browser
# Ctrl + Shift + R
```

### Issue: "Wrong image size"
```python
from PIL import Image
img = Image.open('your_image.jpg')
img = img.resize((768, 1024), Image.Resampling.LANCZOS)
img.save('14680_00.jpg')
```

### Issue: "Mask missing"
```python
# Create simple white mask
from PIL import Image
mask = Image.new('L', (768, 1024), 255)
mask.save('VITON-HD/datasets/test/cloth-mask/14680_00.jpg')
```

---

## Best Practices 🌟

1. **Always backup** the dataset before bulk changes
2. **Use consistent naming** (follow XXXXX_00.jpg format)
3. **Keep original images** in a separate folder
4. **Test one item** before batch-adding many
5. **Document your additions** (which ID = which item)
6. **Restart server** after adding items
7. **Hard refresh browser** to clear cache

---

## Quick Reference Commands

```bash
# Check dataset status
dir VITON-HD\datasets\test\cloth | find /c ".jpg"

# Add single item (automated)
python add_nike_shirt_direct.py

# Add generic item
python add_nike_shirt.py

# Restart Flask server
python web/app.py

# Open web interface
start http://localhost:5000
```

---

**Your Nike shirt is now part of the VITON-HD dataset! 🎽✨**
