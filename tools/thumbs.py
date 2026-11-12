"""Make light WebP previews (540px wide) of the watermarked gallery posts: img/res/t/<name>.webp.
Previews are cut from the already-watermarked originals, so they carry the watermark; they are recorded in img/watermarked.json."""
import glob, os, json, hashlib
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'img', 'watermarked.json'); man = json.load(open(MAN))
os.makedirs(os.path.join(ROOT, 'img/res/t'), exist_ok=True)
for p in sorted(glob.glob(os.path.join(ROOT, 'img/res/*.jpg'))):
    rel = os.path.relpath(p, ROOT); assert rel in man, rel + ' is not watermarked yet: run tools/watermark.py first'
    out = os.path.join(ROOT, 'img/res/t', os.path.basename(p)[:-4] + '.webp')
    im = Image.open(p).convert('RGB'); im = im.resize((540, round(540 * im.height / im.width)), Image.LANCZOS)
    im.save(out, 'WEBP', quality=78, method=6)
    man[os.path.relpath(out, ROOT)] = hashlib.sha1(open(out, 'rb').read()).hexdigest()
json.dump(man, open(MAN, 'w'), indent=1, sort_keys=True); print('previews:', len(glob.glob(os.path.join(ROOT, 'img/res/t/*.webp'))))
