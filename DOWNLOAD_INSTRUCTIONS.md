# 📥 Download VITON-HD Dataset with Keypoints

## ✅ Quick Start Guide

---

## Step 1: Visit the Official Repository

**Link**: https://github.com/shadow2496/VITON-HD

---

## Step 2: Find the Dataset Links

Scroll down to the **"Dataset"** section in the README.

You'll see Google Drive links for:
- **Test dataset** (~2.5 GB) ← Start with this one!
- **Train dataset** (~20 GB) ← Optional, for training

---

## Step 3: Download the Test Dataset

1. Click the **Google Drive link** for "test" dataset
2. Google Drive will open in your browser
3. Click **"Download"** button
4. Save the ZIP file (e.g., `viton_test.zip`)

**Expected file size**: ~2.5 GB

---

## Step 4: Extract the Dataset

1. **Locate the downloaded ZIP file** (probably in your Downloads folder)

2. **Extract** the ZIP file

3. **Move** the extracted folder to:
   ```
   C:\Users\Prasad\OneDrive\Desktop\vton github\VITON-HD\datasets\
   ```

4. **Final structure should be**:
   ```
   VITON-HD/
   └── datasets/
       └── test/
           ├── image/              (2,032 person images)
           ├── cloth/              (2,032 clothing images)
           ├── openpose-json/      ← KEYPOINTS! (2,032 JSON files)
           ├── openpose-img/       ← KEYPOINT IMAGES! (2,032 PNG files)
           ├── image-parse/        (segmentation maps)
           └── cloth-mask/         (clothing masks)
   ```

---

## Step 5: Verify the Download

Run the verification script:

```bash
cd "C:\Users\Prasad\OneDrive\Desktop\vton github"
.\.venv\Scripts\activate
python download_dataset.py
```

Select option **"5"** to verify the dataset.

Or manually check:
- `VITON-HD\datasets\test\openpose-json\` should have 2,032 JSON files
- `VITON-HD\datasets\test\openpose-img\` should have 2,032 PNG files

---

## ✅ What You Get:

### OpenPose Keypoints (JSON files):
**Location**: `VITON-HD/datasets/test/openpose-json/`

**Example file**: `00006_00_keypoints.json`
```json
{
  "people": [
    {
      "pose_keypoints_2d": [
        x1, y1, confidence1,
        x2, y2, confidence2,
        ...  // 25 keypoints
      ]
    }
  ]
}
```

**Keypoints include**:
- Nose (0)
- Neck (1)
- Shoulders (2, 5)
- Elbows (3, 6)
- Wrists (4, 7)
- Hips (9, 12)
- Knees (10, 13)
- Ankles (11, 14)

### Keypoint Visualizations (PNG images):
**Location**: `VITON-HD/datasets/test/openpose-img/`

**Example file**: `00006_00_rendered.png`
- Shows skeleton overlay on person
- Green dots and lines
- Visual verification of pose detection

---

## 🎯 After Download:

Your VITON-HD system will now have:

✅ **Person images** with proper keypoints
✅ **Clothing images** 
✅ **OpenPose JSON data** for pose detection
✅ **Rendered keypoint images** for verification
✅ **Segmentation maps** for body parsing
✅ **Clothing masks**

Everything needed for the virtual try-on to work properly!

---

## 🔧 Alternative: Use Download Helper Script

```bash
cd "C:\Users\Prasad\OneDrive\Desktop\vton github"
.\.venv\Scripts\activate
python download_dataset.py
```

The script will:
1. Guide you through the process
2. Provide direct links
3. Verify the dataset structure
4. Check for missing files

---

## 📊 Dataset Statistics:

**Test Dataset**:
- **Size**: 2.5 GB (compressed)
- **Person images**: 2,032
- **Clothing images**: 2,032
- **Keypoint files**: 2,032 JSON + 2,032 PNG
- **Image resolution**: 1024×768
- **Format**: JPG (images), JSON (keypoints), PNG (rendered)

---

## ⚠️ Important Notes:

1. **Directory names matter!**
   - Must be `openpose-json` (with hyphen)
   - Must be `openpose-img` (with hyphen)
   - Must be `image-parse` (without version number)

2. **File naming convention**:
   - Person image: `00006_00.jpg`
   - Keypoint JSON: `00006_00_keypoints.json`
   - Keypoint image: `00006_00_rendered.png`

3. **Keypoint quality**:
   - Some images may have empty keypoint data
   - Check `openpose-img` visualizations to verify
   - Files like `00006_00` and `00891_00` are known to have good keypoints

---

## 🚀 Quick Checklist:

- [ ] Visit https://github.com/shadow2496/VITON-HD
- [ ] Download test dataset from Google Drive
- [ ] Extract ZIP file
- [ ] Move to `VITON-HD/datasets/test/`
- [ ] Verify `openpose-json` folder exists (2,032 files)
- [ ] Verify `openpose-img` folder exists (2,032 files)
- [ ] Check directory naming (hyphens, not underscores)
- [ ] Run verification script

---

## ✅ You're Done!

Once downloaded, your virtual try-on system will have:
- ✅ All necessary keypoint data
- ✅ Proper pose detection information
- ✅ Ready for both manual and AR try-on

**The keypoints are essential for accurate clothing alignment!**

---

## 💡 Need Help?

If you encounter issues:
1. Check the GitHub repository issues section
2. Verify directory structure matches exactly
3. Run the verification script
4. Make sure file names match the pattern

**The download is straightforward - just follow the steps above!** 🎉
