# 🎨 2D Clothing Addition System - Complete Guide

## Overview

I've created a **web-based tool** to easily add 2D clothing images (dresses, shirts, etc.) to your VITON-HD dataset. This tool automates all the processing, resizing, and integration steps!

---

## ✨ Features

### 🚀 What It Does:

1. **Drag & Drop Upload** - Easily add single or multiple clothing images
2. **Automatic Resizing** - Converts images to VITON-HD standard (768x1024)
3. **Background Options** - White, black, gray, or transparent backgrounds
4. **Cloth Mask Generation** - Automatically creates mask files
5. **Image Centering** - Centers clothing on background for best results
6. **Batch Processing** - Add multiple items at once
7. **Live Preview** - See all images before processing
8. **Smart ID Assignment** - Automatically assigns next available ID
9. **Dataset Integration** - Directly adds to VITON-HD dataset

---

## 🎯 How to Use

### Step 1: Access the Tool

1. **Start Flask server** (if not running):
   ```bash
   cd "C:\Users\Prasad\OneDrive\Desktop\vton github\web"
   python app.py
   ```

2. **Open in browser**:
   ```
   http://localhost:5000
   ```

3. **Click the green button**:
   - Look for "➕ Add 2D Clothing" tab
   - It's highlighted in green with a "TOOL" badge

### Step 2: Upload Images

**Method 1: Drag & Drop**
- Drag image files directly onto the upload area
- Multiple files supported!

**Method 2: Click to Browse**
- Click the upload area
- Select one or more image files
- Click "Open"

**Supported Formats:**
- ✅ JPG/JPEG
- ✅ PNG
- ✅ WebP

### Step 3: Configure Options

**Target Size:**
- `768 × 1024` - VITON-HD Standard (Recommended)
- `512 × 512` - Square format
- `1024 × 1024` - High quality
- `Keep Original Size` - No resizing

**Background Color:**
- `White` - Recommended for best results
- `Transparent` - For PNG outputs
- `Black` - Alternative background
- `Gray` - Neutral background

**Additional Options:**
- ☑️ **Create cloth mask** - Auto-generates mask files (recommended)
- ☑️ **Center image** - Centers clothing on background (recommended)
- **Filename prefix** - Optional (e.g., "dress", "nike")

### Step 4: Preview & Review

- **Selected Images** appear in a grid
- Each shows:
  - Preview thumbnail
  - Original filename
  - File size
- Click **×** button to remove any image

### Step 5: Process & Add

1. Click **"✨ Process & Add to Dataset"** button
2. Wait for progress bar to complete
3. See success message with:
   - Number of items added
   - Assigned cloth IDs
   - Updated total count

---

## 📊 Dashboard Stats

The tool shows real-time statistics:

- **Total Clothes** - Current items in dataset
- **Selected Files** - Images ready to process
- **Next Available ID** - Auto-assigned ID for new items

---

## 🎨 Example Use Cases

### Use Case 1: Adding a Single Dress

1. Save dress image (e.g., `red_dress.jpg`)
2. Go to Add 2D Clothing tool
3. Drag `red_dress.jpg` onto upload area
4. Keep default settings (768x1024, white background)
5. Click "Process & Add to Dataset"
6. Done! Dress is now `14680_00.jpg` in dataset

### Use Case 2: Batch Adding Multiple Shirts

1. Collect 5 shirt images
2. Select all 5 files at once
3. Choose:
   - Target size: 768 × 1024
   - Background: White
   - Prefix: "shirt"
4. Click "Process & Add to Dataset"
5. All 5 shirts added with IDs: 14680, 14681, 14682, 14683, 14684

### Use Case 3: Nike T-Shirts Collection

1. Save Nike shirt images (including the lime-green one)
2. Upload all at once
3. Set prefix: "nike"
4. Process
5. Now available in AR Try-On and regular try-on!

---

## 🔧 Technical Details

### File Structure After Adding

When you add a clothing item with ID `14680_00`:

```
VITON-HD/datasets/test/
├── cloth/
│   └── 14680_00.jpg          ← Your clothing image (768x1024)
└── cloth-mask/
    └── 14680_00.jpg          ← Auto-generated mask
```

