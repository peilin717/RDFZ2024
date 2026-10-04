from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage

root = Path(__file__).resolve().parents[1]
source = Image.open(root / "assets" / "hero-atlas.png").convert("RGBA")
out = root / "assets" / "heroes"
out.mkdir(parents=True, exist_ok=True)

names = ["haq", "fjy", "zbh", "lzy", "wxy"]
cell = source.width / len(names)

for index, name in enumerate(names):
    # This overlapping atlas cell was repaired as a standalone transparent sprite.
    # Equal-width splitting would restore the clipped sleeve and neighboring hair.
    if name == "lzy":
        print("Preserving repaired lzy.png; see tools/lzy-art-repair.json")
        continue
    left = round(index * cell)
    right = round((index + 1) * cell)
    character = source.crop((left, 0, right, source.height))
    rgba = np.array(character)
    labels, count = ndimage.label(rgba[:, :, 3] > 20)
    keep = np.zeros(labels.shape, dtype=bool)
    for label_id in range(1, count + 1):
        ys, xs = np.where(labels == label_id)
        if len(xs) < 80:
            continue
        center_x = xs.mean() / character.width
        area = len(xs)
        if 0.16 <= center_x <= 0.84 or area > character.width * character.height * 0.08:
            keep |= labels == label_id
    rgba[~keep, 3] = 0
    character = Image.fromarray(rgba, "RGBA")
    alpha_box = character.getchannel("A").getbbox()
    if alpha_box:
        character = character.crop((0, alpha_box[1], character.width, alpha_box[3]))
    canvas = Image.new("RGBA", (512, 1024), (0, 0, 0, 0))
    character.thumbnail((500, 1000), Image.Resampling.LANCZOS)
    x = (canvas.width - character.width) // 2
    y = canvas.height - character.height - 8
    canvas.alpha_composite(character, (x, y))
    canvas.save(out / f"{name}.png", optimize=True)
    print(out / f"{name}.png")
