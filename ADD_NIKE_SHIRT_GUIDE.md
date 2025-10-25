# 🎽 Adding Nike Athletic Shirt to VITON-HD Dataset

## Quick Start

You have **2 options** to add the Nike shirt to your dataset:

---

## Option 1: Automated Script (Recommended) ⚡

### Steps:

1. **Save the Nike shirt image** to your computer (e.g., `Downloads/nike_shirt.png`)

2. **Run the script:**
   ```bash
   python add_nike_shirt_direct.py
   ```

3. **Enter the image path** when prompted:
   ```
   Path: C:\Users\Prasad\Downloads\nike_shirt.png
   ```

4. **Done!** The script will:
   - Resize the image to 768x1024 (VITON-HD standard)
   - Save it as `14680_00.jpg` in `VITON-HD/datasets/test/cloth/`
   - Create a mask in `VITON-HD/datasets/test/cloth-mask/`

---

## Option 2: Manual Addition 🔧

### Steps:

1. **Save the Nike shirt image** from the conversation

2. **Process the image:**
   - Open in any image editor (Paint, Photoshop, GIMP, etc.)
   - Resize to **768 x 1024 pixels**
   - Save as JPG with high quality

3. **Copy to dataset:**
   ```bash
   # Copy to cloth directory
   copy your_nike_image.jpg "VITON-HD\datasets\test\cloth\14680_00.jpg"
   ```

4. **Create a mask (optional but recommended):**
   ```bash
   # Copy the same image as a mask
   copy your_nike_image.jpg "VITON-HD\datasets\test\cloth-mask\14680_00.jpg"
   ```

---

## What Happens Next? 🚀

### 1. **Web Interface**
   - Restart Flask server: `python web/app.py`
   - Refresh your browser (Ctrl + Shift + R)
   - The Nike shirt appears in clothing selection!
   - Filename: `14680_00.jpg`

### 2. **AR Try-On**
   - Go to "AR Live Try-On" tab
   - Scroll through clothing selector
   - Find the Nike lime-green/white shirt
   - Click to select and try it on!

### 3. **Best Results Tips**
   - Use the **"Men's Shirt Preset"** button for optimal alignment
   - The bright lime-green shoulders make it easy to see positioning
   - Adjust with sliders if needed
   - Works best with frontal-facing person images

---

## About the Nike Shirt 👕

**Description:**
- White athletic t-shirt with lime-green/yellow raglan sleeves
- Nike brand logo on chest
- "NIKE RUNNING" text on sleeves
- Performance fabric design
- Women's athletic fit

**Dataset Info:**
- **Cloth ID:** `14680_00`
- **Filename:** `14680_00.jpg`
- **Category:** Athletic/Sports wear
- **Color:** White + Lime Green
- **Type:** Short-sleeve t-shirt

---

## Troubleshooting 🔍

### Issue: "Shirt doesn't appear in web interface"
**Solution:**
- Restart the Flask server
- Hard refresh browser (Ctrl + Shift + R)
- Check file exists: `VITON-HD/datasets/test/cloth/14680_00.jpg`

### Issue: "Image looks distorted in AR"
**Solution:**
- Make sure image is exactly 768x1024 pixels
- Use "Men's Shirt Preset" button for better alignment
- Adjust vertical offset slider

### Issue: "Shirt appears at wrong position"
**Solution:**
- Enable "Show Body Keypoints"
- Use quick adjustment buttons (⬆️⬇️⬅️➡️)
- Fine-tune with sliders

---

## Alternative: Adding Multiple Clothing Items

If you want to add more clothes later:

```python
# Use the generic script
python add_nike_shirt.py

# It will:
# - Auto-detect next available ID
# - Prompt for image path
# - Handle all processing automatically
```

---

## File Locations 📁

```
VITON-HD/datasets/test/
├── cloth/
│   └── 14680_00.jpg          ← Nike shirt image
├── cloth-mask/
│   └── 14680_00.jpg          ← Shirt mask
├── image/                     (person images)
├── openpose-json/             (pose keypoints)
└── openpose-img/              (pose visualizations)
```

---

## Testing the Nike Shirt 🧪

### Quick Test:
1. Open web interface: `http://localhost:5000`
2. Select any person image
3. Scroll to find `14680_00.jpg` (last item in clothing list)
4. Click "Generate Virtual Try-On"

### AR Test:
1. Click "AR Live Try-On" tab
2. Allow camera access
3. Select Nike shirt from clothing panel
4. See it live on your body!

---

## Need Help? 💬

- Check `AR_TROUBLESHOOTING.md` for alignment issues
- See `QUICK_ADJUST_GUIDE.md` for AR controls
- Review `SHOULDER_ALIGNMENT_FIX.md` for positioning tips

---

**Enjoy your new Nike athletic shirt in VITON-HD! 🎉**
