#!/usr/bin/env python3
"""
Create circular avatar from image with border and shadow effect
"""
from PIL import Image, ImageDraw, ImageFilter
import os

# Create directories if needed
os.makedirs('assets/images', exist_ok=True)

# For now, we'll create a placeholder avatar with initials
# In production, you would load an actual image file

def create_avatar_with_initials(name="IF", size=300, bg_color=(31, 41, 55), text_color=(255, 255, 255)):
    """Create a circular avatar with initials"""
    # Create image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add gradient effect (simple)
    for i in range(size):
        color_value = int(31 + (60 - 31) * (i / size))
        draw.line([(0, i), (size, i)], fill=(color_value, color_value + 10, color_value + 24))
    
    # Add border
    border_width = 4
    draw.ellipse(
        [0, 0, size - 1, size - 1],
        outline=(76, 175, 80, 255),
        width=border_width
    )
    
    # Add text (initials)
    draw.text(
        (size // 2, size // 2),
        name,
        fill=text_color,
        anchor='mm',
        font=None  # Uses default font
    )
    
    # Apply slight blur for smooth effect
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Save
    img.save('assets/images/ianara-avatar.png')
    print("✓ Avatar created: assets/images/ianara-avatar.png")

if __name__ == '__main__':
    create_avatar_with_initials('IF')
