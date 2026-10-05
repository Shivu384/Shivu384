"""Prep a photo for ASCII conversion: remove bg -> CLAHE contrast -> white background.
Usage: python scripts/prep_photo.py source-photo.jpg   (writes source-prepped.png)
"""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "source-photo.jpg")

cut = remove(Image.open(src).convert("RGB")).convert("RGBA")   # subject with alpha
alpha = np.array(cut)[:, :, 3]
gray = cv2.cvtColor(np.array(cut.convert("RGB")), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)

a = alpha.astype(np.float32) / 255.0
out = (gray * a + 255 * (1 - a)).astype(np.uint8)              # composite on pure white

ys, xs = np.where(alpha > 20)                                  # crop tight to subject
pad = 12
out = out[max(ys.min() - pad, 0): ys.max() + pad, max(xs.min() - pad, 0): xs.max() + pad]
Image.fromarray(out).save(ROOT / "source-prepped.png")
print("wrote source-prepped.png")
