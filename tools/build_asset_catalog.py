"""Rebuild the picture guides from the checked-in manifest (requires Pillow)."""
from collections import defaultdict
from pathlib import Path
import json
import io
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PIXEL = ASSETS / "pixel"
PREVIEWS = ASSETS / "previews"
PREVIEWS.mkdir(exist_ok=True)
MANIFEST = json.loads((PIXEL / "manifest.json").read_text())
ENTRIES = MANIFEST["entries"]
SOURCES = {s["id"]: s for s in json.loads((ASSETS / "sources.json").read_text())["sources"]}
CATEGORIES = {
    "characters": ("Characters & friendly creatures", "Explorers, robots, farmers, drivers, and an animated fox."),
    "animals": ("Animals", "Sheep, cow, chicken, frog, eagle, and opossum."),
    "vehicles": ("Vehicles", "Cars, buses, delivery trucks, emergency vehicles, and flying machines."),
    "terrain": ("Ground & platforms", "Grass, dirt, snow, water, islands, paths, and platforms."),
    "nature": ("Trees, plants & crops", "Trees, bushes, mushrooms, flowers, rocks, and growing vegetables."),
    "buildings": ("Buildings", "Houses, barns, roofs, doors, windows, castles, and hangars."),
    "items": ("Food & collectibles", "Meals, snacks, cherries, gems, coins, keys, and garden tools."),
    "props": ("Objects & decorations", "Crates, signs, fences, switches, pipes, buckets, and seed packets."),
    "backgrounds": ("Backgrounds", "Sky colors, clouds, hills, mountains, and a forest layer."),
    "effects": ("Sparkles & magic", "Glowing sparks, a magic poof, and a collectible sparkle."),
    "hazards": ("Cartoon obstacles", "Spikes and springs for jumping and bouncing games."),
    "ui": ("Hearts, numbers & symbols", "Health hearts, score digits, and simple game symbols."),
}


def font(size):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def fitted_image(entry, width, height):
    im = Image.open(PIXEL / entry["path"]).convert("RGBA")
    scale = min(width / im.width, height / im.height)
    scale = max(1, math.floor(scale)) if scale >= 1 else scale
    return im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.Resampling.NEAREST)


def credit_line(entries):
    ids = {e["source"] for e in entries}
    credits = []
    if ids - {"sunnyland", "crosstown-food"}:
        credits.append("Kenney (CC0)")
    if "sunnyland" in ids:
        credits.append("Ansimuz (CC0)")
    if "crosstown-food" in ids:
        credits.append("PancInteractive via OpenGameArt.org (CC BY 3.0)")
    return "Art: " + "; ".join(credits) + ". Full credits: assets/CREDITS.md"


def save_preview(canvas, path):
    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG", optimize=True)
    temporary = path.with_suffix(".png.tmp")
    temporary.write_bytes(buffer.getvalue())
    temporary.replace(path)


