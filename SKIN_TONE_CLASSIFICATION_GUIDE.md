# 🎨 Skin Tone Classification System - Complete Guide

## Overview

This system automatically classifies person images in your VITON-HD dataset based on **skin tone** using scientifically validated computer vision algorithms.

---

## 🔬 **Technology & Algorithms Used**

### **1. ITA° (Individual Typology Angle)**

**Scientific Background:**
- Developed by Chardon et al., 1991
- Standard dermatological classification method
- Used globally in cosmetics, dermatology, and medical research

**Formula:**
```
ITA° = [arctan((L* - 50) / b*)] × (180 / π)
```

**Where:**
- `L*` = Lightness in CIE Lab color space (0-100)
- `b*` = Blue-Yellow axis in CIE Lab color space (-128 to +127)

**Why ITA°?**
✅ Perceptually uniform (matches human vision)  
✅ International standard  
✅ Objective and reproducible  
✅ Clinically validated  

---

### **2. Face Detection: Haar Cascade**

**Algorithm:** Viola-Jones Object Detection Framework

**How It Works:**
1. **Haar-like Features** - Rectangular patterns (edges, lines, centers)
2. **Integral Image** - Fast feature computation
3. **AdaBoost Learning** - Selects best features
4. **Cascade Classifier** - Rejects non-faces quickly

**Parameters:**
```python
detectMultiScale(
    scaleFactor=1.1,    # Image pyramid scale
    minNeighbors=5,     # Minimum detection confidence
    minSize=(50, 50)    # Minimum face size
)
```

---

### **3. Skin Detection: HSV Color Space**

**Algorithm:** Color-based segmentation

**Why HSV?**
- Separates color (Hue) from brightness (Value)
- Robust to lighting variations
- Skin has consistent Hue across tones

**Skin Color Range:**
```python
H: 0° to 20°      # Orange-red (skin hues)
S: 20 to 255      # Saturation (avoid grayscale)
V: 70 to 255      # Value (avoid very dark)
```

**Morphological Operations:**
- **Closing** - Fills small holes
- **Opening** - Removes noise
- **Kernel** - 5×5 elliptical structure

---

### **4. Color Space: CIE Lab**

**Why Lab?**
- Perceptually uniform (equal distances = equal color differences)
- Device-independent
- Separates luminance (L*) from chrominance (a*, b*)

**Channels:**
- `L*` (0-100): Lightness (black to white)
- `a*` (-128 to +127): Green to Red
- `b*` (-128 to +127): Blue to Yellow

---

## 📊 **Skin Tone Categories**

Based on ITA° angle classification:

| Category | ITA° Range | Description | Example |
|----------|-----------|-------------|---------|
| **Very Light** | 55° to 90° | Very fair skin | Northern European |
| **Light** | 41° to 55° | Fair skin | European, East Asian |
| **Intermediate** | 28° to 41° | Light brown skin | Mediterranean, South Asian |
| **Tan** | 10° to 28° | Medium brown skin | South Asian, Middle Eastern |
| **Brown** | -30° to 10° | Dark brown skin | African, South Asian |
| **Dark** | -90° to -30° | Very dark skin | Sub-Saharan African |

---

## 🚀 **How to Use**

### **Step 1: Run the Script**

```bash
cd "C:\Users\Prasad\OneDrive\Desktop\vton github"
python classify_skin_tone.py
```

### **Step 2: Processing**

The script will:
1. ✅ Load all person images from `VITON-HD/datasets/test/image/`
2. ✅ Detect face in each image
3. ✅ Extract skin pixels from face
4. ✅ Calculate average skin tone
5. ✅ Compute ITA° angle
6. ✅ Classify into categories
7. ✅ Generate detailed report

### **Step 3: Review Results**

**Output Directory:** `skin_tone_classification/`

```
skin_tone_classification/
├── skin_tone_classification.json  # Detailed classification data
├── SKIN_TONE_REPORT.md           # Comprehensive report
├── very_light/                    # Images with very light skin
├── light/                         # Images with light skin
├── intermediate/                  # Images with intermediate skin
├── tan/                          # Images with tan skin
├── brown/                        # Images with brown skin
├── dark/                         # Images with dark skin
└── unknown/                      # Failed detections
```

---

## 📈 **Processing Pipeline**

