# 📸 Live Camera Virtual Try-On Guide

## ✨ New Feature: Capture & Try-On

Stand in front of your camera, and the system will automatically capture a stable image and apply virtual try-on with your selected clothing!

---

## 🚀 Quick Start

### Run the Live Camera Try-On:
```bash
python live_camera_tryon.py
```

### What Happens:
1. **Select Clothing** - Choose from available items
2. **Camera Opens** - Your webcam activates
3. **Stand Still** - System detects when you're stable
4. **Auto Capture** - Takes photo when you stop moving
5. **Virtual Try-On** - Applies selected clothing (~30 seconds)
6. **View Result** - See your try-on result!

---

## 📋 Step-by-Step Instructions

### Step 1: Run the Script
```bash
python live_camera_tryon.py
```

### Step 2: Select Clothing
You'll see a list of available clothing items:
```
AVAILABLE CLOTHING ITEMS
1. 00008_00.jpg
2. 00013_00.jpg
3. 00034_00.jpg
...

Recommended items:
  1. 00008_00.jpg
  2. 00013_00.jpg
  3. 00034_00.jpg
  4. 00055_00.jpg
  5. 00067_00.jpg

Enter clothing filename (or number 1-5 for recommended):
```

**Options:**
- Type a number (1-5) for recommended items
- Type the full filename
- Press Enter for default

### Step 3: Camera Positioning
When the camera opens, position yourself:

✅ **DO:**
- Stand 3-6 feet from camera
- Face the camera directly
- Keep arms slightly away from body
- Ensure good lighting
- Stand in front of plain background
- Wear form-fitting clothes

❌ **DON'T:**
- Stand too close or too far
- Turn sideways
- Cross your arms
- Stand in shadows
- Have cluttered background

### Step 4: Capture
The system will automatically capture when you're stable:

**Stability Indicator:**
- Red bar = Moving (keep still)
- Green bar = Stable (capturing soon)
- Full green bar = Captured!

**Manual Controls:**
- Press **'c'** to force capture immediately
- Press **'q'** to quit without capturing

### Step 5: Processing
After capture:
1. Image is preprocessed (resized to 768x1024)
2. Confirm to continue with try-on
3. Virtual try-on runs (~30 seconds)
4. Result is displayed

### Step 6: View Result
- Result shown in new window
- Also saved in `VITON-HD/results/camera_*/`
- View in web interface at http://127.0.0.1:5000

---

## ⚙️ How It Works

### Stability Detection
The system uses motion detection to ensure a clear, stable image:

1. **Frame Comparison** - Compares consecutive frames
2. **Motion Calculation** - Measures pixel changes
3. **Stability Threshold** - Requires <2% motion
4. **Stable Frames** - Needs 15 consecutive stable frames
5. **Auto Capture** - Takes photo when stable

### Image Processing
1. **Capture** - Raw image from camera (1280x720)
2. **Resize** - Scaled to VITON-HD size (768x1024)
3. **Save** - Stored in dataset directory
4. **Try-On** - Processed through VITON-HD model

### Virtual Try-On Pipeline
1. **Segmentation** - Body parts identified
2. **Pose Detection** - Keypoints extracted
3. **Geometric Matching** - Clothing warped to fit
4. **Synthesis** - Final realistic result generated

---

## 🎯 Best Practices

### For Best Results:

#### Lighting
- ✅ Bright, even lighting
- ✅ Natural daylight or soft white light
- ❌ Avoid harsh shadows
- ❌ Avoid backlighting

#### Pose
- ✅ Stand straight, face camera
- ✅ Arms slightly away from body
- ✅ Relaxed, natural stance
- ❌ Don't cross arms
- ❌ Don't put hands in pockets

#### Background
- ✅ Plain, solid color
- ✅ Minimal clutter
- ✅ Good contrast with your clothing
- ❌ Busy patterns
- ❌ Similar color to your clothes

#### Clothing (What You're Wearing)
- ✅ Form-fitting top
- ✅ Solid colors work best
- ✅ Clear shoulder definition
- ❌ Very loose clothing
- ❌ Bulky jackets

#### Distance
- ✅ 3-6 feet from camera
- ✅ Full upper body visible
- ✅ Head to waist in frame
- ❌ Too close (face only)
- ❌ Too far (full body tiny)

---

## 🔧 Configuration

### Adjust Stability Settings
Edit `live_camera_tryon.py`:

```python
# More sensitive (captures faster, may be less stable)
stable_capture = StableFrameCapture(
    stability_threshold=0.03,  # Higher = more lenient
    stable_frames_required=10   # Lower = faster capture
)

# Less sensitive (captures slower, more stable)
stable_capture = StableFrameCapture(
    stability_threshold=0.01,  # Lower = stricter
    stable_frames_required=20   # Higher = more stable
)
```

