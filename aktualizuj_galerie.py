import os
import re
from PIL import Image, ImageOps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_DIR = os.path.join(BASE_DIR, 'pic')
THUMBS_DIR = os.path.join(PIC_DIR, 'thumbs')
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

os.makedirs(THUMBS_DIR, exist_ok=True)

# Files that belong to website background or icons (not gallery)
EXCLUDED_NAMES = {
    '1.jpg', '2.jpg', '3.jpg',
    '1_web.jpg', '2_web.jpg', '3_web.jpg',
    'rings-2.png', 'champagne-4.png', 'bed-4.png'
}
EXCLUDED_LOWER = {name.lower() for name in EXCLUDED_NAMES}

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')

# 1. Automatycznie twórz brakujące miniaturki dla nowych zdjęć w pic/
for f in os.listdir(PIC_DIR):
    if f.lower() in EXCLUDED_LOWER or f.startswith(('1_web', '2_web', '3_web')):
        continue
    if not f.lower().endswith(valid_extensions):
        continue

    full_path = os.path.join(PIC_DIR, f)
    if os.path.isdir(full_path):
        continue

    thumb_path = os.path.join(THUMBS_DIR, f)
    if not os.path.exists(thumb_path):
        try:
            print(f"Tworzenie miniaturki dla: {f}")
            im = Image.open(full_path)
            im = ImageOps.exif_transpose(im)
            im.thumbnail((800, 800), Image.LANCZOS)
            im.save(thumb_path, quality=80)
        except Exception as e:
            print(f"Błąd przy {f}: {e}")

# 2. Zbieraj tylko te zdjęcia, których miniaturka i pełny plik istnieją
gallery_items = []
for f in sorted(os.listdir(THUMBS_DIR)):
    if f.lower() in EXCLUDED_LOWER or f.startswith(('1_web', '2_web', '3_web')):
        continue
    if not f.lower().endswith(valid_extensions):
        continue

    full_path = os.path.join(PIC_DIR, f)
    if os.path.exists(full_path):
        gallery_items.append(f"            {{ thumb: 'pic/thumbs/{f}', full: 'pic/{f}' }}")

print(f"Znaleziono {len(gallery_items)} aktywnych zdjęć w galerii.")

# 3. Zaktualizuj listę w index.html
with open(INDEX_PATH, 'r', encoding='utf-8') as file:
    content = file.read()

new_gallery_js = "const galleryImages = [\n" + ",\n".join(gallery_items) + "\n        ];"
pattern = r"const galleryImages = \[\s*[\s\S]*?\];"
updated_content = re.sub(pattern, new_gallery_js, content)

with open(INDEX_PATH, 'w', encoding='utf-8') as file:
    file.write(updated_content)

print("Pomyślnie zaktualizowano listę zdjęć w index.html!")
