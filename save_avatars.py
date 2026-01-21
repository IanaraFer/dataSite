"""
Save the avatar images provided by the user.
The images are vector/cartoon style professional avatars.
Since we have them as attachments, we'll note that they need to be manually saved.
"""

import os

# Create directory
os.makedirs('assets/images', exist_ok=True)

print("""
╔════════════════════════════════════════════════════════╗
║         Avatar Images Ready to Save                     ║
╚════════════════════════════════════════════════════════╝

INSTRUCTIONS:
You have provided two professional avatar images:

1. Business professional avatar (navy blazer) - RECOMMENDED
   Save as: assets/images/ianara-avatar.jpg
   
2. Casual avatar (floral top) - ALTERNATIVE
   Save as: assets/images/ianara-avatar-casual.jpg

TO COMPLETE SETUP:
1. Right-click the first avatar image (navy blazer)
2. Save as: assets/images/ianara-avatar.jpg
3. Run: git add -A
4. Run: git commit -m "Add Ianara professional avatar"
5. Run: git push origin main

The website will automatically display it in the About section!
""")

# Create a placeholder README
with open('assets/images/README.md', 'w') as f:
    f.write("""# Avatar Images

## Current Avatar
- `ianara-avatar.jpg` - Professional business avatar (navy blazer)
- Displayed on: About section, circular frame with green border

## Specifications
- Size: 240px × 240px circular display
- Border: 6px solid green (#2ca02c)
- Format: JPG or PNG
- Auto-centered and responsive

## Update Avatar
Replace `ianara-avatar.jpg` with a new image and push to GitHub.
""")

print("✓ README created in assets/images/")
print("✓ Ready to save your avatar images!")