### Camera Resolution
```python
# Higher resolution (better quality, slower)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Lower resolution (faster, lower quality)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## 🐛 Troubleshooting

### Camera Won't Open
**Problem**: "Error: Could not open camera"

**Solutions:**
1. Check camera is connected
2. Close other apps using camera (Zoom, Skype, etc.)
3. Try different camera index:
   ```python
   cap = cv2.VideoCapture(1)  # Try 1, 2, 3...
   ```
4. Check camera permissions in Windows Settings

### Can't Capture Stable Frame
**Problem**: Stability bar never fills

**Solutions:**
1. Stand more still
2. Use a tripod for camera
3. Improve lighting (reduce shadows)
4. Lower stability threshold (see Configuration)
5. Press 'c' to force capture

### Try-On Fails
**Problem**: "Try-on failed" or "No result generated"

**Solutions:**
1. Ensure preprocessing data exists
2. Check captured image quality
3. Run: `python generate_keypoints.py`
4. Use better lighting and pose
5. Try with dataset images first

### Poor Quality Results
**Problem**: Result looks inaccurate or blurry

**Solutions:**
1. Improve camera positioning (see Best Practices)
2. Better lighting
3. Stand in front of plain background
4. Wear form-fitting clothes
5. Ensure full upper body visible
6. Generate proper preprocessing:
   ```bash
   python generate_keypoints.py
   ```

### Slow Processing
**Problem**: Takes too long to process

**Expected**: ~30 seconds on CPU is normal

**To Speed Up:**
1. Close other applications
2. Use GPU if available
3. Lower image resolution
4. Optimize system (see ACCURACY_IMPROVEMENT_GUIDE.md)

---

## 📊 Performance

### Expected Times:
- **Camera initialization**: 1-2 seconds
- **Stable capture**: 1-3 seconds (when standing still)
- **Image preprocessing**: <1 second
- **Virtual try-on**: ~30 seconds (CPU)
- **Total time**: ~35-40 seconds

### Quality:
- **Camera capture**: 1280x720 (HD)
- **Processed image**: 768x1024 (VITON-HD standard)
- **Result quality**: Same as regular try-on

---

## 🎨 Features

### Current Features:
✅ Automatic stability detection  
✅ Real-time stability indicator  
✅ Manual capture option  
✅ Clothing selection  
✅ Image preprocessing  
✅ Virtual try-on integration  
✅ Result display  
✅ Save to history  

### Limitations:
⚠️ Requires preprocessing for best results  
⚠️ CPU processing is slow (~30s)  
⚠️ Works best with front-facing poses  
⚠️ Upper body clothing only  

### Future Enhancements:
🔮 Automatic pose detection  
🔮 Real-time preprocessing  
🔮 Multiple clothing items  
🔮 Full body try-on  
🔮 GPU acceleration  

---

## 📁 File Locations

### Captured Images:
```
camera_captures/capture_<timestamp>.jpg
```

### Processed Images:
```
VITON-HD/datasets/test/image/camera_<timestamp>.jpg
```

### Results:
```
VITON-HD/results/camera_<timestamp>/
```

### View in Web Interface:
```
http://127.0.0.1:5000 → History tab
```

---

## 🔗 Integration with Web Interface

The live camera feature integrates with the existing web interface:

1. **Captured images** are saved to the dataset
2. **Results** appear in History tab
3. **All features** work with captured images
4. **AI recommendations** can suggest clothing

### Access from Web:
The AR Try-On page already has live camera features:
```
http://127.0.0.1:5000/ar_tryon
```

---

## 💡 Tips & Tricks

### Quick Capture:
Press 'c' immediately to skip stability detection

### Multiple Tries:
Run the script multiple times to try different clothing

### Compare Results:
```bash
python compare_results.py --list
python compare_results.py --compare 1 2 3
```

### Best Clothing Choices:
Start with simple, solid-color shirts:
- 00008_00.jpg - Simple white shirt
- 00013_00.jpg - Plain design
- 00034_00.jpg - Clean pattern

### Lighting Setup:
- Use 2-3 soft light sources
- Position lights at 45° angles
- Avoid direct overhead lighting
- Natural window light works great

---

## 🎯 Example Workflow

### Complete Try-On Session:

1. **Prepare**:
   ```bash
   # Ensure web server is running
   cd web
   python app.py
   ```

2. **Run Live Capture**:
   ```bash
   python live_camera_tryon.py
   ```

3. **Select Clothing**:
   ```
   Enter: 1  (for first recommended item)
   ```

4. **Position Yourself**:
   - Stand 4 feet from camera
   - Face camera directly
   - Arms slightly away from body
   - Stand still

5. **Wait for Capture**:
   - Watch stability bar turn green
   - System captures automatically
   - Or press 'c' to force capture

6. **Confirm**:
   ```
   Continue with try-on? (y/n): y
   ```

7. **Wait for Processing**:
   - ~30 seconds
   - Result displayed automatically

8. **View Results**:
   - Check displayed result
   - Open http://127.0.0.1:5000
   - Go to History tab
   - See your try-on!

---

## 📞 Summary

The **Live Camera Virtual Try-On** feature allows you to:
- ✅ Capture yourself with your camera
- ✅ Automatically detect stable frames
- ✅ Apply virtual try-on with selected clothing
- ✅ View results in ~35-40 seconds

**Run it now:**
```bash
python live_camera_tryon.py
```

**For best results:**
- Good lighting
- Plain background
- Front-facing pose
- Stand still for capture

**The feature is ready to use!** 🚀
