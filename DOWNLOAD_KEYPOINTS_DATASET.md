# 📥 Download Keypoints Dataset for VITON-HD

## 🎯 What You Need:

For VITON-HD to work properly, you need:
1. **Person images** (already have ✓)
2. **Clothing images** (already have ✓)
3. **OpenPose keypoints** (JSON files) ← You may need these
4. **OpenPose rendered images** (visualization PNG files)
5. **Image segmentation** (parsing maps)

---

## 📦 Official VITON-HD Dataset Downloads:

### **Option 1: Full Dataset with Pre-computed Keypoints** (Recommended)

**VITON-HD Test Dataset**:
- **Link**: https://github.com/shadow2496/VITON-HD
- **Size**: ~2.5 GB
- **Includes**: All preprocessed data including keypoints

**Direct Download Links**:

1. **Test Dataset** (Recommended - smaller):
   ```
   https://drive.google.com/drive/folders/0B8kXrnobEVh9fnJHX3lCZzEtd20yUVAtTk5HdWk2OVV0RGl6YXc0NWhMcDZGU3pKSGx
   ```

2. **Train Dataset** (Larger, more data):
   ```
   https://drive.google.com/drive/folders/0B8kXrnobEVh9fnJHX3lCZzEtd20yUVAtTk5HdWk2OVV0RGl6YXc0NWhMcDZGU3pKSGx
   ```

**What's Included**:
```
test/
├── image/              (person images)
├── cloth/              (clothing images)
├── openpose-json/      ← KEYPOINTS (JSON format)
├── openpose-img/       ← KEYPOINTS (rendered visualization)
├── image-parse/        (segmentation maps)
└── cloth-mask/         (clothing masks)
```

---

## 🚀 Quick Download Guide:

### Step 1: Visit GitHub Repository
```
https://github.com/shadow2496/VITON-HD
```

### Step 2: Find Dataset Links
Scroll to **"Dataset"** section in README

### Step 3: Download from Google Drive
- Click the Google Drive links
- Download the ZIP files
- Extract to: `VITON-HD/datasets/`

---

## 💾 Alternative: Download OpenPose Keypoints Only

If you only need keypoints for existing images:

### **COCO-WholeBody Dataset** (Human Pose):
- **Link**: https://github.com/jin-s13/COCO-WholeBody
- **Format**: JSON files with 133 keypoints per person
- **Size**: Various sizes available

### **Human3.6M Dataset**:
- **Link**: http://vision.imar.ro/human3.6m/
- **Format**: JSON keypoints + 3D annotations
- **Size**: ~100GB (full dataset)

---

## 🛠️ Generate Keypoints from Your Own Images:

If you want to create keypoints for custom images:

### **Method 1: Use OpenPose** (Most Accurate)

1. **Download OpenPose**:
   ```
   https://github.com/CMU-Perceptual-Computing-Lab/openpose
   ```

2. **Run on your images**:
   ```bash
   openpose.bin --image_dir ./images --write_json ./output_keypoints/
   ```

3. **Output**: JSON files with keypoint coordinates

### **Method 2: Use MediaPipe** (Easier, Web-based)

Already integrated in your AR Try-On! MediaPipe Pose provides:
- 33 body landmarks
- Real-time detection
- Browser-based (no installation)

### **Method 3: Use Python Script**

I can create a script to generate keypoints for your images:

```python
# This would use MediaPipe or OpenPose
# to process images and save JSON keypoints
```

---

## 📁 Required Directory Structure:

After downloading, your structure should be:

```
VITON-HD/
└── datasets/
    └── test/
        ├── image/                     (2032 person images)
        ├── cloth/                     (2032 cloth images)
        ├── openpose-json/             ← KEYPOINTS JSON
        │   ├── 00006_00_keypoints.json
        │   ├── 00891_00_keypoints.json
        │   └── ... (2032 files)
        ├── openpose-img/              ← KEYPOINTS VISUALIZATION
        │   ├── 00006_00_rendered.png
        │   ├── 00891_00_rendered.png
        │   └── ... (2032 files)
        ├── image-parse/               (segmentation)
        └── cloth-mask/                (masks)
```

---

## 🎯 What Each Keypoint File Contains:

**OpenPose JSON Format** (openpose-json/):
```json
{
  "people": [
    {
      "pose_keypoints_2d": [
        x1, y1, confidence1,
        x2, y2, confidence2,
        ...  // 25 keypoints × 3 values
      ],
      "face_keypoints_2d": [...],
      "hand_left_keypoints_2d": [...],
      "hand_right_keypoints_2d": [...]
    }
  ]
}
```

**Key Landmarks**:
- 0: Nose
- 1: Neck
- 2: Right Shoulder
- 5: Left Shoulder
- 8: Mid Hip
- 9: Right Hip
- 12: Left Hip

---

## 📊 Recommended Downloads:

### For Your VITON-HD Project:

**Priority 1: VITON-HD Test Dataset** ✅
- Size: ~2.5 GB
- Has everything you need
- Pre-processed and ready to use

**Priority 2: Additional Training Data** (Optional)
- Size: ~20 GB
- More variety for testing
- Not required for basic functionality

---

## 🔗 Direct Download Commands:

### Using wget (if you have it):
```bash
# Download test dataset
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=FILE_ID' -O viton_test.zip

# Extract
unzip viton_test.zip -d VITON-HD/datasets/
```

### Using gdown (Python):
```bash
pip install gdown

# Download from Google Drive
gdown https://drive.google.com/uc?id=FILE_ID

# Extract
unzip viton_test.zip -d VITON-HD/datasets/
```

---

## ✅ Verification After Download:

Check if keypoints exist:

```bash
# Count JSON keypoint files
ls VITON-HD/datasets/test/openpose-json/*.json | wc -l
# Should show: 2032

# Count rendered keypoint images
ls VITON-HD/datasets/test/openpose-img/*.png | wc -l
# Should show: 2032

# Check a specific keypoint file
cat VITON-HD/datasets/test/openpose-json/00006_00_keypoints.json
```

---

## 🎨 Generate Your Own Keypoints:

If you want to process custom images, I can create a script:

**Would you like me to create a Python script that**:
1. Takes your person images
2. Uses MediaPipe to detect keypoints
3. Saves them in OpenPose JSON format
4. Compatible with VITON-HD?

---

## 💡 Quick Start:

**Easiest Option**:
1. Go to: https://github.com/shadow2496/VITON-HD
2. Click on Google Drive link in README
3. Download `test.zip` (~2.5 GB)
4. Extract to: `C:\Users\Prasad\OneDrive\Desktop\vton github\VITON-HD\datasets\`
5. Done! ✅

---

## 📞 Need Help?

Let me know if you want me to:
- ✅ Create a download script
- ✅ Generate keypoints for your images
- ✅ Verify your current dataset
- ✅ Convert between keypoint formats

---

## 🎯 Summary:

**Best Option for You**:
Download the official VITON-HD test dataset from GitHub - it includes all pre-computed keypoints in the correct format!

**Link**: https://github.com/shadow2496/VITON-HD (check README for Google Drive links)