### Automatic Processing Steps

1. **Load Image** - Reads uploaded file
2. **Convert to RGB** - Ensures proper color format
3. **Resize** - Scales to target dimensions
4. **Create Background** - Adds selected background color
5. **Center Image** - Positions clothing in center
6. **Save Cloth** - Saves to `cloth/` directory
7. **Generate Mask** - Creates mask in `cloth-mask/`
8. **Update Database** - Integrates with VITON-HD

### ID Assignment Logic

- Scans existing files for highest ID
- Auto-increments by 1 for each new item
- Format: `XXXXX_00.jpg` (5 digits + _00 suffix)
- Example sequence: 14680_00, 14681_00, 14682_00...

---

## 🎯 Best Practices

### Image Quality

✅ **Good Images:**
- High resolution (at least 512x512)
- Clean background (white or transparent)
- Flat lay or mannequin photography
- Good lighting, no shadows
- Clothing is centered

❌ **Avoid:**
- Low resolution/blurry images
- Person wearing the clothing
- Busy patterned backgrounds
- Dark/underexposed photos
- Extremely wrinkled clothing

### Processing Tips

1. **Use White Background**
   - Best compatibility with VITON-HD
   - Cleaner results in try-on

2. **Enable Centering**
   - Ensures consistent positioning
   - Better alignment in AR try-on

3. **Create Masks**
   - Important for full VITON-HD pipeline
   - Helps with realistic try-on generation

4. **Standard Size (768x1024)**
   - Optimal for VITON-HD model
   - Matches existing dataset

---

## 🚀 After Adding Clothes

### Make Them Available

**Method 1: Restart Server** (Recommended)
```bash
# In terminal running Flask
Ctrl + C  (stop server)
python app.py  (restart)
```

**Method 2: Hard Refresh Browser**
```
Ctrl + Shift + R
```

### Find Your New Clothes

1. **Main Interface**
   - Go to http://localhost:5000
   - Scroll in clothing selection
   - Look for your new IDs (14680_00, etc.)

2. **AR Try-On**
   - Click "AR Live Try-On" tab
   - Scroll in clothing panel
   - Select your new items

---

## 📱 Using Your New 2D Clothes

### In Regular Try-On

1. Select any person image
2. Scroll to find your new clothing
3. Click to select
4. Generate Virtual Try-On
5. See AI-generated result!

### In AR Live Try-On

1. Go to AR Try-On tab
2. Start camera
3. Select your new clothing item
4. Click "Men's Shirt Preset" for best fit
5. Use quick adjust buttons if needed
6. Capture photo!

---

## 🛠️ Troubleshooting

### Issue: "No files uploaded" error

**Solution:**
- Make sure you selected valid image files
- Check file format (JPG, PNG, WebP only)
- Try selecting files again

### Issue: Clothes don't appear after adding

**Solution:**
```bash
# 1. Verify files exist
dir "VITON-HD\datasets\test\cloth\14680_00.jpg"

# 2. Restart Flask server
# Press Ctrl+C in server terminal
python app.py

# 3. Hard refresh browser
# Ctrl + Shift + R
```

### Issue: Images look distorted

**Solution:**
- Use "Center image" option
- Choose 768×1024 target size
- Ensure source images are good quality

### Issue: Processing takes too long

**Solution:**
- Process fewer files at once (try 5-10 max)
- Reduce image size before uploading
- Close other browser tabs

### Issue: Wrong cloth ID assigned

**Solution:**
- The tool auto-detects next ID
- If you want specific ID, rename manually after processing
- Follow format: `XXXXX_00.jpg`

---

## 🎨 Advanced Usage

### Custom Backgrounds

While the tool offers basic backgrounds, you can edit images manually:

1. Process with transparent background
2. Open in image editor (Photoshop, GIMP)
3. Add custom background
4. Save over existing file in `cloth/` directory

### Batch Rename

If you want to organize by type:

