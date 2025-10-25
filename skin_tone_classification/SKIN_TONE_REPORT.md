# Skin Tone Classification Report

## Overview

- **Total Images**: 2032
- **Successfully Classified**: 1901
- **Failed**: 131

## Classification Method

**Algorithm**: ITA° (Individual Typology Angle)

**Formula**: `ITA° = [arctan((L* - 50)/b*)] × (180/π)`

Where:
- `L*` = Lightness in Lab color space (0-100)
- `b*` = Blue-Yellow axis in Lab color space

**Reference**: Chardon et al., 1991 - Standard dermatological classification

## Skin Tone Categories

| Category | ITA° Range | Description | Count | Percentage |
|----------|-----------|-------------|-------|------------|
| Very Light | 55° to 90° | Very fair skin | 0 | 0.0% |
| Light | 41° to 55° | Fair skin | 181 | 9.5% |
| Intermediate | 28° to 41° | Light brown skin | 1486 | 78.2% |
| Tan | 10° to 28° | Medium brown skin | 233 | 12.3% |
| Brown | -30° to 10° | Dark brown skin | 1 | 0.1% |
| Dark | -90° to -30° | Very dark skin | 0 | 0.0% |

## File Organization

Images have been organized into directories by skin tone:

- `light/`: 181 images
- `intermediate/`: 1486 images
- `tan/`: 233 images
- `brown/`: 1 images
- `unknown/`: 131 images (face/skin not detected)

## Technical Details

### Face Detection
- **Algorithm**: Haar Cascade (OpenCV)
- **Classifier**: Frontal Face Default
- **Parameters**: scaleFactor=1.1, minNeighbors=5

### Skin Detection
- **Color Space**: HSV
- **Skin Range**: H[0-20], S[20-255], V[70-255]
- **Morphology**: Closing + Opening with 5x5 elliptical kernel

### Color Analysis
- **Color Space**: CIE Lab (perceptually uniform)
- **Measurement**: Average L* and b* from skin pixels
- **Classification**: ITA° angle-based categorization

