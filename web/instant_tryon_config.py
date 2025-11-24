"""
Configuration for Instant Try-On Feature
Allows using different datasets and customization
"""

from pathlib import Path

# Base paths
WORKSPACE = Path(__file__).resolve().parent.parent
VITON_DIR = WORKSPACE / 'VITON-HD'

# Dataset Configuration
# You can change these paths to use different datasets
INSTANT_TRYON_CONFIG = {
    # Person images dataset
    'person_dataset': {
        'path': VITON_DIR / 'datasets' / 'test' / 'image',
        'format': '.jpg',
        'limit': 100,  # Number of images to show (None for all)
        'filter': None,  # Optional: list of specific filenames to use
    },
    
    # Clothing images dataset
    'cloth_dataset': {
        'path': VITON_DIR / 'datasets' / 'test' / 'cloth',
        'format': '.jpg',
        'limit': 100,  # Number of images to show (None for all)
        'filter': None,  # Optional: list of specific filenames to use
    },
    
    # Display settings
    'display': {
        'person_aspect_ratio': '3/4',  # CSS aspect ratio
        'cloth_aspect_ratio': '3/4',
        'grid_columns': 2,  # Number of columns in clothing grid
        'items_per_page': 50,
    },
    
    # Processing settings
    'processing': {
        'use_ai': True,  # True = AI processing, False = simple overlay
        'timeout': 60,  # Seconds to wait for AI processing
        'quality': 'high',  # 'high', 'medium', 'low'
    }
}

# Alternative dataset configurations
# Uncomment and modify to use different datasets

# Example: Use only specific high-quality images
"""
INSTANT_TRYON_CONFIG['person_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    '00055_00.jpg',
    '00069_00.jpg',
    # Add more filenames here
]

INSTANT_TRYON_CONFIG['cloth_dataset']['filter'] = [
    '00008_00.jpg',
    '00013_00.jpg',
    '00034_00.jpg',
    # Add more filenames here
]
"""

# Example: Use a different dataset folder
"""
INSTANT_TRYON_CONFIG['person_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'people'
INSTANT_TRYON_CONFIG['cloth_dataset']['path'] = VITON_DIR / 'datasets' / 'custom' / 'clothes'
"""

# Example: Show more items
"""
INSTANT_TRYON_CONFIG['display']['items_per_page'] = 100
INSTANT_TRYON_CONFIG['display']['grid_columns'] = 3
"""

def get_config():
    """Get the instant try-on configuration"""
    return INSTANT_TRYON_CONFIG

def get_person_images():
    """Get list of person images based on configuration"""
    config = INSTANT_TRYON_CONFIG['person_dataset']
    path = config['path']
    format_ext = config['format']
    limit = config['limit']
    filter_list = config['filter']
    
    if not path.exists():
        return []
    
    # Get all images
    images = sorted([f.name for f in path.glob(f'*{format_ext}')])
    
    # Apply filter if specified
    if filter_list:
        images = [img for img in images if img in filter_list]
    
    # Apply limit
    if limit:
        images = images[:limit]
    
    return images

def get_cloth_images():
    """Get list of clothing images based on configuration"""
    config = INSTANT_TRYON_CONFIG['cloth_dataset']
    path = config['path']
    format_ext = config['format']
    limit = config['limit']
    filter_list = config['filter']
    
    if not path.exists():
        return []
    
    # Get all images
    images = sorted([f.name for f in path.glob(f'*{format_ext}')])
    
    # Apply filter if specified
    if filter_list:
        images = [img for img in images if img in filter_list]
    
    # Apply limit
    if limit:
        images = images[:limit]
    
    return images

def get_person_path():
    """Get the path to person images"""
    return INSTANT_TRYON_CONFIG['person_dataset']['path']

def get_cloth_path():
    """Get the path to clothing images"""
    return INSTANT_TRYON_CONFIG['cloth_dataset']['path']