```python
# Example: Rename dresses to sequential IDs
import os
from pathlib import Path

cloth_dir = Path("VITON-HD/datasets/test/cloth")

# Your custom renaming logic here
# But remember: VITON-HD expects XXXXX_00.jpg format!
```

### Creating Better Masks

For production use, consider:

1. **Using remove.bg** - Online background removal
2. **Photoshop Magic Wand** - Manual mask creation
3. **Python rembg library** - Automated background removal

```python
# Example: Better mask with rembg
from rembg import remove
from PIL import Image

input_path = "your_image.jpg"
output_path = "mask.jpg"

with open(input_path, 'rb') as i:
    input_data = i.read()
    output_data = remove(input_data)
    
    # Save as grayscale mask
    img = Image.open(BytesIO(output_data))
    mask = img.convert('L')
    mask.save(output_path)
```

---

## 📊 Dataset Statistics

After adding clothes, check your dataset:

```python
import os

cloth_dir = "VITON-HD/datasets/test/cloth"
clothes = [f for f in os.listdir(cloth_dir) if f.endswith('.jpg')]

print(f"Total clothing items: {len(clothes)}")
print(f"Latest ID: {max(clothes)}")

# Show last 10 items
print("\nRecently added:")
for item in sorted(clothes)[-10:]:
    print(f"  - {item}")
```

---

## 🎯 Next Steps

### After Adding Your First Items:

1. **Test in Regular Try-On**
   - Verify images load correctly
   - Check quality of generated results
   - Fine-tune if needed

2. **Test in AR Try-On**
   - See how they align on body
   - Adjust if positioning is off
   - Use quick adjustment controls

3. **Add More Clothes**
   - Build your collection!
   - Try different styles
   - Experiment with colors

4. **Share Results**
   - Capture screenshots
   - Save generated try-on images
   - Show off your virtual wardrobe!

---

## 💡 Pro Tips

1. **Pre-process Images**
   - Remove backgrounds before uploading
   - Crop to clothing only
   - Adjust brightness/contrast

2. **Organize by Type**
   - Use prefix feature
   - Keep source files organized
   - Document which ID = which item

3. **Quality Over Quantity**
   - Start with 5-10 good items
   - Test thoroughly
   - Expand based on results

4. **Backup Your Dataset**
   - Before bulk additions
   - After successful batches
   - Keep original source images

---

## 🔗 Related Tools & Guides

- **ADD_NIKE_SHIRT_GUIDE.md** - Specific Nike shirt addition
- **DATASET_MANAGEMENT.md** - Full dataset documentation
- **AR_TROUBLESHOOTING.md** - AR alignment issues
- **QUICK_ADJUST_GUIDE.md** - AR control buttons

---

## ❓ FAQ

**Q: How many clothes can I add at once?**
A: Technically unlimited, but recommend 10-20 at a time for best performance.

**Q: Can I delete clothes after adding?**
A: Yes, just delete the files from `cloth/` and `cloth-mask/` directories.

**Q: Will this work with my existing VITON-HD setup?**
A: Yes! It integrates seamlessly with your dataset.

**Q: What if I want a specific cloth ID?**
A: Add using the tool, then manually rename the files in the directories.

**Q: Can I add videos or GIFs?**
A: No, only static images (JPG, PNG, WebP).

**Q: Will added clothes work in AI try-on?**
A: Yes! They work in both regular try-on and AR try-on.

**Q: How do I remove a cloth from the dataset?**
A: Delete both files:
```bash
del "VITON-HD\datasets\test\cloth\14680_00.jpg"
del "VITON-HD\datasets\test\cloth-mask\14680_00.jpg"
```

---

## 🎉 Success!

You now have a powerful tool to easily expand your VITON-HD dataset with 2D clothing items!

**Quick Recap:**
1. Go to http://localhost:5000
2. Click "➕ Add 2D Clothing"
3. Drag & drop images
4. Configure options
5. Click "Process & Add"
6. Done! 🎊

**Your clothes are now ready for:**
- ✅ Regular virtual try-on
- ✅ AR live try-on
- ✅ AI recommendations
- ✅ Automatic pairing

---

**Happy clothing collection building! 👗👕🎽**