def contact_sheet(category, batch, page):
    cols, cw, ch = 8, 150, 134
    canvas = Image.new("RGB", (cols * cw, 58 + math.ceil(len(batch) / cols) * ch + 46), "#f0f4fa")
    draw = ImageDraw.Draw(canvas)
    draw.text((18, 14), f"{CATEGORIES[category][0]}  |  Page {page}", font=font(21), fill="#16324a")
    for i, e in enumerate(batch):
        x, y = (i % cols) * cw, 58 + (i // cols) * ch
        draw.rounded_rectangle((x + 3, y + 3, x + cw - 3, y + ch - 3), radius=8, fill="#dde7ee")
        im = fitted_image(e, cw - 16, 84)
        canvas.paste(im, (x + (cw - im.width) // 2, y + 7 + (84 - im.height) // 2), im)
        label = Path(e["path"]).stem
        for row, line in enumerate(textwrap.wrap(label, 23, break_on_hyphens=True)[:2]):
            draw.text((x + 8, y + 94 + 13 * row), line, font=font(10), fill="#102d42")
        draw.text((x + 8, y + 120), f'{e["width"]} x {e["height"]}', font=font(9), fill="#496171")
    draw.text((14, canvas.height - 31), credit_line(batch), font=font(11), fill="#16324a")
    name = f"{category}-{page:02d}.png"
    save_preview(canvas, PREVIEWS / name)
    return name


def category_guide(category, entries):
    title, description = CATEGORIES[category]
    lines = [f"# {title}", "", description, "", "[Back to all artwork](../README.md)", "",
             f"**{len(entries)} PNG files.** Pick a picture below, then find its filename in the list.", "",
             "Keep images from the same pack together when you want a matching look. Sizes are the original pixel sizes.", ""]
    for page, start in enumerate(range(0, len(entries), 64), 1):
        batch = entries[start:start + 64]
        preview = contact_sheet(category, batch, page)
        lines += [f"## Picture guide {page}", "", f"![{title}, page {page}](../../previews/{preview})", "",
                  "<details>", "<summary>Open the filenames and download links</summary>", "",
                  "| File | Pack | Pixels | Kind |", "| --- | --- | --- | --- |"]
        for e in batch:
            relative = str(Path(e["path"]).relative_to(category))
            lines.append(f'| [{relative}]({relative}) | {SOURCES[e["source"]]["title"]} | {e["width"]} x {e["height"]} | {e["kind"].replace("_", " ")} |')
        lines += ["", "</details>", ""]
    lines += ["## Credits", "", "Keep [the relevant credits](../../CREDITS.md) with artwork you copy into a game.", ""]
    for source_id in sorted({e["source"] for e in entries}):
        s = SOURCES[source_id]
        lines += [f'- [{s["title"]}]({s["source_url"]}) — {s["creator"]}; [{s["license"]}]({s["license_url"]}).']
    if category in {"animals", "characters", "items", "effects"}:
        lines += ["", "For moving pictures, see the [animation guide](../ANIMATIONS.md)."]
    if category == "backgrounds":
        lines += ["", "Most Kenney backgrounds are 24 x 24 tiles to repeat across the screen. SunnyLand has larger scene layers."]
    (PIXEL / category / "README.md").write_text("\n".join(lines) + "\n")


def overview(grouped):
    canvas = Image.new("RGB", (1200, 1030), "#f5f8fd")
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, 1200, 132), fill="#173b54")
    d.text((34, 23), "PICK YOUR GAME ART", font=font(37), fill="white")
    d.text((36, 82), f"{len(ENTRIES)} image files  /  {len(CATEGORIES)} categories  /  7 art packs", font=font(20), fill="#bfe9ec")
    picks = {
        "characters": ["green-explorer-pose-1", "fox-run-frame-01", "farmer-hat"],
        "animals": ["cow", "frog-idle-frame-01", "opossum-run-frame-01"],
        "vehicles": ["school-bus", "firetruck", "blue-jet"],
        "terrain": ["grass-single", "snow-single", "coast-grass-top-left"],
        "nature": ["sunflower", "carrot-ready", "green-tree"],
        "buildings": ["straw-house", "barn-door-large", "brown-doorway"],
        "items": ["hamburger", "donut", "gem-sparkle-frame-01"],
        "props": ["sign-left", "wooden-crate", "carrot-crate"],
        "backgrounds": ["clouds-trees", "sky-and-mountains", "green-trees"],
        "effects": ["magic-poof-frame-03", "collect-sparkle-frame-02", "spark-cross"],
        "hazards": ["spikes-double", "spring-raised", "spikes-top"],
        "ui": ["heart-full", "number-bold-3", "number-bold-9"],
    }
    for index, (category, (title, _)) in enumerate(CATEGORIES.items()):
        x, y = 22 + (index % 3) * 393, 150 + (index // 3) * 207
        d.rounded_rectangle((x, y, x + 371, y + 189), radius=15, fill="#e2edf1")
        d.text((x + 16, y + 14), title, font=font(18), fill="#173b54")
        d.text((x + 16, y + 43), f'{len(grouped[category])} files  /  {category}/', font=font(13), fill="#496777")
        chosen = []
        for prefix in picks[category]:
            e = next((e for e in grouped[category] if Path(e["path"]).stem.startswith(prefix)), None)
            if e is not None:
                chosen.append(e)
        for j, e in enumerate(chosen):
            im = fitted_image(e, 103, 96)
            canvas.paste(im, (x + 17 + j * 117 + (103 - im.width) // 2, y + 79 + (96 - im.height) // 2), im)
    d.text((24, 993), credit_line(ENTRIES), font=font(12), fill="#254958")
    save_preview(canvas, PREVIEWS / "overview.png")


def main():
    grouped = defaultdict(list)
    for e in ENTRIES:
        grouped[e["path"].split("/")[0]].append(e)
    for category in CATEGORIES:
        category_guide(category, grouped[category])
    overview(grouped)
    lines = ["# Pick your game artwork", "", "Choose a folder, open its picture guide, and pick something fun!", "",
             "![A sample from every artwork category](../previews/overview.png)", "",
             f"This collection adds **{len(ENTRIES)} PNG image files** from seven art packs. There are individual sprites, tiles, animation frames, and 17 verified sprite sheets.", "",
             "| What do you need? | Folder | Files |", "| --- | --- | ---: |"]
    for category, (title, _) in CATEGORIES.items():
        lines.append(f'| {title} | [{category}/]({category}/README.md) | {len(grouped[category])} |')
    lines += ["", "## Try an idea", "",
              '- "Make a farm game where I grow carrots and look after a cow."',
              '- "Make a delivery game with a school bus and a little town."',
              '- "Make a fox jumping game where I collect cherries."',
              '- "Make a flying game where I explore islands and collect gems."', "",
              "## Finding matching art", "",
              "Inside each category, files are grouped by the original art pack. Pick the same pack for a matching look. The picture guides show filenames and sizes. A number at the end of a tile name identifies its original tile in the pack.", "",
              "- **Pixel Platformer:** 18 x 18 ground tiles; 24 x 24 characters and background tiles.",
              "- **Tiny Town and Tiny Farm:** 16 x 16 tiles in a compatible small style.",
              "- **Pixel Shmup:** 16 x 16 terrain and icons; 32 x 32 flying vehicles.",
              "- **Pixel Vehicle Pack, food, and SunnyLand:** varied image sizes; see each picture guide.", "",
              "For moving characters and effects, use the [animation guide](ANIMATIONS.md).", "",
              "Phippy and the existing workshop artwork are still listed in the [main artwork guide](../README.md).", "",
              "## For game builders", "",
              "Use the individual PNGs directly in Godot. For example:", "",
              "```text", "res://assets/pixel/vehicles/pixel-vehicle-pack/school-bus.png", "res://assets/pixel/animals/tiny-farm/cow-0121.png", "```", "",
              "Set CanvasItem texture filtering to **Nearest** for crisp pixels and scale sprites by whole numbers when practical. These files keep their original pixels and dimensions. Most tiny terrain pieces are tiles, not full backgrounds. The manifest lists image sizes; it does not define collisions or Godot TileSet terrain rules.", "",
              "The [manifest](manifest.json) maps every new image to its original filename, source pack, size, and SHA-256 checksum. [Source details](../sources.json) record download URLs, versions, license IDs, and archive checksums.", "",
              "## Credits travel with the artwork", "",
              "See [CREDITS.md](../CREDITS.md) for creator names, source links, and reuse rules. Food from Crosstown Smash requires attribution in games that use it. The remaining new packs use CC0; voluntary credits are included too. The repository's Apache-2.0 license does not replace the artwork licenses.", ""]
    (PIXEL / "README.md").write_text("\n".join(lines))
    print(f"Built 12 category guides and {len(list(PREVIEWS.glob('*.png')))} previews.")


if __name__ == "__main__":
    main()
