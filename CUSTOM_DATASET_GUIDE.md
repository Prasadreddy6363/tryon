# 📁 Custom Dataset Guide for Instant Try-On

## 🎯 Overview

You can configure the Instant Try-On feature to use different datasets, specific images, or custom folders.

---

## 🔧 Configuration File

Location: `web/instant_tryon_config.py`

This file controls:
- Which person images to show
- Which clothing images to show
- Display settings
- Processing options

---

## 📝 Basic Configuration

### Option 1: Use Specific Images Only

Edit `web/instant_tryon_config.py`:

```python
# Show only these person images
INSTANT_TRYON_CONFIG['person_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    '00055_00.jpg',
    '00069_00.jpg',
]

# Show only these clothing images
INSTANT_TRYON_CONFIG['cloth_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    '00055_00.jpg',
]
```

### Option 2: Limit Number of Images

```python
# Show only first 50 person images
INSTANT_TRYON_CONFIG['person_dataset']['limit'] = 50

# Show only first 30 clothing images
INSTANT_TRYON_CONFIG['cloth_dataset']['limit'] = 30
```

### Option 3: Use Different Folder

```python
# Use custom person images folder
INSTANT_TRYON_CONFIG['person_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'people'

# Use custom clothing folder
INSTANT_TRYON_CONFIG['cloth_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'clothes'
```

---

## 📂 Creating Custom Dataset

### Step 1: Create Folder Structure

```
VITON-HD/
└── datasets/
    └── custom/
        ├── people/          # Your person images
        │   ├── person1.jpg
        │   ├── person2.jpg
        │   └── ...
        └── clothes/         # Your clothing images
            ├── shirt1.jpg
            ├── shirt2.jpg
            └── ...
```

### Step 2: Prepare Images

**Person Images:**
- **Resolution**: 768x1024 (recommended)
- **Format**: JPG
- **Pose**: Front-facing
- **Background**: Clean, plain
- **Lighting**: Even, well-lit

**Clothing Images:**
- **Resolution**: 768x1024 (recommended)
- **Format**: JPG
- **Background**: White or transparent
- **Orientation**: Flat lay or front view
- **Quality**: High detail

### Step 3: Update Configuration

Edit `web/instant_tryon_config.py`:

```python
INSTANT_TRYON_CONFIG['person_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'people'
INSTANT_TRYON_CONFIG['cloth_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'clothes'
```

### Step 4: Restart Server

```bash
# Stop server (Ctrl+C)
# Start server
cd web
python app.py
```

---

## 🎨 Display Settings

### Change Grid Layout

```python
# Show 3 columns instead of 2
INSTANT_TRYON_CONFIG['display']['grid_columns'] = 3

# Show 100 items per page instead of 50
INSTANT_TRYON_CONFIG['display']['items_per_page'] = 100
```

### Change Aspect Ratios

```python
# Use square images
INSTANT_TRYON_CONFIG['display']['person_aspect_ratio'] = '1/1'
INSTANT_TRYON_CONFIG['display']['cloth_aspect_ratio'] = '1/1'

# Use wide images
INSTANT_TRYON_CONFIG['display']['person_aspect_ratio'] = '16/9'
```

---

## ⚙️ Processing Settings

### Disable AI Processing (Simple Overlay)

```python
# Use simple overlay instead of AI
INSTANT_TRYON_CONFIG['processing']['use_ai'] = False
```

### Adjust Timeout

```python
# Wait longer for AI processing
INSTANT_TRYON_CONFIG['processing']['timeout'] = 120  # 2 minutes
```

---

## 📋 Example Configurations

### Example 1: High-Quality Curated Set

```python
# Use only best quality images
INSTANT_TRYON_CONFIG['person_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    '00055_00.jpg',
    '00069_00.jpg',
    '00077_00.jpg',
    '00091_00.jpg',
    '00101_00.jpg',
]

INSTANT_TRYON_CONFIG['cloth_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    '00055_00.jpg',
    '00067_00.jpg',
]

INSTANT_TRYON_CONFIG['display']['grid_columns'] = 2
INSTANT_TRYON_CONFIG['display']['items_per_page'] = 20
```

### Example 2: Large Catalog

```python
# Show many items
INSTANT_TRYON_CONFIG['person_dataset']['limit'] = 200
INSTANT_TRYON_CONFIG['cloth_dataset']['limit'] = 500

INSTANT_TRYON_CONFIG['display']['grid_columns'] = 3
INSTANT_TRYON_CONFIG['display']['items_per_page'] = 100
```

