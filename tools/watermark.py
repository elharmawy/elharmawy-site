"""Burn the HBC watermark into site images. Usage: python3 tools/watermark.py
Records every processed file in img/watermarked.json so images are never stamped twice."""
import json, hashlib, glob, os, math
from PIL import Image, ImageDraw, ImageFont, ImageStat
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'img', 'watermarked.json')
TARGETS = ['img/res/*.jpg', 'img/svc/*.jpg', 'img/ai/*.jpg', 'founder.jpg', 'og-image.png']
ALREADY = {'img/res/offer_ar.jpg', 'img/res/offer_en.jpg', 'img/res/approval_ar.jpg', 'img/res/approval_en.jpg'}  # made with the watermark built in
FONT = next((f for f in ['/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', '/usr/share/fonts/opentype/inter/Inter-Bold.otf'] + glob.glob('/usr/share/fonts/**/*Bold*.ttf', recursive=True) if os.path.exists(f)), None)
mark = Image.open(os.path.join(ROOT, 'intro-mark.png')).convert('RGBA')
def sha(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()
def stamp(path):
    im = Image.open(path); fmt = im.format; im = im.convert('RGBA'); W, H = im.size
    dark = ImageStat.Stat(im.convert('L')).mean[0] < 128
    ink = (255, 255, 255) if dark else (1, 31, 67)
    layer = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    fs = max(14, int(min(W, H) * 0.026)); f = ImageFont.truetype(FONT, fs) if FONT else ImageFont.load_default()
    txt = 'HBC · ELHARMAWY.COM'; tw = d.textlength(txt, font=f); gx, gy = int(tw * 1.6), int(fs * 5.5)
    for y in range(0, H * 2, gy):
        for x in range(-(y // gy % 2) * gx // 2, W * 2, gx):
            d.text((x, y), txt, font=f, fill=ink + (int(255 * (0.07 if dark else 0.06)),))
    layer = layer.rotate(24, resample=Image.BICUBIC).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
    m = mark.copy(); mw = int(min(W, H) * 0.55); m = m.resize((mw, int(mw * m.height / m.width)), Image.LANCZOS)
    if not dark: m = Image.merge('RGBA', (*[Image.new('L', m.size, c) for c in ink], m.split()[3]))
    alpha = m.split()[3].point(lambda a: int(a * (0.06 if dark else 0.05))); m.putalpha(alpha)
    layer.alpha_composite(m, ((W - m.width) // 2, (H - m.height) // 2))
    out = Image.alpha_composite(im, layer).convert('RGB')
    if path.lower().endswith('.png'): out.save(path, optimize=True)
    else: out.save(path, quality=88, optimize=True, progressive=True)
man = json.load(open(MAN)) if os.path.exists(MAN) else {}
files = sorted({os.path.relpath(p, ROOT) for t in TARGETS for p in glob.glob(os.path.join(ROOT, t))})
n = 0
for rel in files:
    p = os.path.join(ROOT, rel)
    if rel in man and man[rel] == sha(p): continue
    if rel not in ALREADY: stamp(p); n += 1
    man[rel] = sha(p)
json.dump(man, open(MAN, 'w'), indent=1, sort_keys=True)
print('stamped', n, 'of', len(files))
