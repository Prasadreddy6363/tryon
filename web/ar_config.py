"""
AR Try-On Configuration
Advanced settings for improved accuracy and performance
"""

# Pose Detection Settings - MAXIMUM ACCURACY
POSE_CONFIG = {
    'min_detection_confidence': 0.9,  # MAXIMUM accuracy (was 0.7)
    'min_tracking_confidence': 0.9,   # MAXIMUM stability (was 0.7)
    'model_complexity': 2,             # Heavy model (most accurate)
    'smooth_landmarks': True,          # Enable landmark smoothing
    'enable_segmentation': True,       # Enable person segmentation
    'smooth_segmentation': True,       # Smooth segmentation mask
}

# Overlay Settings - MAXIMUM ACCURACY
OVERLAY_CONFIG = {
    'base_alpha': 0.85,               # More opaque for better visibility (was 0.7)
    'adaptive_alpha': True,           # Adjust alpha based on confidence
    'feather_edges': True,            # Smooth edge blending
    'feather_size_ratio': 0.15,       # Larger feather for smoother blend (was 0.1)
    'rotation_compensation': True,    # Compensate for body rotation
    'min_rotation_threshold': 0.05,   # More sensitive rotation detection (was 0.1)
    'perspective_correction': True,   # Apply perspective transformation
}

# Body Measurements - MAXIMUM ACCURACY
BODY_CONFIG = {
    'shoulder_width_multiplier': 1.5,  # Better fit (was 1.4)
    'torso_height_multiplier': 1.4,    # Better coverage (was 1.3)
    'neck_offset_ratio': 0.18,         # Better neck positioning (was 0.15)
    'min_cloth_width': 120,            # Larger minimum for better quality (was 100)
    'min_cloth_height': 180,           # Larger minimum for better quality (was 150)
    'max_cloth_width': 1000,           # Larger maximum (was 800)
    'max_cloth_height': 1200,          # Larger maximum (was 1000)
}

# Keypoint Validation - MAXIMUM ACCURACY
KEYPOINT_CONFIG = {
    'min_visibility': 0.75,            # Stricter visibility threshold (was 0.6)
    'required_keypoints': [            # Required keypoints for overlay
        11,  # Left shoulder
        12,  # Right shoulder
        23,  # Left hip
        24,  # Right hip
    ],
    'optional_keypoints': [            # Optional for enhanced accuracy
        13,  # Left elbow
        14,  # Right elbow
        0,   # Nose
        15,  # Left wrist
        16,  # Right wrist
    ],
    'use_temporal_smoothing': True,    # Smooth keypoints over time
    'smoothing_window': 7,             # More smoothing frames (was 5)
}

# Performance Settings
PERFORMANCE_CONFIG = {
    'target_fps': 30,                  # Target frame rate
    'resize_input': True,              # Resize input for faster processing
    'input_width': 640,                # Input width for processing
    'input_height': 480,               # Input height for processing
    'use_gpu': True,                   # Use GPU if available
    'enable_caching': True,            # Cache processed cloth images
}

# Visual Enhancements - MAXIMUM ACCURACY
VISUAL_CONFIG = {
    'color_correction': True,          # Match cloth colors to lighting
    'brightness_adaptation': True,     # Adapt to frame brightness
    'contrast_enhancement': 1.15,      # More contrast for better visibility (was 1.1)
    'sharpness_enhancement': 1.1,      # Sharper cloth details (was 1.05)
    'shadow_simulation': False,        # Add realistic shadows (experimental)
    'wrinkle_simulation': False,       # Add cloth wrinkles (experimental)
}

# Debug Settings
DEBUG_CONFIG = {
    'show_keypoints': False,           # Draw keypoints on frame
    'show_skeleton': False,            # Draw skeleton lines
    'show_bounding_box': False,        # Draw cloth bounding box
    'show_fps': True,                  # Display FPS counter
    'log_performance': False,          # Log performance metrics
    'save_debug_frames': False,        # Save frames for debugging
}

# Cloth Processing
CLOTH_CONFIG = {
    'remove_background': True,         # Remove cloth background
    'background_threshold': 240,       # White background threshold
    'auto_crop': True,                 # Auto-crop cloth to content
    'padding_ratio': 0.05,             # Padding around cropped cloth
    'interpolation': 'lanczos',        # Resize interpolation method
}

def get_config():
    """Get complete AR configuration"""
    return {
        'pose': POSE_CONFIG,
        'overlay': OVERLAY_CONFIG,
        'body': BODY_CONFIG,
        'keypoint': KEYPOINT_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'visual': VISUAL_CONFIG,
        'debug': DEBUG_CONFIG,
        'cloth': CLOTH_CONFIG,
    }

def get_pose_config():
    """Get MediaPipe Pose configuration"""
    return POSE_CONFIG

def get_overlay_config():
    """Get overlay configuration"""
    return OVERLAY_CONFIG

def get_body_config():
    """Get body measurement configuration"""
    return BODY_CONFIG

def update_config(category, key, value):
    """
    Update a configuration value
    
    Args:
        category: Configuration category (pose, overlay, body, etc.)
        key: Configuration key
        value: New value
    """
    config_map = {
        'pose': POSE_CONFIG,
        'overlay': OVERLAY_CONFIG,
        'body': BODY_CONFIG,
        'keypoint': KEYPOINT_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'visual': VISUAL_CONFIG,
        'debug': DEBUG_CONFIG,
        'cloth': CLOTH_CONFIG,
    }
    
    if category in config_map and key in config_map[category]:
        config_map[category][key] = value
        return True
    return False

# Preset configurations for different use cases
PRESETS = {
    'high_accuracy': {
        'pose': {'model_complexity': 2, 'min_detection_confidence': 0.8},
        'overlay': {'base_alpha': 0.75, 'feather_size_ratio': 0.12},
        'performance': {'target_fps': 24, 'input_width': 800, 'input_height': 600},
    },
    'balanced': {
        'pose': {'model_complexity': 1, 'min_detection_confidence': 0.7},
        'overlay': {'base_alpha': 0.7, 'feather_size_ratio': 0.1},
        'performance': {'target_fps': 30, 'input_width': 640, 'input_height': 480},
    },
    'high_performance': {
        'pose': {'model_complexity': 0, 'min_detection_confidence': 0.6},
        'overlay': {'base_alpha': 0.65, 'feather_size_ratio': 0.08},
        'performance': {'target_fps': 60, 'input_width': 480, 'input_height': 360},
    },
}

def apply_preset(preset_name):
    """
    Apply a configuration preset
    
    Args:
        preset_name: Name of preset (high_accuracy, balanced, high_performance)
    """
    if preset_name not in PRESETS:
        return False
    
    preset = PRESETS[preset_name]
    for category, settings in preset.items():
        for key, value in settings.items():
            update_config(category, key, value)
    
    return True
