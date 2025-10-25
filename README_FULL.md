# 🎨 VITON-HD AI Virtual Try-On System

A complete AI-powered virtual clothing try-on system with advanced features including real-time AR try-on, skin tone classification, smart recommendations, and 2D clothing management.

![VITON-HD](https://img.shields.io/badge/VITON--HD-Virtual%20Try--On-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red)

## ✨ Features

### 🎯 Core Capabilities
- **Virtual Try-On**: Deep learning-based clothing synthesis using VITON-HD architecture
- **Real-Time AR Try-On**: Live camera-based try-on with pose detection
- **AI Recommendations**: Smart clothing suggestions based on color harmony
- **Skin Tone Classification**: Scientific ITA° algorithm for inclusive dataset analysis
- **2D Clothing Manager**: Drag-and-drop interface for adding new garments
- **Auto Background Removal**: Automatic white background removal for clean overlays

### 🧠 AI Features
- Color histogram-based similarity matching
- Cosine similarity for recommendations
- MediaPipe pose detection for AR alignment
- Face detection with Haar Cascade
- HSV-based skin segmentation
- CIE Lab color space analysis

### 🎨 Skin Tone Classification
- **Scientific Method**: ITA° (Individual Typology Angle)
- **Categories**: Very Light, Light, Intermediate, Tan, Brown, Dark
- **Automatic Detection**: Face and skin region detection
- **Dataset Organization**: Auto-organize images by skin tone
- **Inclusive Testing**: Filter and test across diverse skin tones

## 📋 Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features Guide](#features-guide)
- [API Documentation](#api-documentation)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- CUDA-capable GPU (recommended) or CPU
- Git
- 8GB+ RAM

### Step 1: Clone Repository
```bash
git clone https://github.com/Prasadreddy6363/virtual-ar-try-on.git
cd virtual-ar-try-on
```

### Step 2: Install Dependencies
```bash
pip install torch torchvision torchaudio
pip install kornia opencv-python pillow numpy scikit-learn
pip install flask mediapipe
```

### Step 3: Download Dataset
```bash
python download_dataset.py
```

### Step 4: Download Model Checkpoints
Download pre-trained models and place in `VITON-HD/checkpoints/`:
- `seg_final.pth` - Segmentation Network
- `gmm_final.pth` - Geometric Matching Module
- `alias_final.pth` - ALIAS Generator

### Step 5: Generate Keypoints (Optional)
```bash
python generate_keypoints.py
```

## 🎯 Quick Start

### Launch Web Interface
```bash
cd web
python app.py
```

Open browser to `http://127.0.0.1:5000`

### Basic Try-On
1. Select a person image
2. Select a clothing item
3. Click "Generate Virtual Try-On"
4. View results!

### AR Live Try-On
1. Click "AR Try-On" tab
2. Allow camera access
3. Select clothing
4. Adjust position and opacity
5. Capture screenshots

### Skin Tone Classification
```bash
python classify_skin_tone.py
```

This creates:
- `skin_tone_classification/skin_tone_classification.json`
- `skin_tone_classification/SKIN_TONE_REPORT.md`
- Organized image directories by skin tone

## 📖 Features Guide

### 1️⃣ Manual Try-On
**Path**: Main page → Manual Selection tab

- Browse person images
- Browse clothing items
- Search functionality
- Click to select
- Generate try-on result

### 2️⃣ AI Recommendations
**Path**: Main page → Click "Smart Recommendations"

- Select a person first
- AI analyzes skin tone and features
- Recommends best-matching clothes
- Based on color harmony analysis

### 3️⃣ Similar Items Search
**Path**: Main page → "Similar People" or "Similar Clothes"

- Select an item
- AI finds visually similar items
- Color histogram matching
- Cosine similarity ranking

### 4️⃣ Auto-Pairing
**Path**: Main page → Auto-Pair tab

- AI generates best person-cloth combinations
- Considers pose compatibility
- Color harmony analysis
- One-click application

### 5️⃣ AR Live Try-On
**Path**: AR Try-On tab

**Features**:
- Real-time camera feed
- MediaPipe pose detection
- Shoulder-aligned clothing overlay
- Adjustable opacity (0-100%)
- Scale controls
- Capture and save

**Controls**:
- **Opacity Slider**: Adjust transparency
- **Scale Buttons**: Size up/down
- **Reset**: Return to defaults
- **Capture**: Screenshot with clothing

### 6️⃣ Skin Tone Filtering
**Path**: Main page → Skin Tone Filter panel

**Categories**:
- All People
- Light Skin (ITA° 41-55°)
- Intermediate Skin (ITA° 28-41°)
- Tan Skin (ITA° 10-28°)
- Brown Skin (ITA° -30-10°)
- Dark Skin (ITA° -90--30°)

**Usage**:
1. Run `classify_skin_tone.py` first
2. Click any skin tone button
3. Gallery filters to show only that category
4. Status shows count

### 7️⃣ Add 2D Clothing
**Path**: Main page → Add 2D Clothing tab

**Features**:
- Drag-and-drop upload
- Batch processing
- Auto background removal
- Size normalization
- Preview before saving

**Settings**:
- Target size (1024x768, 768x1024, 512x512)
- Background color (transparent, white, black, gray)
- Center image option
- Auto-mask creation

## 🔧 API Documentation

### Recommendation API
```python
POST /api/recommend_clothes
Content-Type: application/json

{
    "person": "00891_00.jpg"
}

Response:
{
    "recommendations": ["shirt1.jpg", "shirt2.jpg", ...]
}
```

### Skin Tone Filter API
```python
POST /api/skin_tone_filter
Content-Type: application/json

{
    "skin_tone": "intermediate"  # or 'light', 'tan', 'brown', 'dark', 'all'
}

Response:
{
    "people": ["person1.jpg", "person2.jpg", ...],
    "total": 1486,
    "category": "intermediate"
}
```

### Similar Items API
```python
POST /api/similar_items
Content-Type: application/json

{
    "type": "person",  # or 'cloth'
    "name": "00891_00.jpg"
}

Response:
{
    "similar": ["similar1.jpg", "similar2.jpg", ...]
}
```

### AR Overlay API
```python
POST /api/ar/overlay
Content-Type: application/json

{
    "frame": "data:image/jpeg;base64,...",
    "cloth": "shirt.jpg",
    "keypoints": {...}
}

Response:
{
    "frame": "data:image/jpeg;base64,..."
}
```

## 🛠 Technologies

### Deep Learning
- **PyTorch** - Deep learning framework
- **VITON-HD** - Virtual try-on architecture
  - Segmentation Network (U-Net)
  - Geometric Matching Module (TPS)
  - ALIAS Generator (GANs)
- **kornia** - Computer vision library (replaces deprecated torchgeometry)

### Computer Vision
- **OpenCV** - Image processing
- **MediaPipe** - Real-time pose detection (33 landmarks)
- **Pillow (PIL)** - Image manipulation
- **Haar Cascade** - Face detection

### Color Science
- **CIE Lab Color Space** - Perceptually uniform colors
- **HSV Color Space** - Skin detection
- **ITA° Algorithm** - Skin tone classification
- **Color Histograms** - Feature extraction

### Web Framework
- **Flask** - Python web framework
- **Jinja2** - HTML templating
- **HTML5 Canvas** - 2D graphics rendering
- **WebRTC** - Camera access

### Machine Learning
- **scikit-learn** - Cosine similarity, feature matching
- **NumPy** - Numerical computing

## 📁 Project Structure

```
virtual-ar-try-on/
├── VITON-HD/                      # Core VITON-HD model
│   ├── datasets/                  # Dataset directory
│   │   └── test/
│   │       ├── image/            # Person images
│   │       ├── cloth/            # Clothing items
│   │       ├── openpose-json/    # Pose keypoints
│   │       └── image-parse/      # Segmentation masks
│   ├── checkpoints/              # Pre-trained models
│   │   ├── seg_final.pth
│   │   ├── gmm_final.pth
│   │   └── alias_final.pth
│   ├── results/                  # Generated try-on results
│   ├── networks.py               # Neural network architectures
│   ├── test.py                   # Inference script
│   └── datasets.py               # Data loading
│
├── web/                          # Flask web application
│   ├── templates/
│   │   ├── index.html           # Main interface
│   │   ├── ar_tryon.html        # AR try-on page
│   │   ├── add_clothing.html    # 2D clothing manager
│   │   └── result.html          # Result display
│   └── app.py                   # Flask routes and API
│
├── skin_tone_classification/     # Skin tone analysis results
│   ├── skin_tone_classification.json
│   ├── SKIN_TONE_REPORT.md
│   ├── light/                   # Light skin images
│   ├── intermediate/            # Intermediate skin images
│   ├── tan/                     # Tan skin images
│   └── brown/                   # Brown skin images
│
├── classify_skin_tone.py         # Skin tone classifier
├── generate_keypoints.py         # OpenPose keypoint generator
├── download_dataset.py           # Dataset downloader
├── add_nike_shirt.py            # Add clothing script
│
└── Documentation/
    ├── 2D_CLOTHING_ADDITION_GUIDE.md
    ├── AR_TRYON_GUIDE.md
    ├── SKIN_TONE_CLASSIFICATION_GUIDE.md
    ├── BACKGROUND_REMOVAL_GUIDE.md
    └── SHOULDER_ALIGNMENT_FIX.md
```

## 🧪 Skin Tone Classification

### Scientific Method: ITA° (Individual Typology Angle)

**Formula**:
```
ITA° = [arctan((L* - 50) / b*)] × (180 / π)

Where:
- L* = Lightness in Lab color space (0-100)
- b* = Blue-Yellow axis in Lab color space
```

### Categories (Chardon et al., 1991)

| Category | ITA° Range | Description |
|----------|-----------|-------------|
| Very Light | 55° to 90° | Very fair skin |
| Light | 41° to 55° | Fair skin |
| Intermediate | 28° to 41° | Light brown skin |
| Tan | 10° to 28° | Medium brown skin |
| Brown | -30° to 10° | Dark brown skin |
| Dark | -90° to -30° | Very dark skin |

### Processing Pipeline
```
Person Image
    ↓
Face Detection (Haar Cascade)
    ↓
Skin Segmentation (HSV masking)
    ↓
Color Analysis (BGR → Lab)
    ↓
ITA° Calculation (arctan formula)
    ↓
Category Classification
    ↓
Results: JSON + Report + Organized folders
```

### Usage
```bash
python classify_skin_tone.py
```

**Output**:
- Detailed JSON with ITA° values for each image
- Markdown report with statistics
- Images organized in category directories
- Visual distribution chart in console

## 🎨 VITON-HD Architecture

### 1. Segmentation Network
- **Architecture**: U-Net based
- **Input**: Person image
- **Output**: 14-channel segmentation map
- **Purpose**: Parse body parts for agnostic representation

### 2. Geometric Matching Module (GMM)
- **Architecture**: Thin-Plate Spline (TPS) warping
- **Input**: Clothing + Agnostic person
- **Output**: Warped clothing aligned to pose
- **Purpose**: Initial clothing alignment

### 3. ALIAS Generator
- **Architecture**: U-Net with attention + normalization
- **Input**: Warped clothing + Person features
- **Output**: Final photorealistic try-on result
- **Purpose**: High-fidelity synthesis with details

### Training Data
- **VITON-HD Dataset**: 11,647 front-view woman and top clothing image pairs
- **Resolution**: 1024×768
- **Annotations**: OpenPose keypoints, DensePose, segmentation masks

## 🌟 Advanced Features

### White Background Removal
**Algorithm**: RGB threshold detection
```python
if r > 240 and g > 240 and b > 240:
    alpha = 0  # Make transparent
```

**Applied in**:
- Upload tool (`remove_white_background()`)
- AR try-on real-time (`drawClothImage()`)

### Color-Based Recommendations
**Method**: Color histogram matching
- Extract 24-dimensional RGB vectors (8 bins per channel)
- Compute cosine similarity between person and clothes
- Rank by similarity score
- Return top-k recommendations

### Pose-Based AR Alignment
**MediaPipe Landmarks Used**:
- Shoulder (11, 12): Clothing width
- Neck (0): Clothing top position
- Hips (23, 24): Clothing length
- Dynamic scaling based on shoulder span

## 🔒 Privacy & Ethics

### Data Privacy
- All processing happens locally
- No data sent to external servers
- AR frames not stored unless user captures
- User controls all image data

### Inclusive AI
- Skin tone classification for fairness testing
- Diverse dataset representation
- Filter by skin tone for balanced testing
- Scientific dermatological standards (ITA°)

### Responsible Use
- Intended for fashion e-commerce and personal use
- Not for deceptive purposes
- Respect copyright of clothing designs
- Follow ethical AI guidelines

## 🐛 Troubleshooting

### CUDA Out of Memory
```bash
# Use CPU mode
export CUDA_VISIBLE_DEVICES=""
```

### Missing Checkpoints
Download from official VITON-HD repository and place in `VITON-HD/checkpoints/`

### Skin Tone Filter Not Working
```bash
# Run classification first
python classify_skin_tone.py
```

### AR Try-On Camera Not Working
- Allow camera permissions in browser
- Use HTTPS or localhost
- Check browser compatibility (Chrome/Firefox recommended)

## 📚 Documentation

- **[2D Clothing Addition Guide](2D_CLOTHING_ADDITION_GUIDE.md)** - Add new garments
- **[AR Try-On Guide](AR_TRYON_GUIDE.md)** - Real-time AR features
- **[Skin Tone Classification Guide](SKIN_TONE_CLASSIFICATION_GUIDE.md)** - ITA° system
- **[Background Removal Guide](BACKGROUND_REMOVAL_GUIDE.md)** - Clean overlays
- **[Shoulder Alignment Fix](SHOULDER_ALIGNMENT_FIX.md)** - AR alignment

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is based on VITON-HD. Please refer to the original [VITON-HD repository](https://github.com/shadow2496/VITON-HD) for license information.

## 🙏 Acknowledgments

- **VITON-HD Team** - Original virtual try-on architecture
- **MediaPipe** - Real-time pose detection
- **OpenCV** - Computer vision tools
- **Chardon et al. (1991)** - ITA° skin tone classification method

## 📧 Contact

**Developer**: Prasad Reddy  
**GitHub**: [@Prasadreddy6363](https://github.com/Prasadreddy6363)  
**Repository**: [virtual-ar-try-on](https://github.com/Prasadreddy6363/virtual-ar-try-on)

## 🌟 Star History

If this project helped you, please consider giving it a ⭐!

---

**Made with ❤️ using AI and Deep Learning**