### Example 3: Custom Dataset

```python
# Use completely custom images
INSTANT_TRYON_CONFIG['person_dataset']['path'] = VITON_DIR / 'datasets' / 'my_models'
INSTANT_TRYON_CONFIG['cloth_dataset']['path'] = VITON_DIR / 'datasets' / 'my_clothes'

INSTANT_TRYON_CONFIG['person_dataset']['limit'] = None  # Show all
INSTANT_TRYON_CONFIG['cloth_dataset']['limit'] = None  # Show all
```

---

## 🔍 Image Requirements

### For AI Processing to Work:

Person images need preprocessing:
1. **OpenPose keypoints** - Body pose detection
2. **Segmentation masks** - Body part identification
3. **Agnostic representation** - Clothing-independent version

**To generate preprocessing:**
```bash
python generate_keypoints.py
```

### For Simple Overlay (No AI):

```python
# Disable AI processing
INSTANT_TRYON_CONFIG['processing']['use_ai'] = False
```

No preprocessing needed, but results will be simple overlays.

---

## 📊 Recommended Settings

### For Best Quality:

```python
INSTANT_TRYON_CONFIG = {
    'person_dataset': {
        'path': VITON_DIR / 'datasets' / 'test' / 'image',
        'format': '.jpg',
        'limit': 50,  # Curated selection
        'filter': [
            # List your best quality images
            '00008_00.jpg',
            '00013_00.jpg',
            # ... more
        ],
    },
    'cloth_dataset': {
        'path': VITON_DIR / 'datasets' / 'test' / 'cloth',
        'format': '.jpg',
        'limit': 50,
        'filter': [
            # List your best clothing items
            '00008_00.jpg',
            '00013_00.jpg',
            # ... more
        ],
    },
    'display': {
        'person_aspect_ratio': '3/4',
        'cloth_aspect_ratio': '3/4',
        'grid_columns': 2,
        'items_per_page': 50,
    },
    'processing': {
        'use_ai': True,
        'timeout': 60,
        'quality': 'high',
    }
}
```

### For Fast Browsing:

```python
INSTANT_TRYON_CONFIG['processing']['use_ai'] = False  # Simple overlay
INSTANT_TRYON_CONFIG['display']['grid_columns'] = 3  # More items visible
INSTANT_TRYON_CONFIG['display']['items_per_page'] = 100  # Show more
```

---

## 🛠️ Troubleshooting

### Images Not Showing?

**Check paths:**
```python
from instant_tryon_config import get_person_path, get_cloth_path
print(get_person_path())
print(get_cloth_path())
```

**Verify files exist:**
```bash
dir VITON-HD\datasets\test\image
dir VITON-HD\datasets\test\cloth
```

### AI Processing Fails?

**Ensure preprocessing exists:**
- Check `VITON-HD/datasets/test/openpose-json/`
- Check `VITON-HD/datasets/test/image-parse/`
- Run: `python generate_keypoints.py`

### Wrong Images Showing?

**Clear filter:**
```python
INSTANT_TRYON_CONFIG['person_dataset']['filter'] = None
INSTANT_TRYON_CONFIG['cloth_dataset']['filter'] = None
```

**Restart server:**
```bash
cd web
python app.py
```

---

## 📝 Quick Start Examples

### Use Only 10 Best Images:

1. Edit `web/instant_tryon_config.py`
2. Uncomment the filter section
3. Add your image filenames
4. Restart server

### Use Custom Folder:

1. Create folder: `VITON-HD/datasets/custom/`
2. Add subfolders: `people/` and `clothes/`
3. Copy your images there
4. Update config paths
5. Restart server

### Show More Items:

1. Edit `web/instant_tryon_config.py`
2. Change `limit` to higher number
3. Change `items_per_page` to 100
4. Restart server

---

## ✅ Verification

After configuration:

1. **Restart server**
2. **Open**: http://127.0.0.1:5000/instant_tryon
3. **Check**: Right panel shows your images
4. **Verify**: Correct number of items
5. **Test**: Click to try on

---

## 🎉 Summary

**Configuration file**: `web/instant_tryon_config.py`

**Main options:**
- `filter` - Use specific images only
- `limit` - Limit number of images
- `path` - Use different folder
- `grid_columns` - Change layout
- `use_ai` - Enable/disable AI processing

**After changes:**
- Always restart server
- Refresh browser page
- Check console for errors

---

**Customize your instant try-on experience! 🚀**
