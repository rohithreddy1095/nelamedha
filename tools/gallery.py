"""Turns the photos in photos/ into the gallery: two web-sized copies of each (no location or camera data),
and gallery/photos.json listing them newest first. Runs on GitHub whenever photos are added; can also be run by hand.

Name a photo like  2025-06-14 mango flowers.jpg  to give it a date and a caption.
Without a date in the name, the date the camera recorded is used.
"""
import json, os, re, hashlib
from datetime import datetime
from PIL import Image, ImageOps
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = os.path.join(ROOT, 'photos'), os.path.join(ROOT, 'gallery', 'img')
EXT = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif')
SIZES = {'s': 640, 'l': 1800}
os.makedirs(OUT, exist_ok=True)

def taken(im, name):
    m = re.match(r'(\d{4})[-_.]?(\d{2})[-_.]?(\d{2})', name)
    if m:
        try: return datetime(*map(int, m.groups())).date().isoformat()
        except ValueError: pass
    try:
        ex = im.getexif(); v = ex.get_ifd(0x8769).get(36867) or ex.get(306)
        if v: return datetime.strptime(v[:19], '%Y:%m:%d %H:%M:%S').date().isoformat()
    except Exception: pass
    m = re.search(r'(20\d{2})[-_]?(\d{2})[-_]?(\d{2})', name)   # phone names like IMG_20250614_101500 or WhatsApp Image 2025-06-14
    if m:
        try: return datetime(*map(int, m.groups())).date().isoformat()
        except ValueError: pass
    return None

def caption(name):
    c = re.sub(r'^\d{4}[-_.]?\d{2}[-_.]?\d{2}', '', os.path.splitext(name)[0])
    c = re.sub(r'^(IMG|PXL|DSC|VID|WhatsApp Image)[-_ ]?[\d_ .-]*(at[\d. ]*)?', '', c, flags=re.I)
    c = re.sub(r'[_-]+', ' ', c).strip(' .')
    return c[:1].upper() + c[1:] if c else ''

items, keep = [], set()
for name in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
    if not name.lower().endswith(EXT): continue
    path = os.path.join(SRC, name)
    key = hashlib.sha1(open(path, 'rb').read()).hexdigest()[:12]
    try: im = Image.open(path)
    except Exception as e:
        print('skip', name, e); continue
    when = taken(im, name)
    im = ImageOps.exif_transpose(im).convert('RGB')        # turn it the right way up, then drop all metadata
    files = {}
    for k, w in SIZES.items():
        fn = f'{key}-{k}.webp'; files[k] = fn; keep.add(fn)
        out = os.path.join(OUT, fn)
        if not os.path.exists(out):
            c = im.copy(); c.thumbnail((w, w), Image.LANCZOS); c.save(out, 'WEBP', quality=80 if k == 'l' else 74, method=6)
    w, h = im.size
    items.append({'src': files['l'], 'thumb': files['s'], 'date': when, 'caption': caption(name), 'w': w, 'h': h, 'name': name})
    print(name, when, w, h)

for fn in os.listdir(OUT):                                  # photos removed from photos/ leave the gallery too
    if fn.endswith('.webp') and fn not in keep: os.remove(os.path.join(OUT, fn))
items.sort(key=lambda x: (x['date'] or '0000', x['name']), reverse=True)
json.dump({'photos': items}, open(os.path.join(ROOT, 'gallery', 'photos.json'), 'w'), ensure_ascii=False, indent=1)
print(len(items), 'photos')
