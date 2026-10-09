"""Check the new artwork inventory offline. Add --pixels for Pillow sheet checks."""
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PIXEL = ASSETS / "pixel"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def png_size(path):
    data = path.read_bytes()
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"Not a PNG: {path}")
    offset, size, image_data, ended = 8, None, bytearray(), False
    while offset < len(data):
        require(offset + 12 <= len(data), f"Truncated PNG chunk: {path}")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        end = offset + 12 + length
        require(end <= len(data), f"Truncated PNG data: {path}")
        checksum = struct.unpack(">I", data[end - 4:end])[0]
        require(zlib.crc32(chunk + payload) & 0xFFFFFFFF == checksum, f"PNG checksum mismatch: {path}")
        if chunk == b"IHDR":
            require(offset == 8 and length == 13, f"Invalid PNG header: {path}")
            size = struct.unpack(">II", payload[:8])
        elif chunk == b"IDAT":
            image_data.extend(payload)
        elif chunk == b"IEND":
            require(end == len(data), f"Unexpected trailing PNG data: {path}")
            ended = True
        offset = end
    require(size and all(size) and ended and image_data, f"Incomplete PNG: {path}")
    zlib.decompress(image_data)
    return size


def main():
    manifest = json.loads((PIXEL / "manifest.json").read_text())
    entries = manifest["entries"]
    sources_list = json.loads((ASSETS / "sources.json").read_text())["sources"]
    sources = {s["id"]: s for s in sources_list}
    require(len(sources) == len(sources_list), "Duplicate source ID")
    paths = {e["path"]: e for e in entries}
    require(len(paths) == len(entries), "Duplicate asset path")
    require(len({p.casefold() for p in paths}) == len(paths), "Case-insensitive filename collision")
    for e in entries:
        rel = Path(e["path"])
        require(not rel.is_absolute() and ".." not in rel.parts, f"Unsafe relative path: {rel}")
        require(re.fullmatch(r"[a-z0-9/.-]+", str(rel)), f"Non-portable filename: {rel}")
        path = PIXEL / rel
        require(e["source"] in sources, f"Missing source: {rel}")
        require(path.is_file(), f"Missing asset: {rel}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == e["sha256"], f"Changed asset bytes: {rel}")
        require(png_size(path) == (e["width"], e["height"]), f"Wrong dimensions: {rel}")
    categories = {Path(p).parts[0] for p in paths}
    actual = {str(p.relative_to(PIXEL)) for cat in categories for p in (PIXEL / cat).rglob("*.png")}
    require(actual == set(paths), "Inventory differs from PNG files on disk")
    for source in sources.values():
        require((ASSETS / "licenses" / (source["license"] + ".txt")).is_file(), f'Missing license: {source["id"]}')
        require(re.fullmatch(r"[0-9a-f]{64}", source["archive_sha256"]), "Invalid archive hash")
        require(source["source_url"].startswith("https://"), "Missing source URL")
        if source.get("upstream_notice"):
            require((ASSETS / source["upstream_notice"]).is_file(), "Missing original license notice")
        if source["license"] == "CC-BY-3.0":
            require(all(word in source["attribution"] for word in ["PancInteractive", "OpenGameArt.org", "CC BY 3.0"]), "Incomplete food attribution")
    animations = json.loads((PIXEL / "animations.json").read_text())["animations"]
    sheet_count = 0
    for a in animations:
        w, h = a["frame_width"], a["frame_height"]
        for i, path in enumerate(a["frames"], 1):
            require(path in paths, f"Missing animation frame: {path}")
            e = paths[path]
            require((e["width"], e["height"], e["frame"]) == (w, h, i), f"Wrong frame metadata: {path}")
            require(e["animation"] == a["name"], f"Wrong sequence: {path}")
        if "sheet" not in a:
            continue
        sheet_count += 1
        e = paths[a["sheet"]]
        require((e["width"], e["height"], e["columns"], e["rows"]) == (w * len(a["frames"]), h, len(a["frames"]), 1), f'Wrong sheet layout: {a["name"]}')
        if "--pixels" in sys.argv:
            from PIL import Image
            with Image.open(PIXEL / a["sheet"]) as image:
                sheet = image.convert("RGBA")
            for i, frame_path in enumerate(a["frames"]):
                with Image.open(PIXEL / frame_path) as image:
                    frame = image.convert("RGBA")
                require(sheet.crop((i * w, 0, (i + 1) * w, h)).tobytes() == frame.tobytes(), f'Sheet pixels differ: {a["name"]}, frame {i + 1}')
    previews = list((ASSETS / "previews").glob("*.png"))
    for path in previews:
        png_size(path)
    markdown_files = [ROOT / "README.md", ROOT / "AGENTS.md"] + list(ASSETS.rglob("*.md"))
    link_count = 0
    for path in markdown_files:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            target = target.split(' "')[0]
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            require(dest.is_relative_to(ROOT), f"Link leaves repository: {path}: {target}")
            require(dest.exists(), f"Broken link: {path}: {target}")
            link_count += 1
    print(f"OK: {len(entries)} art PNGs, {len(categories)} categories, {len(sources)} source/license records.")
    print(f"OK: {len(animations)} animation/pose sequences, {sheet_count} sheets, {len(previews)} previews, {link_count} local links.")
    print("OK: PNG integrity, dimensions, SHA-256 hashes, complete inventory, portable paths, and license notices.")
    if "--pixels" in sys.argv:
        print("OK: every included sprite-sheet frame matches its individual PNG pixels.")
    print("Note: visual suitability and source license review are manual; this checker does not infer them.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, zlib.error) as error:
        print(f"Asset check failed: {error}", file=sys.stderr)
        sys.exit(1)
