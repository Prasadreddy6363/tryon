# Virtual AR Try-On System

## Overview
This is an advanced Virtual Try-On system based on VITON-HD that enables users to visualize clothing on themselves using AI. The system includes both 2D virtual try-on and AR live try-on capabilities.

## Features
- **2D Virtual Try-On**: Traditional image-based virtual try-on using VITON-HD
- **AR Live Try-On**: Real-time augmented reality try-on using webcam feed
- **Enhanced Keypoint Detection**: Improved body landmark detection including elbow keypoints for better sleeve positioning
- **AI-Powered Recommendations**: Smart clothing recommendations based on color matching
- **Skin Tone Classification**: Automatic skin tone detection and categorization
- **Shopping Integration**: Integration with Myntra and Ajio for purchasing options
- **Real-time Processing**: Live camera feed with real-time clothing overlay

## Technologies Used
- Python Flask for web framework
- MediaPipe for pose estimation
- OpenCV for image processing
- TensorFlow/PyTorch for deep learning models
- HTML5 Canvas for AR rendering
- JavaScript for frontend functionality

## Setup Instructions

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the VITON-HD model:
   - Download the pre-trained models
   - Place them in the checkpoints directory
4. Run the application:
   ```bash
   python web/app.py
   ```

## Enhanced Elbow Keypoints
The system now includes enhanced elbow keypoints (landmarks 13 and 14) and wrist keypoints (landmarks 15 and 16) for better:
- Sleeve positioning and alignment
- Arm tracking accuracy
- Real-time clothing overlay precision
- Improved shoulder-to-wrist connection visualization

## Usage
1. Access the application at `http://localhost:5000`
2. Select the AR Try-On option for real-time experience
3. Choose a clothing item from the gallery
4. Allow camera access when prompted
5. See the clothing overlay on your live feed

## Project Structure
- `web/` - Flask application and web interface
- `VITON-HD/` - Core VITON-HD model implementation
- `datasets/` - Test datasets and keypoints
- `skin_tone_classification/` - Skin tone analysis module