```
Person Image
    ↓
╔═══════════════════════╗
║  1. Face Detection    ║  (Haar Cascade)
╚═══════════════════════╝
    ↓
Face Region Extracted
    ↓
╔═══════════════════════╗
║  2. Skin Detection    ║  (HSV Color Range)
╚═══════════════════════╝
    ↓
Skin Pixels Masked
    ↓
╔═══════════════════════╗
║  3. Color Analysis    ║  (Average BGR → Lab)
╚═══════════════════════╝
    ↓
L* and b* Values
    ↓
╔═══════════════════════╗
║  4. ITA° Calculation  ║  (arctan formula)
╚═══════════════════════╝
    ↓
ITA° Angle
    ↓
╔═══════════════════════╗
║  5. Classification    ║  (Category lookup)
╚═══════════════════════╝
    ↓
Skin Tone Category
```

---

## 🔧 **Technical Details**

### **Algorithm Breakdown**

#### **Step 1: Face Detection**

```python
# Convert to grayscale (Haar works on intensity)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load pre-trained Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50,50))

# Select largest face (main subject)
largest_face = max(faces, key=lambda rect: rect[2] * rect[3])

# Extract with 10% padding
face_region = img[y1:y2, x1:x2]
```

#### **Step 2: Skin Segmentation**

```python
# Convert to HSV
hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

# Define skin range
lower_skin = [0, 20, 70]   # H, S, V minimum
upper_skin = [20, 255, 255] # H, S, V maximum

# Create binary mask
skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

# Morphological cleanup
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
```

#### **Step 3: Color Extraction**

```python
# Extract skin pixels only
skin_pixels = face_region[skin_mask > 0]

# Calculate average color
avg_skin_bgr = np.mean(skin_pixels, axis=0)

# Convert BGR → Lab
avg_lab = cv2.cvtColor(
    np.uint8([[avg_skin_bgr]]), 
    cv2.COLOR_BGR2Lab
)[0][0]

L = avg_lab[0]  # Lightness
b = avg_lab[2]  # Blue-Yellow
```

#### **Step 4: ITA° Calculation**

```python
def calculate_ita_angle(L, b):
    angle_rad = np.arctan((L - 50) / b)
    angle_deg = angle_rad * (180 / np.pi)
    return angle_deg
```

#### **Step 5: Classification**

```python
def classify_skin_tone(ita_angle):
    if 55 <= ita_angle < 90:
        return 'very_light'
    elif 41 <= ita_angle < 55:
        return 'light'
    elif 28 <= ita_angle < 41:
        return 'intermediate'
    elif 10 <= ita_angle < 28:
        return 'tan'
    elif -30 <= ita_angle < 10:
        return 'brown'
    else:
        return 'dark'
```

---

## 📊 **Output Files**

### **1. JSON Classification Data**

```json
{
  "total_images": 2032,
  "successful": 1987,
  "failed": 45,
  "classification": {
    "light": ["00006_00.jpg", "00008_00.jpg", ...],
    "tan": ["00013_00.jpg", ...],
    "brown": ["00017_00.jpg", ...]
  },
  "detailed_results": [
    {
      "filename": "00006_00.jpg",
      "category": "light",
      "category_name": "Light",
      "ita_angle": 48.3,
      "L": 72.5,
      "b": 15.2,
      "avg_color_bgr": [180, 155, 142]
    }
  ]
}
```

### **2. Markdown Report**

Includes:
- Statistical summary
- Classification method explanation
- Category distribution table
- Visual bar chart (text-based)
- Technical details

---

## 🎯 **Use Cases**

### **1. Dataset Analysis**

```
Understand skin tone diversity in your dataset:
- Are all skin tones represented?
- Is the dataset balanced?
- Which tones need more samples?
```

### **2. Bias Detection**

```
Ensure fair representation:
- Model may perform differently on under-represented tones
- Identify imbalances
- Guide data collection
```

### **3. Targeted Try-On**

```
Recommend clothing based on skin tone:
- Color harmony algorithms
- Seasonal color analysis
- Complementary color matching
```

### **4. Research & Analytics**

```
Scientific analysis:
- Skin tone distribution studies
- Cross-cultural analysis
- Dermatological applications
```

---

## 💡 **Advanced Features**

### **Customize Categories**

Edit `SKIN_TONE_CATEGORIES` in the script:

```python
SKIN_TONE_CATEGORIES = {
    'custom_light': {'min': 50, 'max': 90, 'name': 'Custom Light'},
    'custom_dark': {'min': -90, 'max': 50, 'name': 'Custom Dark'}
}
```

