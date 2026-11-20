# -*- coding: utf-8 -*-
import os, shutil
from PIL import Image

DL = r"C:\Users\thoma\Downloads"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logos")
os.makedirs(OUT, exist_ok=True)

def trim(im):
    im = im.convert("RGBA")
    # build a mask of non-(transparent/white) pixels
    px = im.load(); w,h = im.size
    bbox = im.getbbox()  # alpha-based
    # if fully opaque (white bg), bbox by non-white
    if bbox and (bbox == (0,0,w,h)):
        from PIL import Image as I
        bg = I.new("RGBA", im.size, (255,255,255,255))
        diff = I.new("L", im.size, 0)
        dp = diff.load()
        for y in range(h):
            for x in range(w):
                r,g,b,a = px[x,y]
                if a>10 and not (r>245 and g>245 and b>245):
                    dp[x,y]=255
        bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im

# 1) Finning: key yellow bg -> transparent black wordmark
fin = Image.open(os.path.join(DL, "finning logo.png")).convert("RGBA")
px = fin.load(); w,h = fin.size
for y in range(h):
    for x in range(w):
        r,g,b,a = px[x,y]
        mx = max(r,g,b)
        px[x,y] = (40,40,40, int(a*(255-mx)/255))
fin = trim(fin)
fin.save(os.path.join(OUT, "finning.png"))
print("finning", fin.size)

# 2) copy + trim the raster logos
for src, name in [("evora logo.png","evora.png"),
                  ("Schuco-Logo.png","schuco.png"),
                  ("Onbuy-Logo.png","onbuy.png")]:
    im = trim(Image.open(os.path.join(DL, src)))
    im.save(os.path.join(OUT, name))
    print(name, im.size)

# 3) OEM is svg -> copy as-is
shutil.copy(os.path.join(DL, "oemreman-logo.svg"), os.path.join(OUT, "oem.svg"))
print("oem.svg copied")
print("done ->", OUT)
