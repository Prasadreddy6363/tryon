# 📸 Live Camera Virtual Try-On - Quick Start

## ✨ NEW FEATURE ADDED!

Stand in front of your camera → System captures stable image → Virtual try-on applied automatically!

---

## 🚀 RUN COMMAND

```bash
python live_camera_tryon.py
```

---

## 📋 What It Does

1. **Opens your camera**
2. **Detects when you stand still** (automatic stability detection)
3. **Captures your image** when stable
4. **Applies virtual try-on** with selected clothing
5. **Shows result** in ~35-40 seconds

---

## 🎯 Quick Instructions

### Step 1: Run
```bash
python live_camera_tryon.py
```

### Step 2: Select Clothing
```
Enter clothing filename (or number 1-5 for recommended): 1
```

### Step 3: Position Yourself
- Stand 3-6 feet from camera
- Face camera directly
- Arms slightly away from body
- Stand still

### Step 4: Capture
- System auto-captures when you're stable (green bar)
- Or press **'c'** to capture immediately
- Press **'q'** to quit

### Step 5: View Result
- Result displayed automatically
- Also at: http://127.0.0.1:5000 (History tab)

---

## ✅ Features

- ✅ **Automatic stability detection** - No need to press buttons
- ✅ **Real-time feedback** - See stability indicator
- ✅ **Manual capture option** - Press 'c' anytime
- ✅ **Clothing selection** - Choose from 2000+ items
- ✅ **Full integration** - Works with web interface
- ✅ **Result history** - All captures saved

---

## 🎨 Best Practices

### For Best Results:
- ✅ Good lighting (bright, even)
- ✅ Plain background
- ✅ Front-facing pose
- ✅ Form-fitting clothes
- ✅ Stand still for 1-2 seconds

### Avoid:
- ❌ Poor lighting or shadows
- ❌ Cluttered background
- ❌ Side/back views
- ❌ Crossed arms
- ❌ Moving around

---

## 📊 Performance

- **Capture time**: 1-3 seconds (when standing still)
- **Processing time**: ~30 seconds
- **Total time**: ~35-40 seconds
- **Quality**: Same as regular try-on

---

## 🔧 Controls

| Key | Action |
|-----|--------|
| **Stand Still** | Auto-capture when stable |
| **'c'** | Force capture immediately |
| **'q'** | Quit without capturing |

---

## 📁 Where Files Are Saved

- **Captured images**: `camera_captures/`
- **Processed images**: `VITON-HD/datasets/test/image/`
- **Results**: `VITON-HD/results/camera_*/`
- **Web view**: http://127.0.0.1:5000 → History

---

## 🐛 Troubleshooting

### Camera won't open?
- Close other apps using camera
- Check camera permissions
- Try: `cap = cv2.VideoCapture(1)` (different camera)

### Can't capture stable frame?
- Stand more still
- Better lighting
- Press 'c' to force capture

### Poor results?
- Improve lighting
- Plain background
- Better pose (front-facing)
- See: LIVE_CAMERA_TRYON_GUIDE.md

---

## 📚 Documentation

- **Quick Start**: This file
- **Detailed Guide**: LIVE_CAMERA_TRYON_GUIDE.md
- **Accuracy Tips**: ACCURACY_IMPROVEMENT_GUIDE.md
- **Full Setup**: SETUP_COMPLETE.md

---

## 🎉 Example Usage

```bash
# Run the live camera try-on
python live_camera_tryon.py

# Select clothing (enter 1 for first recommended)
> 1

# Camera opens - stand in front
# System detects stability
# Auto-captures when you're still
# Processes virtual try-on (~30s)
# Result displayed!
```

---

## ✨ Summary

**NEW FEATURE**: Live camera capture with automatic stability detection!

**RUN NOW**:
```bash
python live_camera_tryon.py
```

**RESULT**: Your photo with virtual clothing in ~40 seconds!

---

**The feature is ready to use! Try it now! 🚀**
