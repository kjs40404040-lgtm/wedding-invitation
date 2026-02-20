"""Wedding invitation image compressor - resize to 1200px width, JPEG 80%"""
from PIL import Image
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')
MAX_WIDTH = 1200
QUALITY = 80

for fname in os.listdir(IMG_DIR):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    fpath = os.path.join(IMG_DIR, fname)
    size_before = os.path.getsize(fpath)
    
    img = Image.open(fpath)
    # Convert RGBA to RGB if needed
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Resize maintaining aspect ratio
    w, h = img.size
    if w > MAX_WIDTH:
        new_h = int(h * MAX_WIDTH / w)
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
    
    # Save with compression
    img.save(fpath, 'JPEG', quality=QUALITY, optimize=True)
    
    size_after = os.path.getsize(fpath)
    reduction = (1 - size_after / size_before) * 100
    print(f"{fname}: {size_before/1024/1024:.1f}MB -> {size_after/1024:.0f}KB ({reduction:.0f}% reduced)")

print("\nDone! All images compressed.")