### **Adjust Skin Detection**

Modify HSV range for different lighting:

```python
# More permissive (includes more pixels)
lower_skin = [0, 15, 60]

# More restrictive (excludes more pixels)
upper_skin = [25, 255, 255]
```

### **Change Face Detection**

Use different cascade for profile faces:

```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_profileface.xml'
)
```

---

## 🛠️ **Troubleshooting**

### **Issue: "No face detected"**

**Causes:**
- Face not visible or occluded
- Side/profile view
- Poor image quality
- Very small face

**Solutions:**
- Use profile face cascade
- Adjust `minSize` parameter
- Lower `minNeighbors` (but more false positives)

### **Issue: "No skin detected"**

**Causes:**
- Face region too small
- Heavy makeup masking skin
- Extreme lighting

**Solutions:**
- Increase face padding
- Adjust HSV skin range
- Pre-process images (histogram equalization)

### **Issue: "Wrong classification"**

**Causes:**
- Poor lighting in photo
- Colored lighting affecting skin tone
- Shadows on face

**Solutions:**
- Use images with neutral lighting
- Apply color constancy algorithms
- Manual verification for edge cases

---

## 📚 **Scientific References**

1. **Chardon, A., Cretois, I., & Hourseau, C. (1991)**  
   "Skin colour typology and suntanning pathways"  
   *International Journal of Cosmetic Science*

2. **Viola, P., & Jones, M. (2001)**  
   "Rapid object detection using a boosted cascade of simple features"  
   *IEEE CVPR*

3. **Kolkur, S., et al. (2017)**  
   "Human Skin Detection Using RGB, HSV and YCbCr Color Models"  
   *ICCASP*

4. **Del Bino, S., & Bernerd, F. (2013)**  
   "Variations in skin colour and the biological consequences of ultraviolet radiation exposure"  
   *British Journal of Dermatology*

---

## 🎓 **Educational Value**

This system demonstrates:

### **Computer Vision Concepts:**
- Color space transformations (BGR → HSV → Lab)
- Object detection (Haar Cascades)
- Image segmentation (HSV masking)
- Morphological operations (erosion, dilation)

### **Machine Learning:**
- Feature extraction (color histograms)
- Classification (ITA° thresholds)
- Data organization and labeling

### **Scientific Computing:**
- NumPy array operations
- Mathematical transformations (arctan, degrees)
- Statistical analysis (mean, median)

---

## 🚀 **Integration Ideas**

### **1. Enhanced Recommendations**

```python
def recommend_by_skin_tone(person, skin_tone_category):
    """
    Recommend clothing colors that complement skin tone.
    
    Color Theory:
    - Light skin: Cool tones (blues, purples)
    - Tan skin: Warm tones (oranges, golds)
    - Dark skin: Vibrant tones (reds, jewel tones)
    """
    color_map = {
        'light': ['blue', 'purple', 'pink'],
        'tan': ['orange', 'gold', 'green'],
        'dark': ['red', 'yellow', 'white']
    }
    
    preferred_colors = color_map.get(skin_tone_category, [])
    # Filter clothing by dominant color...
```

### **2. Balanced Sampling**

```python
def create_balanced_dataset(classification, samples_per_category=100):
    """
    Create balanced dataset with equal representation.
    """
    balanced = []
    for category, files in classification.items():
        if category == 'unknown':
            continue
        sampled = np.random.choice(files, 
                                  min(samples_per_category, len(files)),
                                  replace=False)
        balanced.extend(sampled)
    return balanced
```

### **3. Fairness Testing**

```python
def test_model_fairness(model, classification):
    """
    Test if model performs equally across skin tones.
    """
    results = {}
    for category, files in classification.items():
        accuracy = evaluate_model(model, files)
        results[category] = accuracy
    
    # Check if accuracy variance is acceptable
    fairness_score = np.std(list(results.values()))
    return results, fairness_score
```

---

## ✨ **Summary**

This skin tone classification system:

✅ **Uses scientifically validated methods** (ITA°)  
✅ **Fully automated** (no manual labeling)  
✅ **Objective and reproducible**  
✅ **Generates comprehensive reports**  
✅ **Organizes dataset for easy access**  
✅ **Enables fairness analysis**  
✅ **Educational and research-ready**  

---

**Run it now and gain deep insights into your dataset's diversity!** 🎨📊
