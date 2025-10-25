#!/usr/bin/env python3
"""
Generate a test men's shirt image optimized for AR try-on alignment.
This creates a properly formatted shirt with correct proportions.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_mens_shirt(output_path, color='blue', pattern='solid'):
    """
    Create a men's shirt image with proper proportions for AR try-on.
    
    Standard men's shirt dimensions:
    - Width: shoulder span + sleeves (typically 600px for template)
    - Height: collar to waist (typically 800px for template)
    - Aspect ratio: ~3:4 (width:height)
    """
    
    # Standard shirt dimensions optimized for AR overlay
    width = 600
    height = 800
    
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define color schemes
    colors = {
        'blue': (65, 105, 225),      # Royal Blue
        'white': (240, 240, 245),    # Off-white
        'black': (45, 45, 48),       # Dark Gray (not pure black)
        'red': (220, 53, 69),        # Red
        'green': (40, 167, 69),      # Green
        'gray': (108, 117, 125),     # Gray
        'navy': (13, 27, 62),        # Navy Blue
        'burgundy': (128, 0, 32)     # Burgundy
    }
    
    base_color = colors.get(color, colors['blue'])
    
    # ===== SHIRT BODY =====
    # Main shirt rectangle (torso area)
    shirt_body = [
        (50, 100),   # Top left (below collar)
        (550, 100),  # Top right
        (550, 700),  # Bottom right
        (50, 700)    # Bottom left
    ]
    draw.polygon(shirt_body, fill=base_color + (255,))
    
    # ===== COLLAR =====
    # V-neck or round collar area
    collar_points = [
        (250, 80),   # Left collar point
        (300, 150),  # Center V point (deep V)
        (350, 80),   # Right collar point
        (350, 100),  # Right inner
        (300, 130),  # Center inner
        (250, 100)   # Left inner
    ]
    # Collar with slightly lighter shade
    collar_color = tuple(min(c + 20, 255) for c in base_color) + (255,)
    draw.polygon(collar_points, fill=collar_color)
    
    # ===== SLEEVES =====
    # Left sleeve
    left_sleeve = [
        (50, 100),   # Shoulder point
        (0, 200),    # Outer elbow
        (30, 350),   # Lower sleeve
        (80, 300),   # Inner sleeve
        (80, 150)    # Armpit
    ]
    draw.polygon(left_sleeve, fill=base_color + (255,))
    
    # Right sleeve (mirror)
    right_sleeve = [
        (550, 100),  # Shoulder point
        (600, 200),  # Outer elbow
        (570, 350),  # Lower sleeve
        (520, 300),  # Inner sleeve
        (520, 150)   # Armpit
    ]
    draw.polygon(right_sleeve, fill=base_color + (255,))
    
    # ===== DETAILS =====
    # Add subtle shading for depth
    shadow_color = tuple(max(c - 30, 0) for c in base_color) + (128,)
    
    # Left side shadow
    draw.rectangle([50, 150, 100, 700], fill=shadow_color)
    
    # Right side highlight
    highlight_color = tuple(min(c + 30, 255) for c in base_color) + (128,)
    draw.rectangle([500, 150, 550, 700], fill=highlight_color)
    
    # Add buttons (optional detail)
    button_color = (230, 230, 230, 255)
    button_positions = [200, 300, 400, 500, 600]
    for y in button_positions:
        draw.ellipse([290, y-5, 310, y+5], fill=button_color)
    
    # ===== PATTERNS (Optional) =====
    if pattern == 'stripes':
        stripe_color = tuple(max(c - 40, 0) for c in base_color) + (255,)
        for i in range(0, height, 40):
            draw.rectangle([50, i, 550, i+20], fill=stripe_color)
    
    elif pattern == 'checkered':
        check_color = tuple(max(c - 40, 0) for c in base_color) + (255,)
        check_size = 30
        for i in range(50, 550, check_size * 2):
            for j in range(100, 700, check_size * 2):
                draw.rectangle([i, j, i+check_size, j+check_size], fill=check_color)
                draw.rectangle([i+check_size, j+check_size, i+check_size*2, j+check_size*2], fill=check_color)
    
    # ===== OUTLINE for better visibility =====
    draw.polygon(shirt_body, outline=(0, 0, 0, 200), width=2)
    draw.polygon(left_sleeve, outline=(0, 0, 0, 200), width=2)
    draw.polygon(right_sleeve, outline=(0, 0, 0, 200), width=2)
    
    # Convert to RGB (remove alpha for JPG)
    # Create white background
    background = Image.new('RGB', (width, height), (255, 255, 255))
    background.paste(img, (0, 0), img)
    
    # Save the image
    background.save(output_path, 'JPEG', quality=95)
    print(f"✓ Created shirt: {output_path}")
    return output_path


def main():
    """Generate multiple test shirts with different colors and patterns."""
    
    # Create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cloth_dir = os.path.join(script_dir, 'VITON-HD', 'datasets', 'test', 'cloth')
    
    if not os.path.exists(cloth_dir):
        print(f"Error: Cloth directory not found: {cloth_dir}")
        print("Please ensure VITON-HD dataset is properly set up.")
        return
    
    print("Generating test men's shirts optimized for AR alignment...\n")
    
    # Generate various shirt styles
    shirts = [
        ('test_shirt_blue_solid.jpg', 'blue', 'solid'),
        ('test_shirt_white_solid.jpg', 'white', 'solid'),
        ('test_shirt_black_solid.jpg', 'black', 'solid'),
        ('test_shirt_red_solid.jpg', 'red', 'solid'),
        ('test_shirt_navy_stripes.jpg', 'navy', 'stripes'),
        ('test_shirt_gray_checkered.jpg', 'gray', 'checkered'),
    ]
    
    for filename, color, pattern in shirts:
        output_path = os.path.join(cloth_dir, filename)
        create_mens_shirt(output_path, color, pattern)
    
    print(f"\n✓ Successfully generated {len(shirts)} test shirts!")
    print(f"✓ Location: {cloth_dir}")
    print("\nThese shirts are optimized for AR try-on with:")
    print("  - Correct aspect ratio (3:4)")
    print("  - Proper collar positioning")
    print("  - Full shoulder + sleeve coverage")
    print("  - Clear visual boundaries")
    print("\nYou can now select these shirts in the AR try-on interface!")


if __name__ == '__main__':
    main()
