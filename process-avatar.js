const fs = require('fs');
const path = require('path');

// This script will help process and convert avatar images
// Usage: node process-avatar.js <source-image> <output-name>

console.log(`
╔════════════════════════════════════════════════════════╗
║         Avatar Image Processing Tool                   ║
╚════════════════════════════════════════════════════════╝

To use this tool, you'll need to:

1. Install sharp (image processing library):
   npm install sharp

2. Place your image in the workspace root

3. Run: node process-avatar.js <image-file>

For now, manually save your photo as:
  assets/images/ianara-avatar.jpg

Then commit and push:
  git add -A
  git commit -m "Add Ianara avatar"
  git push origin main

Your About section will display the circular avatar automatically.
`);
