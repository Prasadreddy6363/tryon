# 🎯 Generate Keypoints for VITON-HD

## Two Options for Getting Keypoints:

---

## Option 1: 📥 Download Pre-computed Dataset (Easiest)

### Official VITON-HD Dataset:

**Link**: https://github.com/shadow2496/VITON-HD

**What you get**:
- ✅ 2,032 person images with keypoints
- ✅ 2,032 clothing images
- ✅ Pre-computed OpenPose JSON files
- ✅ Rendered keypoint visualizations
- ✅ Image segmentation maps

**Download Steps**:
1. Visit: https://github.com/shadow2496/VITON-HD
2. Scroll to "Dataset" section
3. Click Google Drive link for "test" dataset (~2.5 GB)
4. Extract to: `VITON-HD/datasets/test/`

**Structure after extraction**:
```
VITON-HD/datasets/test/
├── image/           (person images)
├── cloth/           (clothing images)
├── openpose-json/   ← KEYPOINTS (JSON)
├── openpose-img/    ← KEYPOINTS (visualizations)
├── image-parse/     (segmentation)
└── cloth-mask/      (masks)
```

---

## Option 2: 🛠️ Generate Your Own Keypoints

### Use the Provided Script

I've created `generate_keypoints.py` that:
- ✅ Uses MediaPipe Pose detection
- ✅ Converts to OpenPose format
- ✅ Compatible with VITON-HD
- ✅ Creates JSON + visualization files

### Installation:

```bash
# Navigate to project directory
cd "c:\Users\Prasad\OneDrive\Desktop\vton github"

# Activate virtual environment
.\.venv\Scripts\activate

# Install MediaPipe
pip install mediapipe
```

### Usage:

#### **Method 1: Automatic (if images are in standard location)**

```bash
python generate_keypoints.py
```

This will automatically process images in:
- Input: `VITON-HD/datasets/test/image/`
- Output JSON: `VITON-HD/datasets/test/openpose-json/`
- Output Images: `VITON-HD/datasets/test/openpose-img/`

#### **Method 2: Custom directories**

```bash
python generate_keypoints.py -i <input_dir> -j <json_output> -r <render_output>
```

Example:
```bash
python generate_keypoints.py \
  -i "VITON-HD/datasets/test/image" \
  -j "VITON-HD/datasets/test/openpose-json" \
  -r "VITON-HD/datasets/test/openpose-img"
```

### What It Does:

1. **Reads** all images from input directory
2. **Detects** pose using MediaPipe (33 landmarks)
3. **Converts** to OpenPose format (25 keypoints)
4. **Saves** JSON files with keypoint coordinates
5. **Creates** visualization images showing detected pose

### Output Format:

**JSON File** (`00006_00_keypoints.json`):
```json
{
  "version": 1.3,
  "people": [
    {
      "person_id": [-1],
      "pose_keypoints_2d": [
        x1, y1, confidence1,
        x2, y2, confidence2,
        ...  // 25 keypoints × 3 values
      ],
      "face_keypoints_2d": [],
      "hand_left_keypoints_2d": [],
      "hand_right_keypoints_2d": []
    }
  ]
}
```

**Rendered Image** (`00006_00_rendered.png`):
- Green dots at keypoint locations
- Green lines connecting skeleton
- Visual verification of detection quality

---

## 🎯 Comparison: Download vs Generate

| Aspect | Download Dataset | Generate Keypoints |
|--------|------------------|-------------------|
| **Speed** | Fast (one-time download) | Slower (processes each image) |
| **Accuracy** | High (OpenPose) | Good (MediaPipe) |
| **Ease** | Very easy | Moderate |
| **Custom Images** | No | Yes ✅ |
| **File Size** | 2.5 GB | Depends on your images |
| **Best For** | Quick start, testing | Custom datasets |

---

## 📊 Keypoint Detection Quality:

### MediaPipe vs OpenPose:

**MediaPipe** (our script):
- ✅ Fast (runs in browser/CPU)
- ✅ Easy to install
- ✅ 33 landmarks (more detailed)
- ⚠️ Slightly less accurate than OpenPose
- ✅ Good enough for VITON-HD

**OpenPose** (original dataset):
- ✅ Very accurate
- ✅ 25 keypoints (standard)
- ❌ Harder to install
- ❌ Requires GPU for speed
- ✅ Professional quality

---

## 🔍 Verify Generated Keypoints:

After generating, check the files:

```bash
# Count generated JSON files
ls VITON-HD/datasets/test/openpose-json/*.json | wc -l

# Count rendered images
ls VITON-HD/datasets/test/openpose-img/*.png | wc -l

# View a keypoint file
cat VITON-HD/datasets/test/openpose-json/00006_00_keypoints.json

# Open a rendered image to verify detection
start VITON-HD/datasets/test/openpose-img/00006_00_rendered.png
```

---

## 💡 Troubleshooting:

### Issue: "No pose detected"
**Solution**: 
- Ensure person is fully visible in image
- Good lighting conditions
- Person facing camera
- Try different images

### Issue: MediaPipe not installed
**Solution**:
```bash
pip install mediapipe opencv-python
```

### Issue: Low accuracy
**Solution**:
- Use higher resolution images
- Ensure clear pose (not occluded)
- Consider downloading official dataset instead

### Issue: Script runs slow
**Solution**:
- Normal! Processing takes time
- MediaPipe processes each image individually
- Consider downloading pre-computed dataset for faster setup

---

## 🚀 Quick Start Recommendation:

### For Testing/Learning:
**Download the official dataset** → Fastest way to get started!

### For Custom Images:
**Use the generation script** → Create keypoints for your own images!

### For Production:
**Use OpenPose directly** → Best accuracy, professional results

---

## 📝 Example Workflow:

### Scenario 1: Quick Start (Recommended)
```bash
1. Download dataset from GitHub (2.5 GB)
2. Extract to VITON-HD/datasets/
3. Done! Ready to use ✓
```

### Scenario 2: Custom Images
```bash
1. Put your images in VITON-HD/datasets/test/image/
2. Run: python generate_keypoints.py
3. Keypoints generated in openpose-json/ ✓
4. Visualizations in openpose-img/ ✓
```

---

## ✅ My Recommendation:

**Best option for you**: 

**Download the official VITON-HD test dataset**

Why:
- ✅ Pre-processed and ready to use
- ✅ High-quality OpenPose keypoints
- ✅ Includes all necessary files
- ✅ Saves time
- ✅ Professional quality

**Link**: https://github.com/shadow2496/VITON-HD
(Look for Google Drive link in README)

---

## 🎯 Summary:

1. **Easiest**: Download official dataset
2. **Most Flexible**: Generate with provided script
3. **Best Quality**: Use OpenPose directly
4. **For AR Try-On**: MediaPipe (already integrated!)

**Need help deciding? Let me know your use case!**
